import pathlib,json,subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
from runtime import resolve_cli
PC=resolve_cli('PHOTOCRAFT_CLI', 'photocraft-cli')
out=ROOT/'deliverables';out.mkdir(exist_ok=True)
actions=[]
def shape(name,x,y,w,h,color):
    actions.append(('shape.create',{'kind':'rect','rect':[x,y,w,h],'fill':color,'stroke':{'width':4,'color':'#000000'},'name':name}))
def text(name,copy,x,y,size,color='#000000',weight=900):
    actions.append(('type.create',{'x':x,'y':y,'text':copy,'font':'Arial','weight':weight,'size':size,'color':color,'name':name}))
text('Series','THE BUSINESS STARTER',84,220,28,weight=700)
shape('Rule',84,255,912,4,'#000000')
shape('Label',84,310,370,78,'#FFFDF5')
text('Step count','6 PRACTICAL STEPS',105,363,28,weight=700)
text('Start','START A',78,590,140)
text('Business','BUSINESS',78,755,140)
text('Promise','FROM IDEA TO FIRST CUSTOMER',84,835,33,weight=700)
for j,(a,b,color) in enumerate([('01','VALIDATE DEMAND','#FFFDF5'),('02','PLAN THE NUMBERS','#C0F7FE'),('03','LAUNCH SMALL','#99E885')]):
    y=940+j*180
    shape('Card shadow '+a,94,y+10,902,140,'#000000')
    shape('Card '+a,84,y,902,140,color)
    text('Number '+a,a,115,y+90,42)
    text('Action '+a,b,225,y+90,41)
shape('Footer',84,1580,902,115,'#000000')
text('Footer text','SAVE YOUR STARTUP CHECKLIST',110,1654,34,'#FFFFFF',700)
argv=[PC,'run','--new',json.dumps({'width':1080,'height':1920,'background':'#F7CB46','resolution':72,'name':'Start a business — Reel cover'})]
for cmd,params in actions:argv+=['--cmd',cmd,'--params',json.dumps(params)]
argv+=['--out',str(out/'business-reel-cover.psd')]
r=subprocess.run(argv,capture_output=True,text=True)
(ROOT/'tools/cover-build.log').write_text(r.stdout+r.stderr,encoding='utf-8')
if r.returncode:raise RuntimeError(r.stderr+r.stdout)
for ext in ['jpg','png']:
    subprocess.run([PC,'convert',str(out/'business-reel-cover.psd'),str(out/f'business-reel-cover.{ext}')],check=True,capture_output=True)
print('Created layered PhotoCraft PSD, PNG and JPEG covers.')
