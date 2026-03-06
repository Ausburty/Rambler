import xml.etree.ElementTree as ET
import json, urllib.request, re

def strip(s):
    return re.sub('<[^>]+>', '', s or '').replace('Send a text', '').strip()

def fmtDur(val):
    if not val: return ''
    try:
        s = int(val)
        return f"{s//60}:{str(s%60).zfill(2)}"
    except:
        return val

# Buzzsprout
req = urllib.request.Request('https://feeds.buzzsprout.com/2569924.rss', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as r:
    tree = ET.fromstring(r.read())

ns = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd', 'podcast': 'https://podcastindex.org/namespace/1.0'}
items = tree.findall('./channel/item')
episodes = []

for i, item in enumerate(items):
    dur = item.find('itunes:duration', ns)
    enclosure = item.find('enclosure')
    guid = item.findtext('guid') or ''
    ep_id = guid.replace('Buzzsprout-', '')
    mp3 = enclosure.get('url') if enclosure is not None else ''
    transcript = f"https://www.buzzsprout.com/2569924/{ep_id}/transcript"

    episodes.append({
        'num': len(items) - i,
        'id': ep_id,
        'title': item.findtext('title', '').strip(),
        'desc': strip(item.findtext('description', ''))[:120] + '…',
        'dur': fmtDur(dur.text if dur is not None else ''),
        'date': item.findtext('pubDate', ''),
        'mp3': mp3,
        'transcript': transcript,
    })

with open('episodes.json', 'w') as f:
    json.dump(episodes, f)

# Substack
req = urllib.request.Request('https://substack-proxy.austinburton.workers.dev/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as r:
    sub = ET.fromstring(r.read())

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
