"""Create a portable Linux release archive after PyInstaller finishes."""

from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


def main() -> int:
    """Bundle the executable, editable configuration and instructions.

    Returns:
        int: Zero on success, or one after a reported application error.
    """
    try:
        with ZipFile("dist/pac-man-linux.zip", "w", ZIP_DEFLATED) as archive:
            for source, name in (
                ("dist/pac-man", "pac-man"),
                ("config.json", "config.json"),
                ("README.md", "README.md"),
                ("CHECKLIST.md", "CHECKLIST.md"),
                ("CHANGES.md", "CHANGES.md"),
                ("src/assets/arcade/LICENSE.md",
                 "src/assets/arcade/LICENSE.md"),
            ):
                archive.write(Path(source), name)
            for document in Path("project-management").glob("*.md"):
                archive.write(document, document.as_posix())
        return 0
    except OSError as error:
        print(f"Cannot package Pac-Man: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
