from dataclasses import dataclass

@dataclass
class AudioPreprocessingConfig:
    target_sample_rate: int = 16_000

    apply_length_filter: bool = True
    min_duration_seconds: float = 1.0
    max_duration_seconds: float | None = 30.0

    apply_silent_filter: bool = True
    silence_rms_threshold: float = 0.005

    # TODO: noice filter
    # apply_noise_filter: bool = False
    # noise_threshold: float = 0.01