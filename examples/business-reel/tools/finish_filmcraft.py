import pathlib,json,subprocess,shutil,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
from runtime import resolve_cli
FC=resolve_cli('FILMCRAFT_CLI', 'filmcraft-cli')
OUT=ROOT/'deliverables';OUT.mkdir(exist_ok=True)
PROJECT=ROOT/'business-reel-final.fcproj'
timing=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'));T=254016000000; seqcount=0
def call(args):
    r=subprocess.run([FC]+args,capture_output=True,text=True,encoding='utf-8')
    with (ROOT/'tools/final-filmcraft.log').open('a',encoding='utf-8') as f:f.write(r.stdout+r.stderr+'\n')
    if r.returncode:raise RuntimeError(r.stdout+r.stderr)
    if not r.stdout.strip(): return None
    try:return json.loads(r.stdout)
    except json.JSONDecodeError:return [json.loads(line) for line in r.stdout.splitlines() if line.startswith('{')]
def command(id,**params):return call(['--project',str(PROJECT),'--save','exec',id,json.dumps(params)])
def run(actions):
    global seqcount
    seqcount+=1;p=ROOT/'tools'/f'final-stage-{seqcount}.jsonl'
    p.write_text('\n'.join(json.dumps({'id':id,'params':params}) for id,params in actions))
    call(['--project',str(PROJECT),'--save','run',str(p)])
def inspect():return call(['--project',str(PROJECT),'inspect','sequence'])
def addfile(path):return call(['--project',str(PROJECT),'--save','import',str(path)])['items'][0]
if PROJECT.exists(): raise SystemExit('Final project already exists; move it aside before rebuilding.')
call(['--save-as',str(PROJECT),'exec','file.newSequence',json.dumps({'name':'Start a business — final Reel','width':1080,'height':1920,'fps':30,'video':3,'audio':3})])
master=addfile(ROOT/'renders/graphics-master.mp4')
run([('source.open',{'item':master}),('source.overwrite',{})])
sq=inspect(); voice=[c['clip'] for tr in sq['audio'] for c in tr['items']]
for c in voice:command('clip.audioGain',clips=[c],mode='adjust',db=4.5)
for fname,track,gain in [('original-score.wav','A2',-1),('step-accents.wav','A3',-8)]:
    item=addfile(ROOT/'assets'/fname)
    run([('playhead.set',{'seconds':timing['duration']}),('source.open',{'item':item}),('source.overwrite',{})])
    sq=inspect();clip=next(c['clip'] for tr in sq['audio'] for c in tr['items'] if c['item']==item)
    command('timeline.move',moves=[{'clip':clip,'track':track,'time':0}],insert=False,linked=False)
    command('clip.audioGain',clips=[clip],mode='adjust',db=gain)
    if track=='A2':
        command('sequence.applyAudioTransition',clip=clip,effect='constant_gain',frames=18,edge='in')
        command('sequence.applyAudioTransition',clip=clip,effect='exponential_fade',frames=45,edge='out')
command('mixer.addInsert',strip='Mix',effect='hard_limiter',slot=0)
command('mixer.setInsert',strip='Mix',slot=0,params={'max':-1,'boost':0,'lookahead':7,'release':100})
for s in timing['scenes']:
    tm=round(s['start']*30)*T//30
    if tm:command('timeline.razor',time=tm,track='V1')
    command('markers.add',target='program',time=tm,name=s['label'],comment=s['text'])
command('project.setNotes',text='54.47s portrait Reel. FilmCraft: stock selects, framing, Lumetri correction, final edit, +4.5dB voice, low original score, step accents, music fades and master limiter. HyperFrames: typography, illustrations, cards and word-timed captions. PhotoCraft: layered cover. Script and source credits accompany project.')
shutil.copy2(ROOT/'SCRIPT.md',OUT/'SCRIPT.md');shutil.copy2(ROOT/'captions.srt',OUT/'captions.srt')
print('FilmCraft final timeline assembled. Exporting...',flush=True)
command('file.exportMedia',path=str(OUT/'start-a-business-reel.mp4'),preset='Social Vertical 1080×1920',format='h264',width=1080,height=1920,fps=30,bitrateKbps=12000,audio=True,loudnessLufs=-16,hardwareEncoding='off',wait=True)
print('Finished FilmCraft export:',OUT/'start-a-business-reel.mp4',flush=True)
