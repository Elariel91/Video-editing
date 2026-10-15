import pathlib,json,html,shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'timing.json').read_text(encoding='utf-8')); scenes=data['scenes']; D=data['duration']
frames=ROOT/'compositions/frames';frames.mkdir(exist_ok=True,parents=True)
E=html.escape
CSS='''
@font-face{font-family:Inter;src:url(assets/Inter.ttf);font-weight:100 900}
@font-face{font-family:"Space Grotesk";src:url(assets/SpaceGrotesk.ttf);font-weight:300 700}
*{box-sizing:border-box}body{margin:0;background:#000;color:#000;font-family:Inter,sans-serif}#root{width:100%;height:100%;position:relative;overflow:hidden}
.clip{position:absolute;inset:0}.scene{position:absolute;inset:0;overflow:hidden}.ground{position:absolute;inset:0;background:var(--paper)}
.scene-body{position:absolute;inset:0}.brand{position:absolute;left:84px;top:130px;font-family:"Space Grotesk";font-size:25px;font-weight:700;letter-spacing:4px}
.brand-rule{position:absolute;left:84px;right:84px;top:182px;height:4px;background:currentColor}.label{position:absolute;left:84px;top:225px;border:3px solid currentColor;border-radius:40px;padding:14px 25px;font-family:"Space Grotesk";font-size:28px;font-weight:700;background:var(--tag,#fff)}
.heading{position:absolute;top:340px;left:84px;width:910px;margin:0;font-size:94px;line-height:1.02;letter-spacing:-5px;font-weight:900;text-transform:uppercase}.heading span{display:block;width:100%}.takeaway{position:absolute;left:84px;top:609px;font-size:37px;font-weight:800;letter-spacing:-1px;border-bottom:5px solid currentColor;padding-bottom:14px}
.card{position:absolute;background:#FFFDF5;border:4px solid #000;box-shadow:9px 9px 0 #000;color:#000}.card-title{font-size:36px;font-weight:800;letter-spacing:-1px}.caption{position:absolute;left:84px;right:110px;top:1490px;display:flex;justify-content:center;z-index:30}.caption-line{display:inline-block;background:#000;color:#fff;padding:15px 25px;font-size:42px;line-height:1.36;font-weight:800;text-align:center;border:3px solid #000;max-width:870px}.caption-word{display:inline-block;padding:0 4px}.progress{position:absolute;left:84px;right:110px;top:1720px;display:flex;gap:12px}.stepdot{height:12px;flex:1;background:currentColor;opacity:.22}.stepdot.done{opacity:1}.page{position:absolute;right:110px;top:225px;font-family:"Space Grotesk";font-size:29px;font-weight:700;padding:14px 0}
.stack{position:absolute;left:84px;top:800px;width:860px}.stackrow{position:relative;padding:27px 30px;margin-bottom:22px;display:flex;align-items:center;gap:25px;font-size:34px;font-weight:800;background:#fff;border:4px solid #000;box-shadow:8px 8px 0 #000}.num{display:grid;place-items:center;width:60px;height:60px;flex-shrink:0;background:#F7CB46;border:3px solid #000;font-size:30px}
.footage{position:absolute;left:84px;top:790px;width:860px;height:486px;border:4px solid #000;box-shadow:10px 10px 0 #000;overflow:hidden;background:#000}.footage video{width:100%;height:100%;object-fit:cover;position:absolute;inset:0}.footage-label{position:absolute;left:20px;top:20px;background:#F7CB46;border:3px solid #000;padding:12px 18px;color:#000;font-family:"Space Grotesk";font-size:25px;font-weight:700}
.chips{position:absolute;left:84px;top:1313px;display:flex;gap:14px;width:860px}.chip{padding:15px 18px;background:#fff;border:3px solid #000;font-size:24px;font-weight:800;color:#000;flex:1;text-align:center}
.person{position:absolute;left:84px;top:820px;width:340px;height:440px;background:#FE90E8;display:grid;place-items:center}.person svg{width:240px;height:280px}.problem-copy{position:absolute;left:480px;top:820px;width:464px}.q{margin:0 0 30px;padding:20px 0;border-bottom:3px solid #000;font-size:37px;font-weight:800;line-height:1.2}.q small{display:block;font-family:"Space Grotesk";font-size:24px;margin-bottom:8px;font-weight:600}
.offer{left:84px;top:800px;width:860px;padding:35px}.offer-head{font-size:28px;font-family:"Space Grotesk";font-weight:700;letter-spacing:3px;border-bottom:4px solid #000;padding-bottom:20px;margin-bottom:5px}.offer-row{display:flex;justify-content:space-between;border-bottom:2px solid #000;padding:24px 0;gap:30px;font-size:31px}.offer-row b{font-weight:800}.offer-row span{text-align:right;font-weight:500}
.cash{left:84px;top:810px;width:860px;padding:30px;background:#FFFDF5}.cashrow{display:flex;justify-content:space-between;align-items:center;font-size:34px;font-weight:800;padding:29px 0;border-bottom:3px solid #000}.cashrow:last-child{border-bottom:0}.cashrow i{display:block;width:155px;height:26px;background:#99E885;border:3px solid #000;transform-origin:left center}.cashrow:nth-child(2) i{background:#FE90E8;width:115px}.cashrow:nth-child(3) i{background:#F7CB46;width:190px}.cash-note{position:absolute;left:84px;top:1280px;font-size:27px;font-family:"Space Grotesk";font-weight:700;width:860px}
.hook .heading{font-size:108px;top:350px}.hook .takeaway{top:630px;font-size:52px}.hook-stack{position:absolute;left:84px;top:855px;width:860px}.hook-step{position:relative;display:flex;align-items:center;gap:25px;padding:25px 30px;border:4px solid #000;background:#FFFDF5;box-shadow:8px 8px 0 #000;margin:0 0 24px;font-size:40px;font-weight:900}.hook-step:nth-child(2){background:#C0F7FE}.hook-step:nth-child(3){background:#99E885}.arrow{margin-left:auto;font-size:44px}
.cta{color:#fff}.cta .ground{background:#000}.cta .label{background:#000}.cta .heading{font-size:110px}.cta .takeaway{font-size:38px;top:630px;border:0;color:#F7CB46}.end-card{position:absolute;left:84px;top:850px;width:860px;background:#F7CB46;color:#000;border:4px solid #fff;box-shadow:10px 10px 0 #fff;padding:45px}.play{width:86px;height:86px;border:4px solid #000;border-radius:50%;display:grid;place-items:center;font-size:38px;margin-bottom:28px}.end-card h2{font-size:54px;line-height:1.05;letter-spacing:-2px;margin:0 0 20px;font-weight:900}.end-card p{font-size:29px;font-family:"Space Grotesk";font-weight:700;margin:0}.save{position:absolute;left:84px;top:1300px;font-size:29px;letter-spacing:2px;font-family:"Space Grotesk";font-weight:700}.cta .caption-line{background:#FFFDF5;color:#000}.cta .caption-word{color:#000}
'''
grounds=['#F7CB46','#FFFDF5','#C0F7FE','#FFFDF5','#FE90E8','#FFFDF5','#99E885','#000000']
CSS+='\n.caption{bottom:auto;height:auto;align-items:flex-start}.caption-line{flex:0 1 auto}.hook .takeaway{top:660px}.heading{font-size:88px}.hook .heading{font-size:98px}\n'
def footage(sid,file,label,duration):
    return f'<div class="footage"><video id="{sid}-video" src="assets/{file}-edit.mp4" muted playsinline data-start="0" data-duration="{duration:.3f}" data-media-start="0" data-playback-rate="{4.95/duration:.6f}" data-track-index="1"></video><div class="footage-label">{label}</div></div>'
