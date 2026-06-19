"""Extract 2 representative quotes per session from speaking records."""
import json, re
from pathlib import Path

PAST = Path("/home/notthere/ai-assisted-learning/potential/nantang-fair/past-docs")
OUTPUT = Path("/home/notthere/ai-assisted-learning/potential/nantang-fair/website/session_quotes.js")

def score(text):
    """Same heuristics as extract_quotes.py v2."""
    s = 0
    L = len(text)
    if 30 <= L <= 100: s += 8
    elif 15 <= L <= 150: s += 4
    elif L < 10: s -= 20
    elif L > 250: s -= 5
    for w in ['孤独','开心','难过','担心','惨','饿','冷','累','烦','感动','陪伴','感谢','不容易','迷茫']:
        if w in text: s += 3
    for w in ['我觉得我','我发现','我意识到','说实话','其实我','我也不知道','我不确定','我有点']:
        if w in text: s += 4
    for w in ['没有一个人','怎么办','遥遥无期','灯都没开','挨饿','太惨']:
        if w in text: s += 3
    for w in ['点击','测试','确认','听到吗','萝卜丁','imeeting','iMeeting']:
        if w.lower() in text.lower(): s -= 4
    for w in ['提案','表决','动议','附议','议程','投票']:
        if w in text: s -= 3
    if L < 25 and any(g in text for g in ['大家好','晚上好','哈喽','能听到']): s -= 20
    if text.strip() in ['嗯','好','可以','OK']: s -= 30
    return s

def session_label(fname):
    for part in fname.replace('.md','').split('-'):
        m = re.search(r'赶集会(\d)', part)
        if m: return f"第{m.group(1)}期"
    return None

def main():
    session_quotes = {}

    for sf in sorted(PAST.glob("*发言记录*")):
        fname = sf.name
        if '村里那些事' in fname or '建立与执行' in fname:
            continue
        label = session_label(fname)
        if not label:
            continue

        content = sf.read_text(encoding='utf-8')
        lines = content.split('\n')
        candidates = []

        for i, line in enumerate(lines):
            m = re.match(r'\d+\.\s+\*\*(.+?)\*\*\s*\[(.+?)\]\s*[（(](.+?)[）)]', line)
            if not m: continue
            name = m.group(1).strip()
            if name in ['系统', '智能主持人', '智能秘书']: continue
            quote = ''
            if i+1 < len(lines):
                q = lines[i+1].strip()
                if q and not q.startswith('**') and not q.startswith('#') and '发言整理' not in q:
                    quote = q[:120]
            if quote and len(quote) >= 15:
                s = score(quote)
                candidates.append((name, quote, s))

        # Pick top 2
        candidates.sort(key=lambda x: x[2], reverse=True)
        best = candidates[:2]
        session_quotes[label] = [{'name': n, 'quote': q, 'score': s} for n, q, s in best]
        print(f"{label}: {len(candidates)} candidates → {len(best)} selected")
        for n, q, s in best:
            print(f"  [{n}] (score={s}) {q[:80]}...")

    js = "const sessionQuoteData = " + json.dumps(session_quotes, ensure_ascii=False, indent=2) + ";"
    OUTPUT.write_text(js, encoding='utf-8')
    print(f"\nDone: {OUTPUT}")

if __name__ == '__main__':
    main()
