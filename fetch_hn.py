import requests
import re

SOURCES = {
    'HN': 'https://news.ycombinator.com/news',
    'Reddit-ML': 'https://www.reddit.com/r/MachineLearning/.rss',
}

def fetch_hn():
    r = requests.get(SOURCES['HN'], timeout=10)
    items = re.findall(r'<tr class="athing submission" id="\d+">.*?<td class="title"><span class="titleline"><a href="([^"]+)">([^<]+)</a>.*?<span class="score" id="score_\d+">(\d+) points', r.text, re.DOTALL)
    return [{'title': t, 'url': u, 'score': s, 'source': 'HN'} for u, t, s in items[:15]]

def fetch_reddit_ml():
    try:
        r = requests.get(SOURCES['Reddit-ML'], headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        # Simple RSS parse
        titles = re.findall(r'<title><!\[CDATA\[([^\]]+)\]\]></title>', r.text)
        links = re.findall(r'<link><!\[CDATA\[([^\]]+)\]\]></link>', r.text)
        scores = re.findall(r'<reddit:score>(\d+)</reddit:score>', r.text)
        results = []
        for i in range(min(len(titles), len(links), 12)):
            if 'r/MachineLearning' in titles[i]:
                continue
            results.append({
                'title': titles[i],
                'url': links[i] if links[i].startswith('http') else '',
                'score': scores[i] if i < len(scores) else '0',
                'source': 'r/MachineLearning'
            })
        return results
    except Exception as e:
        return [{'title': f'Error: {e}', 'url': '', 'score': '0', 'source': 'Reddit-ML'}]

print("=== 今日 AI 热门话题 ===\n")
print("## Hacker News\n")
hn = fetch_hn()
for rank, item in enumerate(hn, 1):
    print(f"{rank}. [{item['score']} pts] {item['title']}")
    if item['url']:
        print(f"   {item['url']}")

print("\n## Reddit r/MachineLearning\n")
reddit = fetch_reddit_ml()
for rank, item in enumerate(reddit[:10], 1):
    print(f"{rank}. [{item['score']} score] {item['title']}")
    if item['url']:
        print(f"   {item['url']}")