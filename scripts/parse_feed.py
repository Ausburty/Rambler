import xml.etree.ElementTree as ET
import json, urllib.request, re, os

def strip(s):
    return re.sub('<[^>]+>', '', s or '').replace('Send a text', '').replace('Check out the brand new substack!', '').strip()

def fmtDur(val):
    if not val: return ''
    try:
        s = int(val)
        return f"{s//60}:{str(s%60).zfill(2)}"
    except:
        return val

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as r:
        return r.read()

# Buzzsprout
tree = ET.fromstring(fetch('https://feeds.buzzsprout.com/2569924.rss'))
ns = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}
items = tree.findall('./channel/item')
episodes = []

for i, item in enumerate(items):
    dur = item.find('itunes:duration', ns)
    enclosure = item.find('enclosure')
    guid = item.findtext('guid') or ''
    ep_id = guid.replace('Buzzsprout-', '')
    mp3 = enclosure.get('url') if enclosure is not None else ''

    episodes.append({
        'num': len(items) - i,
        'id': ep_id,
        'title': item.findtext('title', '').strip(),
        'desc': strip(item.findtext('description', ''))[:120] + '…',
        'dur': fmtDur(dur.text if dur is not None else ''),
        'date': item.findtext('pubDate', ''),
        'mp3': mp3,
    })

with open('episodes.json', 'w') as f:
    json.dump(episodes, f)

# Transcripts
os.makedirs('transcripts', exist_ok=True)
for ep in episodes:
    path = f"transcripts/{ep['id']}.html"
    if os.path.exists(path):
        continue  # skip if already fetched
    try:
        html = fetch(f"https://www.buzzsprout.com/2569924/{ep['id']}/transcript").decode('utf-8')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Fetched transcript {ep['id']}")
    except Exception as e:
        print(f"Failed transcript {ep['id']}: {e}")

# Substack
sub = ET.fromstring(fetch('https://substack-proxy.austinburton.workers.dev/'))
posts = []
for item in sub.findall('./channel/item')[:5]:
    posts.append({
        'title': item.findtext('title', '').strip(),
        'desc': strip(item.findtext('description', ''))[:100] + '…',
        'date': item.findtext('pubDate', ''),
        'link': item.findtext('link', ''),
    })

with open('posts.json', 'w') as f:
    json.dump(posts, f)

with open('posts.json', 'w') as f:
    json.dump(posts, f)
