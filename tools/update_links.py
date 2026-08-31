#!/usr/bin/env python3
"""articles.json を正として、全記事の「関連ガイド」・LPのガイド一覧・sitemap.xml を再生成。
記事を追加したら articles.json に1行足して実行するだけ。冪等。"""
import json, re, os
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
data = json.load(open('tools/articles.json'))
urls = ['https://kiy00.com/']
for app, cfg in data.items():
    arts = cfg['articles']
    urls.append(f'https://kiy00.com/{app}/')
    for a in arts:
        urls.append(f'https://kiy00.com/{app}/guide/{a["slug"]}/')
        p = f'{app}/guide/{a["slug"]}/index.html'
        if not os.path.exists(p): print('SKIP(未作成):', p); continue
        s = open(p).read()
        others = '\n'.join(f'<li><a href="/{app}/guide/{o["slug"]}/">{o["title"]}</a></li>'
                           for o in arts if o['slug'] != a['slug'])
        cta = cfg.get('related_cta', 'アプリでなぞって書く(無料)')
        block = f'<h2>関連ガイド</h2>\n<ul>\n{others}\n<li><a href="/{app}/">{cta}</a></li>\n</ul>'
        if '<h2>関連ガイド</h2>' in s:
            s = re.sub(r'<h2>関連ガイド</h2>\s*<ul>.*?</ul>', block, s, flags=re.S)
        else:
            s = s.replace('<footer>', block + '\n\n<footer>')
        open(p, 'w').write(s)
    # LPのガイド一覧
    lp = f'{app}/index.html'
    if os.path.exists(lp):
        s = open(lp).read()
        lis = '\n'.join(f'<li><a href="/{app}/guide/{a["slug"]}/">{a["title"]}</a></li>' for a in arts)
        heading = cfg.get('guide_heading', '書き方ガイド')
        s = re.sub(r'(<h2>' + re.escape(heading) + r'</h2>\s*<ul>).*?(</ul>)', r'\1\n' + lis + r'\n\2', s, flags=re.S)
        open(lp, 'w').write(s)
open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + '\n'.join(f'<url><loc>{u}</loc></url>' for u in urls) + '\n</urlset>\n')
print(f'関連ガイド・LP一覧・sitemap({len(urls)}URL)を再生成')