hosts=[]
for ix,s in enumerate(scenes):
    sid='s'+s['id']; dur=s['duration']; typ=s['visual']; js=[]
    old=frames/f"{s['id']}.html"
    if old.exists(): old.unlink()
    title=''.join(f'<span id="{sid}-line-{j}">{E(line)}</span>' for j,line in enumerate(s['title']))
    content=f'<div class="brand">THE BUSINESS STARTER</div><div class="brand-rule"></div><div class="label">{E(s["label"])}</div><div class="page">{ix+1:02d} / 08</div><h1 class="heading">{title}</h1><div class="takeaway">{E(s["accent"])}</div>'
    if typ=='hook':
        content+='<div class="hook-stack">'+''.join(f'<div class="hook-step" id="{sid}-item-{j}"><span class="num">{j+1:02d}</span>{v}<span class="arrow">→</span></div>' for j,v in enumerate(s['chips']))+'</div>'
    elif typ=='problem':
        content+='<div class="person card"><svg viewBox="0 0 240 280" aria-hidden="true"><circle cx="120" cy="70" r="48" fill="#F7CB46" stroke="#000" stroke-width="7"/><path d="M30 255v-34a90 90 0 0 1 180 0v34z" fill="#FFFDF5" stroke="#000" stroke-width="7"/></svg></div><div class="problem-copy">'+''.join(f'<div class="q" id="{sid}-item-{j}"><small>QUESTION {j+1:02d}</small>{v}</div>' for j,v in enumerate(['Who needs help?','What is the pain?','What is the result?']))+'</div>'
    elif typ in ['demand','setup','launch']:
        file,label={'demand':('stock-4809','REAL CONVERSATIONS'),'setup':('stock-241','BEFORE YOU LAUNCH'),'launch':('boardroom-1785','START WITH ONE CUSTOMER')}[typ]
        content+=footage(sid,file,label,dur)
        content+='<div class="chips">'+''.join(f'<div class="chip" id="{sid}-item-{j}">{v}</div>' for j,v in enumerate(s['chips']))+'</div>'
    elif typ=='offer':
        content+='<div class="offer card"><div class="offer-head">YOUR ONE-PAGE OFFER</div>'+''.join(f'<div class="offer-row" id="{sid}-item-{j}"><b>{a}</b><span>{b}</span></div>' for j,(a,b) in enumerate([('WHAT','One clear deliverable'),('HOW MUCH','A clear price'),('WHY YOU','A reason to choose you')]))+'</div>'
    elif typ=='numbers':
        content+='<div class="cash card">'+''.join(f'<div class="cashrow" id="{sid}-item-{j}"><span>{v}</span><i></i></div>' for j,v in enumerate(s['chips']))+'</div><div class="cash-note">INCLUDE A PLAN TO FUND THE GAP.</div>'
    elif typ=='cta':
        content+='<div class="end-card"><div class="play">▶</div><h2>THE FULL<br/>STEP-BY-STEP<br/>DEEP DIVE</h2><p>AVAILABLE ON MY CHANNEL →</p></div><div class="save">SAVE THIS CHECKLIST.</div>'
    content+='<div class="progress">'+''.join(f'<div class="stepdot {"done" if j<ix else ""}"></div>' for j in range(6))+'</div>'
    # Adapted registry headline-slam entrance: weighty scale landing, then still reading.
    js.append(f'tl.fromTo("#{sid}-line-0",{{scale:1.32,opacity:0}},{{scale:1,opacity:1,duration:.48,ease:"expo.out"}},.08);')
    js.append(f'tl.fromTo("#{sid}-line-1",{{x:-75,opacity:0}},{{x:0,opacity:1,duration:.48,ease:"power3.out"}},.27);')
    js.append(f'tl.fromTo("#{sid}-takeaway",{{y:20,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"power3.out"}},{min(dur*.6,3.5):.3f});')
    # Assign IDs to target inner nodes so framework clip visibility remains authoritative.
    content=content.replace('class="takeaway"',f'id="{sid}-takeaway" class="takeaway"')
    for j in range(3):
        cue=[1.05,max(1.65,dur*.38),max(2.6,dur*.64)][j]
        js.append(f'if(document.getElementById("{sid}-item-{j}"))tl.fromTo("#{sid}-item-{j}",{{y:28,opacity:0}},{{y:0,opacity:1,duration:.38,ease:"power3.out"}},{cue:.3f});')
    if typ=='numbers': js.append(f'tl.fromTo("#{sid} .cashrow i",{{scaleX:0}},{{scaleX:1,duration:.6,stagger:.15,ease:"power3.out"}},1.2);')
    if typ=='cta':
        content=content.replace('class="end-card"',f'id="{sid}-end" class="end-card"')
        js.append(f'tl.fromTo("#{sid}-end",{{scale:.92,y:25,opacity:0}},{{scale:1,y:0,opacity:1,duration:.6,ease:"back.out(1.15)"}},1.15);')
    scene=f'<template><div id="{sid}" data-composition-id="{sid}" data-duration="{dur:.6f}" style="width:100%;height:100%;position:absolute;inset:0;--paper:{grounds[ix]}" class="scene {typ}"><div id="{sid}-ground" class="clip ground" data-start="0" data-duration="{dur:.6f}" data-track-index="0"></div><div class="scene-body">{content}</div></div><script>(()=>{{const tl=gsap.timeline({{paused:true}});{"".join(js)}window.__timelines["{sid}"]=tl;}})();</script></template>'
    (frames/f'{sid}.html').write_text(scene,encoding='utf-8')
    hosts.append(f'<div class="clip" id="host-{sid}" data-composition-id="{sid}" data-composition-src="compositions/frames/{sid}.html" data-start="{s["start"]:.6f}" data-duration="{dur:.6f}" data-width="1080" data-height="1920" data-track-index="0"></div>')
