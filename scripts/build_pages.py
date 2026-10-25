from pathlib import Path
p=Path(__file__).resolve().parents[1]/'dist';template=(p/'index.html').read_text()
for name,title in [('lessons','Choose a level'),('n5','N5 Japanese lessons'),('n4','N4 Japanese lessons'),('n3','N3 Japanese lessons'),('n2','N2 Japanese lessons'),('n1','N1 Japanese lessons'),('review','Practice Japanese'),('progress','Learning progress')]:
 html=template.replace('<title>Nihongo Path · N5–N1 Japanese</title>',f'<title>{title} · Nihongo Path</title>')
 (p/(name+'.html')).write_text(html)
