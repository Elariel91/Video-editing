"""Run an individual production stage from any working directory."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
STAGES = {
    'assets': 'bootstrap_assets.py',
    'narrate': 'narrate.py',
    'prepare': 'prepare_media.py',
    'broll': 'filmcraft_broll.py',
    'build': 'build_video.py',
    'finish': 'finish_filmcraft.py',
    'cover': 'make_cover.py',
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('stage', choices=[*STAGES, 'check', 'snapshot', 'preview', 'render'])
args = parser.parse_args()
env = os.environ.copy()
env['PATH'] = str(ROOT / 'tools/bin') + os.pathsep + env.get('PATH', '')
if args.stage in STAGES:
    command = [sys.executable, str(ROOT / 'tools' / STAGES[args.stage])]
else:
    npx = shutil.which('npx.cmd' if os.name == 'nt' else 'npx')
    if not npx:
        raise SystemExit('Install Node.js 22+ and npm first.')
    tail = {
        'check': ['check'],
        'snapshot': ['snapshot', '--at', '5.2,11.1,17.2,25.5,32,39.5,46,52'],
        'preview': ['preview', '--background'],
        'render': ['render', '--quality', 'delivery', '--workers', '1', '--output', 'renders/graphics-master.mp4'],
    }[args.stage]
    command = [npx, '--yes', 'hyperframes@0.8.162', *tail]
raise SystemExit(subprocess.call(command, cwd=ROOT, env=env))
