"""Build the dependency-free GitHub Pages site from weekly Markdown guides."""
from pathlib import Path
import html
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'

def inline(text):
    text = html.escape(text)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

def markdown(text):
    """Render this repo's headings, paragraphs, lists, checklists and tables."""
    lines = text.strip().splitlines()
    out = []; i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1; continue
        if s.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c) for c in cells): rows.append(cells)
                i += 1
            out.append('<div class="table-scroll"><table><thead><tr>' + ''.join('<th>'+inline(c)+'</th>' for c in rows[0]) + '</tr></thead><tbody>')
            out.extend('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>' for row in rows[1:])
            out.append('</tbody></table></div>'); continue
        heading = re.match(r'^(#{1,6}) (.+)', s)
        if heading:
            n = len(heading[1]); out.append(f'<h{n}>'+inline(heading[2])+f'</h{n}>'); i += 1; continue
        item = re.match(r'^(- |\d+\. )(.+)', s)
        if item:
            ordered = item[1] != '- '; tag = 'ol' if ordered else 'ul'
            out.append(f'<{tag}>')
            while i < len(lines):
                item = re.match(r'^(- |\d+\. )(.+)', lines[i].strip())
                if not item or (item[1] != '- ') != ordered: break
                body = item[2]
                if body.startswith('[ ] '):
                    out.append('<li class="check-item"><label><input type="checkbox"><span>'+inline(body[4:])+'</span></label></li>')
                else: out.append('<li>'+inline(body)+'</li>')
                i += 1
            out.append(f'</{tag}>'); continue
        paragraph = [s]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#|\||- |\d+\. )', lines[i].strip()):
            paragraph.append(lines[i].strip()); i += 1
        out.append('<p>'+inline(' '.join(paragraph))+'</p>')
    return '\n'.join(out)

def build():
    OUT.mkdir(exist_ok=True)
    (OUT / '.nojekyll').touch()
    for name in ['style.css', 'app.js']:
        shutil.copyfile(ROOT/'site'/name, OUT/name)
    guides = sorted(ROOT.glob('week-of-*/README.md'), reverse=True)
    assert guides, 'No weekly guides found'
    template = (ROOT/'site/template.html').read_text()
    for path in guides:
        source = re.sub(r'^---\n.*?\n---\n', '', path.read_text(), count=1, flags=re.S)
        title = re.search(r'^# (.+)', source, re.M)[1]
        sections = re.split(r'^## (.+)\n', source, flags=re.M)
        entries = list(zip(sections[1::2], sections[2::2]))
        recipes = [(h,b) for h,b in entries if re.match(r'^(Monday|Tuesday|Wednesday|Thursday|Friday):', h)]
        assert len(recipes) == 5, f'{path}: expected five weekday recipes'
        cards = []; details = []
        for n,(heading,body) in enumerate(recipes,1):
            day, name = heading.split(': ',1)
            timing = re.search(r'^\*\*(.+?)\*\*', body.strip())[1]
            cards.append(f'<a class="meal meal-{n}" href="#recipe-{n}"><span class="day">{day}</span><span class="meal-number">0{n}</span><h3>{inline(name)}</h3><span class="card-time">{inline(timing.split("·")[-1].strip())}</span><span class="cook">Cook this <span aria-hidden="true">↗</span></span></a>')
            details.append(f'<details class="recipe" id="recipe-{n}"><summary><span class="recipe-day">{day[:3].upper()}</span><span><span class="recipe-name">{inline(name)}</span><span class="recipe-meta">{inline(timing)}</span></span><span class="plus" aria-hidden="true">+</span></summary><div class="recipe-body">{markdown(body)}</div></details>')
        shopping = next(b for h,b in entries if h == 'Shopping list')
        notes = ''.join('<details class="note"><summary>'+inline(h)+'</summary>'+markdown(b)+'</details>' for h,b in entries if (h,b) not in recipes and h != 'Shopping list')
        weeks = ''.join(f'<option value="{p.parent.name}.html"'+(' selected' if p == path else '')+'>'+html.escape(p.parent.name.replace('week-of-', 'Week of '))+'</option>' for p in guides)
        values = {'TITLE':inline(title),'WEEK':path.parent.name,'CARDS':''.join(cards),'RECIPES':''.join(details),'SHOPPING':markdown(shopping),'NOTES':notes,'WEEKS':weeks}
        result = template
        for key,value in values.items(): result=result.replace('{{'+key+'}}',value)
        assert not re.search(r'\{\{[A-Z]+\}\}', result)
        (OUT / (path.parent.name+'.html')).write_text(result)
        if path == guides[0]: (OUT/'index.html').write_text(result)
    print(f'Built {len(guides)} week(s) in docs/')

if __name__ == '__main__': build()
