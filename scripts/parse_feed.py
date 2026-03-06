import xml.etree.ElementTree as ET
import json, urllib.request, re

def strip(s):
    return re.sub('<[^>]+>', '', s or '').strip()

# Buzzsprout
req = urllib.request.Request('https://feeds.buzzsprout.com/2569924.rss', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as r:
    tree = ET.fromstring(r.read())
ns = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}
items = tree.findall('./channel/item')
episodes = []
for i, item in enumerate(items):
    dur = item.find('itunes:duration', ns)
    episodes.append({
        'num': len(items) - i,
        'title': item.findtext('title', '').strip(),
        'desc': strip(item.findtext('description', ''))[:120] + '…',
        'dur': dur.text if dur is not None else '',
        'date': item.findtext('pubDate', ''),
        'link': item.findtext('link', ''),
    })
with open('episodes.json', 'w') as f:
    json.dump(episodes, f)

# Substack
import urllib.request, xml.etree.ElementTree as ET

req = urllib.request.Request(
    'https://substack-proxy.austinburton.workers.dev/',
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*',
    }
)
with urllib.request.urlopen(req) as r:
    sub = ET.fromstring(r.read())

