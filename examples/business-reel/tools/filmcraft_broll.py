import pathlib, json, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
from runtime import resolve_cli
FC=resolve_cli('FILMCRAFT_CLI', 'filmcraft-cli')
T=254016000000
shots=[('boardroom-1785',4,104,[540,340],.12,7,-12,8),('stock-308',3,98,[540,340],.12,5,-15,7),('stock-241',1,100,[540,340],.05,5,-12,5),('stock-4809',2,100,[540,340],.10,5,-12,6)]
for name,mark,scale,pos,exposure,contrast,highlights,shadows in shots:
    output=ROOT/'assets'/f'{name}-edit.mp4'
    project=ROOT/f'{name}.fcproj'
    if output.exists(): continue
    actions=[
      {'id':'file.newSequence','params':{'name':name+' — corrected select','width':1080,'height':680,'fps':30,'video':3,'audio':3}},
      {'id':'file.import','params':{'paths':[str(ROOT/'assets'/f'{name}.mp4')]}},
      {'id':'project.setMarks','params':{'item':8,'in':mark*T,'out':(mark+5)*T}},
      {'id':'source.open','params':{'item':8}},
      {'id':'source.overwrite','params':{}},
      {'id':'effects.setParam','params':{'clip':9,'effect':'motion','param':'scale','value':scale}},
      {'id':'effects.setParam','params':{'clip':9,'effect':'motion','param':'position','value':pos}},
      {'id':'effects.apply','params':{'clips':[9],'effect':'lumetri'}}]
    for p,v in [('exposure',exposure),('contrast',contrast),('highlights',highlights),('shadows',shadows),('saturation',97)]:
        actions.append({'id':'effects.setParam','params':{'clip':9,'effect':'lumetri','param':p,'value':v}})
    actions.append({'id':'project.setNotes','params':{'text':'Business Reel: five-second select, reframed for the graphic window. Restrained Lumetri exposure, highlight recovery, shadow lift and contrast correction.'}})
    script=ROOT/'tools'/f'{name}.jsonl'
    script.write_text('\n'.join(json.dumps(a) for a in actions))
    print('Preparing',name,flush=True)
    r=subprocess.run([FC,'--save-as',str(project),'run',str(script)],capture_output=True,text=True)
    (ROOT/'tools'/f'{name}-commands.log').write_text(r.stdout+r.stderr)
    if r.returncode: print(r.stdout,r.stderr); sys.exit(r.returncode)
    r=subprocess.run([FC,'--project',str(project),'export',str(output),'--format','h264','--gpu-rendering','off','--no-audio'],capture_output=True,text=True)
    (ROOT/'tools'/f'{name}-export.log').write_text(r.stdout+r.stderr)
    if r.returncode: print(r.stdout,r.stderr); sys.exit(r.returncode)
    print('Exported',output.name,output.stat().st_size,flush=True)
