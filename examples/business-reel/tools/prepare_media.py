import sys, pathlib, json, subprocess, shutil, math, wave
ROOT = pathlib.Path(__file__).resolve().parents[1]
import imageio_ffmpeg, numpy as np
import os, platform
(ROOT/'assets').mkdir(exist_ok=True)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
BIN = ROOT/'tools/bin'; BIN.mkdir(exist_ok=True)
shutil.copy2(FFMPEG, BIN/('ffmpeg.exe' if os.name=='nt' else 'ffmpeg'))
host={'Windows':'win32','Darwin':'darwin','Linux':'linux'}[platform.system()]
arch='arm64' if platform.machine().lower() in ('arm64','aarch64') else 'x64'
probe_name='ffprobe.exe' if os.name=='nt' else 'ffprobe'
probe_source=shutil.which('ffprobe') or str(ROOT/'tools/node_modules/ffprobe-static/bin'/host/arch/probe_name)
if not pathlib.Path(probe_source).exists(): raise SystemExit('Install ffprobe on PATH for this platform.')
shutil.copy2(probe_source, BIN/probe_name)
if os.name!='nt':
    (BIN/'ffmpeg').chmod(0o755); (BIN/probe_name).chmod(0o755)
shutil.copy2(ROOT/'tools/node_modules/gsap/dist/gsap.min.js', ROOT/'assets/gsap.min.js')
PROBE = str(BIN/probe_name)
scenes = json.loads((ROOT/'scenes.json').read_text(encoding='utf-8'))
cursor = 0
voice_parts=[]
sr=48000
for i,s in enumerate(scenes):
    p=ROOT/'assets'/f"{s['id']}.mp3"
    duration=float(subprocess.check_output([PROBE,'-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)]))
    s['start']=round(cursor,6)
    s['duration']=math.ceil((duration+.10+(0.4 if i==7 else 0))*30)/30
    s['words']=json.loads((ROOT/'assets'/f"{s['id']}.words.json").read_text())
    pcm=subprocess.check_output([FFMPEG,'-v','error','-i',str(p),'-f','s16le','-ac','1','-ar',str(sr),'-'])
    samples=np.frombuffer(pcm,dtype=np.int16)
    part=np.zeros(round(s['duration']*sr),dtype=np.int16)
    part[:min(len(part),len(samples))]=samples[:len(part)]
    voice_parts.append(part)
    cursor+=s['duration']
assert 40<=cursor<=60, cursor
def wav(name, signal):
    with wave.open(str(ROOT/'assets'/name),'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr); f.writeframes(signal.astype(np.int16).tobytes())
wav('narration.wav',np.concatenate(voice_parts))
# Original restrained electronic score: a repeating four-chord figure, soft bass and percussion.
n=round(cursor*sr); music=np.zeros(n,dtype=np.float64); beat=60/112
chords=[(146.832,174.614,220),(130.813,164.814,195.998),(110,130.813,164.814),(130.813,174.614,220)]
for k in range(math.ceil(cursor/(beat*4))):
    start=round(k*beat*4*sr); length=min(round(beat*4.2*sr),n-start)
    if length<=0: break
    t=np.arange(length)/sr
    env=np.minimum(t/.12,1)*np.minimum((length/sr-t)/.35,1)
    pad=sum(np.sin(2*np.pi*f*t)+.15*np.sin(2*np.pi*f*2*t) for f in chords[k%4])/3
    music[start:start+length]+=.09*pad*env
for k in range(math.ceil(cursor/beat)):
    start=round(k*beat*sr); length=min(round(.22*sr),n-start)
    if length<=0: break
    t=np.arange(length)/sr
    music[start:start+length]+=.2*np.sin(2*np.pi*(52*t+5*(1-np.exp(-t*35))))*np.exp(-t*23)
for k in range(math.ceil(cursor/(beat/2))):
    start=round(k*beat/2*sr); length=min(round(.045*sr),n-start)
    if length<=0: break
    t=np.arange(length)/sr
    music[start:start+length]+=.025*(np.sin(2*np.pi*7823*t)+np.sin(2*np.pi*6137*t))*np.exp(-t*90)
wav('original-score.wav',np.clip(music,-1,1)*20000)
# Separate short, original UI tick/impact accents for the FilmCraft sound mix.
sfx=np.zeros(n,dtype=np.float64)
for s in scenes:
    start=round((s['start']+.12)*sr); length=min(round(.18*sr),n-start); t=np.arange(length)/sr
    sfx[start:start+length]+=.22*np.sin(2*np.pi*(180*t+35*t*t))*np.exp(-t*34)
wav('step-accents.wav',sfx*32767)
(ROOT/'timing.json').write_text(json.dumps({'duration':round(cursor,6),'scenes':scenes},indent=2))
script='# Script — Start a business\n\n**Voice:** Aria, English (US), Microsoft neural TTS\n\n**Delivery:** Clear, confident and conversational; brisk but with pauses between steps.\n\n'
board=f'---\nformat: 1080x1920\nduration: {cursor:.3f}s\nmessage: Validate demand, define one offer, launch small.\narc: how-to-process\naudience: first-time founders\nmode: autonomous\nmusic: original electronic score mixed in FilmCraft\n---\n\n## Video direction\n\nBlockFrame palette, bold type, hard-edged cards. Word-timed captions occupy y=1490–1680. Main teaching content stays between y=260 and y=1380. A six-step progress strip connects the film. FilmCraft supplies cut, reframed and corrected B-roll; HyperFrames supplies the complete graphics and caption treatment. One clear teaching move per scene.\n\n'
for i,s in enumerate(scenes,1):
    end=s['start']+s['duration']
    script+=f"## Line {i} — {s['label']} (Frame {i})\n\n**Time:** {s['start']:.2f}–{end:.2f}s\n\n    {s['text']}\n\n"
    board+=f"## Frame {i} — {s['label']}\n\n- status: outline\n- src: compositions/frames/{s['id']}.html\n- duration: {s['duration']:.6f}s\n- transition_in: cut\n- scene: {' '.join(s['title'])} {s['accent']}\n- voiceover: {s['text']}\n- blueprint: compose\n- focal: {' '.join(s['title'])}\n- roles: headline = foreground; numbered cards = supporting\n\nScene 1 (0–1.0s): headline lands with a bounded kinetic entrance.\nScene 2 (1.0–{s['duration']*.65:.2f}s): teaching cards reveal in narration order; selected B-roll provides context.\nScene 3 ({s['duration']*.65:.2f}–{s['duration']:.2f}s): accent takeaway lands and holds for reading. Captions follow exact spoken word timestamps.\n\n"
(ROOT/'SCRIPT.md').write_text(script,encoding='utf-8')
(ROOT/'STORYBOARD.md').write_text(board,encoding='utf-8')
print('Prepared voice, original score, sound accents, script, storyboard. Duration:',round(cursor,3),flush=True)
