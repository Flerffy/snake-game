import os
import math
import wave
import struct
import pygame

# Simple sound manager for SFX and BGM. Keeps loaded sounds cached so repeated
# requests reuse the same pygame.mixer.Sound instances.

_SFX = {}
_BGM = {}
_SFX_INITIALIZED = False
# store sfx and bgm under assets/ for clearer organization
BASE_ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
SFX_DIR = os.path.join(BASE_ASSETS_DIR, 'sfx')
BGM_DIR = os.path.join(BASE_ASSETS_DIR, 'bgm')
_BEEP_PATH = os.path.join(SFX_DIR, 'sfx_beep.wav')


def _ensure_asset_dirs():
    try:
        os.makedirs(SFX_DIR, exist_ok=True)
        os.makedirs(BGM_DIR, exist_ok=True)
    except Exception:
        # best-effort; creation may fail in restricted envs
        pass


def _ensure_mixer():
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except Exception:
        # best-effort, callers should tolerate None returns
        pass


def _create_beep_wav(path, freq_hz=880, duration_ms=120, volume=0.5, sample_rate=44100):
    """Create a mono 16-bit PCM WAV file at `path` containing a sine beep.

    Applies a simple ADSR envelope to reduce harshness.
    """
    # default envelope params (ms)
    attack_ms = 5
    decay_ms = 30
    sustain_level = 0.8
    release_ms = 60

    n_samples = int(sample_rate * (duration_ms / 1000.0))
    max_amp = 2 ** 15 - 1

    def _env(i):
        t_ms = (i / sample_rate) * 1000.0
        if t_ms < attack_ms:
            return (t_ms / attack_ms)
        t_ms -= attack_ms
        if t_ms < decay_ms:
            # decay from 1.0 -> sustain_level
            return 1.0 - (1.0 - sustain_level) * (t_ms / decay_ms)
        # sustain until release region
        release_start_ms = max(0.0, duration_ms - release_ms)
        if (i / sample_rate) * 1000.0 >= release_start_ms:
            # in release
            rel_t = ((i / sample_rate) * 1000.0) - release_start_ms
            return sustain_level * max(0.0, 1.0 - (rel_t / release_ms))
        return sustain_level

    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)

        for i in range(n_samples):
            sample_t = i / sample_rate
            env = _env(i)
            sample = volume * env * math.sin(2 * math.pi * freq_hz * sample_t)
            val = int(max(-1.0, min(1.0, sample)) * max_amp)
            data = struct.pack('<h', val)
            wf.writeframesraw(data)

        wf.writeframes(b'')


def _create_chord_wav(path, freqs, duration_ms=120, volume=0.5, sample_rate=44100):
    """Create a mono 16-bit PCM WAV file containing a chord made by summing
    the given list of frequencies (in Hz). `freqs` is an iterable of numbers.
    The mixed signal is normalized so clipping is avoided.
    """
    freqs = list(freqs)
    if not freqs:
        return
    n_samples = int(sample_rate * (duration_ms / 1000.0))
    max_amp = 2 ** 15 - 1
    n_notes = len(freqs)

    # envelope params (ms)
    attack_ms = 8
    decay_ms = 50
    sustain_level = 0.75
    release_ms = 80

    def _env(i):
        t_ms = (i / sample_rate) * 1000.0
        if t_ms < attack_ms:
            return (t_ms / attack_ms)
        t_ms -= attack_ms
        if t_ms < decay_ms:
            return 1.0 - (1.0 - sustain_level) * (t_ms / decay_ms)
        release_start_ms = max(0.0, duration_ms - release_ms)
        if (i / sample_rate) * 1000.0 >= release_start_ms:
            rel_t = ((i / sample_rate) * 1000.0) - release_start_ms
            return sustain_level * max(0.0, 1.0 - (rel_t / release_ms))
        return sustain_level

    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)

        for i in range(n_samples):
            t = i / sample_rate
            s = 0.0
            for f in freqs:
                s += math.sin(2 * math.pi * f * t)
            # normalize by number of notes
            sample_base = (s / n_notes)
            env = _env(i)
            sample = volume * env * sample_base
            val = int(max(-1.0, min(1.0, sample)) * max_amp)
            data = struct.pack('<h', val)
            wf.writeframesraw(data)

        wf.writeframes(b'')


