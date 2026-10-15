"""Fetch source assets from their publishers; generated media is not in Git."""
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
FILES = {
    'boardroom-1785.mp4': 'https://assets.mixkit.co/videos/1785/1785-720.mp4',
    'stock-308.mp4': 'https://assets.mixkit.co/videos/308/308-720.mp4',
    'stock-241.mp4': 'https://assets.mixkit.co/videos/241/241-720.mp4',
    'stock-4809.mp4': 'https://assets.mixkit.co/videos/4809/4809-720.mp4',
    'Inter.ttf': 'https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf',
    'Inter-OFL.txt': 'https://raw.githubusercontent.com/google/fonts/main/ofl/inter/OFL.txt',
    'SpaceGrotesk.ttf': 'https://raw.githubusercontent.com/google/fonts/main/ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf',
    'SpaceGrotesk-OFL.txt': 'https://raw.githubusercontent.com/google/fonts/main/ofl/spacegrotesk/OFL.txt',
}
for name, url in FILES.items():
    target = ASSETS / name
    if target.exists():
        print('Already present:', name)
        continue
    print('Downloading:', name, flush=True)
    temporary = target.with_suffix(target.suffix + '.part')
    with urlopen(url, timeout=120) as source, temporary.open('wb') as output:
        while chunk := source.read(1024 * 1024):
            output.write(chunk)
    temporary.replace(target)
