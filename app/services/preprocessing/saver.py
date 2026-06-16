from pathlib import Path
from uuid import UUID

import numpy as np
import soundfile as sf  # type: ignore[import-untyped]


class AudioSaver:
    def save(
        self,
        audio: np.ndarray,
        sample_rate: int,
        source_path: Path,
        output_dir: Path,
    ) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)

        audio_uuid = self.extract_uuid_from_filename(source_path)
        output_path = output_dir / f"{audio_uuid}.wav"

        sf.write(
            file=str(output_path),
            data=audio,
            samplerate=sample_rate,
        )

        return output_path

    def extract_uuid_from_filename(self, source_path: Path) -> str:
        filename_without_extension = source_path.stem

        try:
            UUID(filename_without_extension)
        except ValueError:
            return filename_without_extension

        return filename_without_extension