def init_sounds(load_beep=True, freq_hz=880, duration_ms=120, volume=0.5, sample_rate=44100):
    """Initialize mixer and load builtin SFX (only 'beep' by default).
    Returns True if mixer and at least one SFX is available."""
    global _SFX_INITIALIZED
    if _SFX_INITIALIZED:
        return bool(_SFX)
    _SFX_INITIALIZED = True

    _ensure_mixer()
    _ensure_asset_dirs()
    if load_beep:
        try:
            # default high-pitched beep
            # Create a high C-major chord for success (C8,E8,G8)
            c4 = 261.6256
            e4 = 329.6276
            g4 = 392.0
            # target success chord at C8 (4 octaves above C4 -> *16)
            c8 = c4 * 16.0
            e8 = e4 * 16.0
            g8 = g4 * 16.0
            if not os.path.exists(_BEEP_PATH):
                chord_args = {
                    'freqs': [c8, e8, g8],
                    'duration_ms': duration_ms,
                    'volume': volume,
                    'sample_rate': sample_rate,
                }
                _create_chord_wav(_BEEP_PATH, **chord_args)
            snd = pygame.mixer.Sound(_BEEP_PATH)
            _SFX['beep'] = snd
            # also create a low-frequency C-minor chord for collisions ~2 octaves lower
            low_path = os.path.join(SFX_DIR, 'sfx_low_beep.wav')
            if not os.path.exists(low_path):
                # use C6 (two octaves above C4 -> *4) for the low beep (C6, Eb6, G6)
                c6 = c4 * 4.0
                # Eb6 is E-flat at the 6th octave
                eb6 = e4 * 4.0 * (2 ** (-1/12))
                g6 = g4 * 4.0
                low_args = {
                    'freqs': [c6, eb6, g6],
                    'duration_ms': max(160, duration_ms + 40),
                    'volume': max(0.25, volume * 0.9),
                    'sample_rate': sample_rate,
                }
                _create_chord_wav(low_path, **low_args)
            try:
                _SFX['low_beep'] = pygame.mixer.Sound(low_path)
            except Exception:
                _SFX.pop('low_beep', None)
        except Exception:
            # keep going; callers will see missing entry
            _SFX.pop('beep', None)

    return bool(_SFX)


def get_sfx(name):
    """Return the pygame.mixer.Sound for `name` or None if not available."""
    return _SFX.get(name)


def play_sfx(name, volume=None):
    """Play a short sound effect by name. If `volume` is provided (0.0-1.0)
    it will be applied for this play call only."""
    snd = get_sfx(name)
    if snd is None:
        # try to lazily initialize builtins
        init_sounds()
        snd = get_sfx(name)
        if snd is None:
            return False

    try:
        if volume is not None:
            prev = snd.get_volume()
            snd.set_volume(float(max(0.0, min(1.0, volume))))
            snd.play()
            snd.set_volume(prev)
        else:
            snd.play()
        return True
    except Exception:
        return False


def register_sfx(name, path):
    """Load and register a SFX from a file path under the given name."""
    _ensure_mixer()
    try:
        snd = pygame.mixer.Sound(path)
        _SFX[name] = snd
        return True
    except Exception:
        return False


# Basic BGM control using pygame.mixer.music
def play_bgm(path_or_name, loops=-1):
    """Play background music. If path_or_name matches a registered key in
    _BGM, its path is used; otherwise the string is treated as a file path."""
    _ensure_mixer()
    path = _BGM.get(path_or_name, path_or_name)
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops)
        return True
    except Exception:
        return False


def stop_bgm():
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass


def set_bgm_volume(vol):
    try:
        pygame.mixer.music.set_volume(max(0.0, min(1.0, float(vol))))
    except Exception:
        pass


def set_sfx_volume(vol):
    try:
        v = max(0.0, min(1.0, float(vol)))
        for snd in _SFX.values():
            try:
                snd.set_volume(v)
            except Exception:
                pass
    except Exception:
        pass
