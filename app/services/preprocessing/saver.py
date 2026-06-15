from pathlib import Path
import re

import numpy as np
import soundfile as sf  # type: ignore[import-untyped]


UUID_PATTERN = re.compile(
    r"[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}"
)


class AudioSaver:
    def save(
        self,
        audio: np.ndarray,
        sample_rate: int,
        source_path: Path,
        output_dir: Path,
    ) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)

        audio_uuid = self._extract_uuid_from_filename(source_path)
        output_path = output_dir / f"{audio_uuid}.wav"

        sf.write(
            file=output_path,
            data=audio,
            samplerate=sample_rate,
        )

        return output_path

    def _extract_uuid_from_filename(self, source_path: Path) -> str:
        filename_without_extension = source_path.stem

        uuid_match = UUID_PATTERN.search(filename_without_extension)

        if uuid_match is not None:
            return uuid_match.group(0)

        return filename_without_extension
