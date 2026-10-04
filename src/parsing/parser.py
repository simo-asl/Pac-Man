from .modele import ConfigLevel, GameConfig
from pathlib import Path
import json


class Parser:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)

    def _read_file(self) -> str:
        if not self.file_path.exists():
            raise FileNotFoundError("Didnt Find the file")
        return self.file_path.read_text()

    def _remove_comments(self, text: str) -> str:
        new = []
        inside_block = False
        for line in text.splitlines():
            stripped = line.lstrip()

            if inside_block:
                if "*/" in stripped:
                    inside_block = False
                continue

            if stripped.startswith("#"):
                continue

            if stripped.startswith("//"):
                continue

            if stripped.startswith("/*"):
                inside_block = True
                continue

            new.append(line)
        return "\n".join(new)
