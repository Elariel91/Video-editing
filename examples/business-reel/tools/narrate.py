import sys, json, asyncio, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
import edge_tts

async def main():
    (ROOT/'assets').mkdir(exist_ok=True)
    scenes = json.loads((ROOT / 'scenes.json').read_text(encoding='utf-8'))
    print('Script words:', sum(len(s['text'].split()) for s in scenes), flush=True)
    for s in scenes:
        path = ROOT / 'assets' / (s['id'] + '.mp3')
        words = []
        tts = edge_tts.Communicate(s['text'], 'en-US-AriaNeural', rate='+15%', boundary='WordBoundary')
        with path.open('wb') as out:
            async for chunk in tts.stream():
                if chunk['type'] == 'audio':
                    out.write(chunk['data'])
                elif chunk['type'] == 'WordBoundary':
                    words.append({'text':chunk['text'], 'start':chunk['offset']/1e7, 'end':(chunk['offset']+chunk['duration'])/1e7})
        (ROOT / 'assets' / (s['id']+'.words.json')).write_text(json.dumps(words), encoding='utf-8')
        print(s['id'], 'words', len(words), 'end', words[-1]['end'] if words else 0, flush=True)

asyncio.run(main())