# Word-timed caption groups, burned in and also exported as SRT.
caps=[]; ct=[];srt=[];count=1
def stamp(t):
    ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
for si,s in enumerate(scenes):
    ws=s['words']
    for j in range(0,len(ws),4):
        group=ws[j:j+4]; start=s['start']+group[0]['start'];end=s['start']+(ws[j+4]['start'] if j+4<len(ws) else min(s['duration']-.1,group[-1]['end']+.22))
        cid=f'cap-{si}-{j}'; spans=''.join(f'<span class="caption-word" id="{cid}-w{k}">{E(w["text"])}</span>' for k,w in enumerate(group))
        caps.append(f'<div class="clip caption" id="{cid}" data-start="{start:.6f}" data-duration="{end-start:.6f}" data-track-index="5"><span class="caption-line">{spans}</span></div>')
        for k,w in enumerate(group):
            a=s['start']+w['start'];b=s['start']+w['end']
            ct.append(f'tl.set("#{cid}-w{k}",{{color:"#F7CB46"}},{a:.6f});tl.set("#{cid}-w{k}",{{color:"#FFFFFF"}},{b:.6f});')
        srt.append(f'{count}\n{stamp(start)} --> {stamp(end)}\n'+ ' '.join(w['text'] for w in group)+'\n');count+=1
audio=f'<audio id="voice" src="assets/narration.wav" data-start="0" data-duration="{D}" data-track-index="6" data-volume="1"></audio>'
master=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><title>Start a business — six steps</title><script src="assets/gsap.min.js"></script><style>{CSS}</style></head><body><div id="root" data-composition-id="business-reel" data-width="1080" data-height="1920" data-duration="{D}" data-fps="30">'+''.join(hosts)+''.join(caps)+audio+'</div><script>const tl=gsap.timeline({paused:true});'+''.join(ct)+'window.__timelines["business-reel"]=tl;</script></body></html>'
(ROOT/'index.html').write_text(master,encoding='utf-8')
(ROOT/'captions.srt').write_text('\n'.join(srt),encoding='utf-8')
board=(ROOT/'STORYBOARD.md').read_text(encoding='utf-8').replace('- status: outline','- status: animated')
for s in scenes: board=board.replace('compositions/frames/'+s['id']+'.html','compositions/frames/s'+s['id']+'.html')
(ROOT/'STORYBOARD.md').write_text(board,encoding='utf-8')
print('Built eight scenes and',count-1,'caption groups. Duration:',D)
