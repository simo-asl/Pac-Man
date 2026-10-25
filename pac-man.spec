# Build with: make package
from pathlib import Path

root = Path(SPECPATH)
a = Analysis(
    [str(root / 'pac-man.py')],
    pathex=[str(root)],
    binaries=[],
    datas=[(str(root / 'src/assets/arcade'), 'src/assets/arcade')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name='pac-man', debug=False, strip=False, upx=False, console=True,
)
