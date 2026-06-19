"""Extract personal, revealing quotes from speaking records. v2.
Criteria: emotional texture, personal moments, scene-rich language.
Avoids: procedural, technical, formal motions, greetings."""
import json, re
from pathlib import Path

PAST = Path("/home/notthere/ai-assisted-learning/potential/nantang-fair/past-docs")
OUTPUT = Path("/home/notthere/ai-assisted-learning/potential/nantang-fair/website/quotes.js")

def score_quote(text):
    """Score how personally revealing / interesting a quote is. Higher = better."""
    score = 0
    length = len(text)

    # LENGTH: prefer 30-100 chars
    if 30 <= length <= 100:
        score += 8
    elif 15 <= length <= 150:
        score += 4
    elif length < 10:
        score -= 20
    elif length > 250:
        score -= 5

    # PERSONAL / EMOTIONAL TEXTURE
    emotional = ['孤独', '开心', '难过', '担心', '害怕', '兴奋', '惨', '饿', '冷',
                 '累', '烦', '想家', '感动', '哭了', '笑了', '我一个人', '陪伴',
                 '感谢', '不容易', '迷茫', '犹豫', '困惑', '终于', '竟然', '居然']
    for w in emotional:
        if w in text:
            score += 3

    # SELF-REVELATION: "I" statements that go beyond opinion
    self_reveal = ['我觉得我', '我发现', '我意识到', '说实话', '其实我', '我也不知道',
                   '我不确定', '我有点', '我经常', '我好像', '我应该', '我可能']
    for w in self_reveal:
        if w in text:
            score += 4

    # VIVID / UNEXPECTED
    vivid = ['没有一个人', '怎么办', '遥遥无期', '灯都没开', '挨饿', '太惨',
             '不知道', '想不通', '很奇怪', '有意思', '好玩', '搞笑',
             '突然', '第一次', '从来没', '居然', '竟然']
    for w in vivid:
        if w in text:
            score += 3

    # SPECIFIC SCENE: mentions a place, time, or specific person
    scene_words = ['合作社', '南塘', '办公室', '厨房', '宿舍', '大院',
                   '昨天', '今天', '明天', '上午', '下午', '晚上',
                   '上次', '这次', '之前']
    for w in scene_words:
        if w in text:
            score += 1

    # NEGATIVE: procedural / hosting
    procedural = ['点击', '测试', '确认', '听到吗', '能听到', '听得到',
                  '发言整理', 'OK', '主持人', '表情包', '萝卜丁', 'imeeting']
    for w in procedural:
        if w.lower() in text.lower():
            score -= 4

    # NEGATIVE: formal meeting jargon
    formal = ['提案', '表决', '动议', '附议', '议程', '投票',
              '赞成', '反对', '默认一致', '修正案']
    for w in formal:
        if w in text:
            score -= 3

    # NEGATIVE: pure greeting / functional
    if length < 25 and any(g in text for g in ['大家好', '晚上好', '哈喽', 'hello', '能听到']):
        score -= 20
    if text.strip() in ['嗯', '好', '可以', 'OK', '好的', '谢谢']:
        score -= 30

    return score

def extract_session_num(filename):
    """Extract session number from filename."""
    for part in filename.split('-'):
        if '赶集会' in part:
            num = re.sub(r'赶集会', '', part)
            num = num.strip('0123456789-')
            # Try to get number
            m = re.search(r'(\d+)', part)
            if m:
                return f"第{m.group(1)}期"
    # Fallback: try to find number
    m = re.search(r'赶集会(\d)', filename)
    if m:
        return f"第{m.group(1)}期"
    return "赶集会"

def main():
    # Get people list from data.js
    with open(Path("/home/notthere/ai-assisted-learning/potential/nantang-fair/website/data.js")) as f:
        text = f.read()
    match = re.search(r'"people":\s*(\[.+?\])', text, re.DOTALL)
    people_data = json.loads(match.group(1)) if match else []
    people_names = {p['name'] for p in people_data}

    all_quotes = {}  # name -> list of (quote, score, session)

    for sf in sorted(PAST.glob("*发言记录*")):
        fname = sf.name
        # Skip pre-赶集会 files
        if '村里那些事' in fname or '建立与执行' in fname:
            continue

        session_label = extract_session_num(fname)
        content = sf.read_text(encoding='utf-8')
        lines = content.split('\n')

        for i, line in enumerate(lines):
            # Match speaker header: "5. **名字** [time]（type）"
            m = re.match(r'\d+\.\s+\*\*(.+?)\*\*\s*\[(.+?)\]\s*[（(](.+?)[）)]', line)
            if not m:
                continue

            name = m.group(1).strip()
            if name in ['系统', '智能主持人', '智能秘书']:
                continue

            # Get the actual quote (next line)
            quote = ''
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not next_line.startswith('**') and not next_line.startswith('#'):
                    quote = next_line

            # Skip "发言整理" blocks
            if '发言整理' in quote:
                continue

            if quote and len(quote) >= 15:
                s = score_quote(quote)
                if name not in all_quotes:
                    all_quotes[name] = []
                all_quotes[name].append((quote, s, session_label))

    # For each person, pick the single best quote
    results = {}
    for name in people_names:
        if name in all_quotes and all_quotes[name]:
            all_quotes[name].sort(key=lambda x: x[1], reverse=True)
            best_quote, best_score, session = all_quotes[name][0]
            # Trim long quotes to ~100 chars at a natural break
            display = best_quote
            if len(display) > 100:
                # Try to break at punctuation
                for punct in ['。', '？', '！', '…', '，']:
                    idx = display[:100].rfind(punct)
                    if idx > 60:
                        display = display[:idx+1]
                        break
                else:
                    display = display[:100] + '…'
            results[name] = {
                'quote': display,
                'session': session,
                'score': best_score,
                'total_quotes': len(all_quotes[name])
            }
            print(f"  [{session}] {name} (score={best_score}): {display[:80]}...")
        else:
            results[name] = {'quote': '', 'session': '', 'score': 0, 'total_quotes': 0}

    # Write output
    js = "const quoteData = " + json.dumps(results, ensure_ascii=False, indent=2) + ";"
    OUTPUT.write_text(js, encoding='utf-8')
    found = sum(1 for v in results.values() if v['quote'])
    print(f"\nDone: {found}/{len(results)} people have quotes. Output: {OUTPUT}")

if __name__ == '__main__':
    main()
