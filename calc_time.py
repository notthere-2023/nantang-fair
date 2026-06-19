"""Calculate per-topic and per-motion time from speaking records. v2."""
import re
from pathlib import Path

PAST = Path("/home/notthere/ai-assisted-learning/potential/nantang-fair/past-docs")

def parse_time(t_str):
    """Parse time like '下午7:59:35' to seconds since midnight."""
    t_str = t_str.replace('下午','').replace('上午','').replace('中午','').replace('晚上','').strip()
    parts = t_str.split(':')
    h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
    # PM times
    if h < 12:
        h += 12
    return h*3600 + m*60 + s

def main():
    results = {}

    for sf in sorted(PAST.glob("*发言记录*")):
        fname = sf.name
        if '村里那些事' in fname or '建立与执行' in fname:
            continue

        # Session label
        session = None
        for part in fname.replace('.md','').split('-'):
            m = re.search(r'赶集会(\d)', part)
            if m:
                session = f"第{m.group(1)}期"
                break
        if not session:
            continue

        content = sf.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Collect all timed entries
        entries = []
        for i, line in enumerate(lines):
            m = re.match(r'\d+\.\s+\*\*(.+?)\*\*\s*\[(.+?)\]\s*[（(](.+?)[）)]', line)
            if not m:
                continue
            name = m.group(1)
            time_range = m.group(2)
            speech_type = m.group(3)

            # Parse start time
            parts = time_range.split('-')
            start_str = parts[0].strip() if len(parts) >= 1 else ''
            end_str = parts[1].strip() if len(parts) >= 2 else ''

            try:
                start_sec = parse_time(start_str)
                end_sec = parse_time(end_str) if end_str else start_sec
            except:
                continue

            duration = end_sec - start_sec
            if duration <= 0 or duration > 3600:
                continue

            # Get quote
            quote = ''
            if i+1 < len(lines):
                q = lines[i+1].strip()
                if q and not q.startswith('**') and not q.startswith('#') and '发言整理' not in q:
                    quote = q[:100]

            entries.append({
                'name': name,
                'type': speech_type,
                'start': start_sec,
                'duration': duration,
                'quote': quote
            })

        if not entries:
            continue

        # Classify entries
        free_disc = [e for e in entries if e['type'] in ['自由发言', '提问']]
        motion_rel = [e for e in entries if e['type'] in ['设定议程', '主持中立发言', '润色']]
        hosting = [e for e in entries if '主持' in e['type']]
        other = [e for e in entries if e['type'] not in ['自由发言','提问','设定议程','主持中立发言','润色'] and '主持' not in e['type']]

        total_sec = sum(e['duration'] for e in entries)
        free_sec = sum(e['duration'] for e in free_disc)
        motion_sec = sum(e['duration'] for e in motion_rel)

        if session not in results:
            results[session] = {}
        # Merge if duplicate
        if results[session]:
            total_sec += results[session].get('total',0)
            free_sec += results[session].get('discussion',0)
            motion_sec += results[session].get('motion',0)

        results[session] = {
            'total': total_sec,
            'discussion': free_sec,
            'motion': motion_sec,
            'entries': len(entries)
        }

    print("Session | 总时长 | 自由发言 | 动议相关 | 自由占比")
    print("-" * 55)
    for label in sorted(results.keys()):
        r = results[label]
        if r['total'] > 0:
            d_pct = r['discussion'] / r['total'] * 100
            m_pct = r['motion'] / r['total'] * 100
            print(f"{label:8s} | {r['total']//60:3d}min | {r['discussion']//60:3d}min | {r['motion']//60:3d}min | {d_pct:.0f}%自由 {m_pct:.0f}%动议")

if __name__ == '__main__':
    main()
