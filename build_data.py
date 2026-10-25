import json,pathlib,shutil
root=pathlib.Path('/workspace/scratch/openjlpt'); out=pathlib.Path('dist/data');out.mkdir(parents=True,exist_ok=True)
for n in [5,4,3,2]:
 d={k:json.loads((root/f'data/json/{k}/n{n}.json').read_text()) for k in ['vocab','grammar']}
 (out/f'n{n}.json').write_text(json.dumps(d,ensure_ascii=False))
for f in ['LICENSE','NOTICE.md']: shutil.copy(root/f,out/f)
