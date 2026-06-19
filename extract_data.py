"""Extract structured data from 赶集会 meeting minutes. v2 - cleaner."""
import json, re, os
from pathlib import Path

PAST_DOCS = Path("/home/notthere/ai-assisted-learning/potential/nantang-fair/past-docs")
OUTPUT = Path("/home/notthere/ai-assisted-learning/potential/nantang-fair/website/data.js")

# Only process these 9 actual 赶集会 sessions (by date pattern in filename)
# Exclude 村里那些事 (pre-series) and the establishment meeting (20260317)
GATHER_SESSIONS = {
    '赶集会': '20260322_111810',      # Session 1
    '赶集会1-2': '20260322_163400',    # Session 1 cont.
    '赶集会2': '20260330_165614',      # Session 2
    '赶集会3': '20260410_114312',      # Session 3
    '赶集会4': '20260420_113502',      # Session 4
    '赶集会5': '20260430_234736',      # Session 5
    '赶集会6': '20260511_001011',      # Session 6
    '赶集会7': '20260520_232746',      # Session 7
    '赶集会8': '20260530_220028',      # Session 8
    '赶集会9': '20260610_232933',      # Session 9
}

def clean_text(s):
    """Remove markdown formatting and truncate."""
    s = re.sub(r'\*\*', '', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
    s = re.sub(r'[#>*_`]', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()[:300]

def parse_attendees(text):
    """Extract attendee names and status."""
    attendees = {}
    in_table = False
    for line in text.split('\n'):
        if '| 姓名 |' in line or '| :---:' in line:
            in_table = True
            continue
        if in_table:
            if not line.startswith('|'):
                break
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 3 and parts[0] not in ['姓名', '表决权']:
                name = parts[0]
                status = parts[2]
                attendees[name] = status
    return attendees

def parse_motions(text):
    """Extract motions: proposer, content summary, result."""
    motions = []
    lines = text.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Detect motion header
        is_motion = False
        motion_type = ''
        if '主动议' in line or '修正案' in line:
            if '议程' in line or '讨论' in line or line.startswith('###'):
                is_motion = True
                if '主动议' in line:
                    motion_type = '主动议'
                elif '修正案' in line:
                    motion_type = '修正案'

        if is_motion:
            motion = {'type': motion_type, 'proposer': '', 'content': '', 'result': ''}

            # Look ahead for proposer, content, result
            for j in range(i+1, min(i+30, len(lines))):
                l = lines[j].strip()
                if '提议人' in l and '**' in l:
                    m = re.search(r'提议人[：:]\s*\*?\*?(.+?)\*?\*?$', l)
                    if m:
                        motion['proposer'] = clean_text(m.group(1))[:50]
                if '表决结果' in l:
                    for k in range(j, min(j+8, len(lines))):
                        lk = lines[k].strip()
                        if '通过' in lk:
                            motion['result'] = '通过'
                            break
                        elif '未解决' in lk:
                            motion['result'] = '未解决'
                            break
                        elif '终止' in lk:
                            motion['result'] = '被终止'
                            break
                    break
                if '内容' in l and '```' not in l:
                    # Get next meaningful line as content
                    for k in range(j+1, min(j+5, len(lines))):
                        lk = lines[k].strip()
                        if lk and '```' not in lk and '**' not in lk and len(lk) > 10:
                            motion['content'] = clean_text(lk)[:200]
                            break

            if motion['proposer'] or motion['content']:
                motions.append(motion)
            i = j
        i += 1

    return motions

def parse_topics(text):
    """Extract discussion topic names."""
    topics = []
    for m in re.finditer(r'###\s+自由讨论\s*\d*\s*[：:]\s*(.+)', text):
        t = m.group(1).strip()
        if t and len(t) > 3:
            topics.append(t[:60])
    return topics[:10]

def parse_speakers_from_record(text):
    """Count speaker occurrences in speaking record."""
    speakers = {}
    for m in re.finditer(r'\*\*(.+?)\*\*\s*\[(.+?)\]\s*[（(](.+?)[）)]', text):
        name = m.group(1).strip()
        if name in ['系统', '智能主持人', '智能秘书', '主持人']:
            continue
        if name not in speakers:
            speakers[name] = 0
        speakers[name] += 1
    return speakers

def main():
    all_minutes = sorted(PAST_DOCS.glob("*会议纪要*"))
    all_speaking = {f.stem.split('-')[-2]: f for f in PAST_DOCS.glob("*发言记录*")}

    sessions = []
    all_people = {}

    for mf in all_minutes:
        fname = mf.name
        # Check if this file matches one of our target sessions
        matched = False
        session_label = ''
        for label, date_part in GATHER_SESSIONS.items():
            if date_part in fname:
                matched = True
                session_label = label
                break

        if not matched:
            continue

        text = mf.read_text(encoding='utf-8')
        date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)
        if date_match:
            date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
        else:
            date_str = re.search(r'(\d{8})', fname).group(1)
            date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"

        attendees = parse_attendees(text)
        motions = parse_motions(text)
        topics = parse_topics(text)
        present_count = sum(1 for s in attendees.values() if '出席' in s and '缺席' not in s)

        # Find corresponding speaking record
        speaking_speakers = {}
        for sf in PAST_DOCS.glob("*发言记录*"):
            if date_match:
                sf_date = re.search(r'(\d{8})', sf.name)
                if sf_date and sf_date.group(1)[:6] == date_match.group(0).replace('-', '')[:6]:
                    stext = sf.read_text(encoding='utf-8')
                    speaking_speakers = parse_speakers_from_record(stext)
                    break

        # Accumulate people data
        for name, status in attendees.items():
            if name not in all_people:
                all_people[name] = {
                    'attendedSessions': [],
                    'totalSpeeches': 0,
                    'motionsProposed': 0
                }
            if '出席' in status and '缺席' not in status:
                all_people[name]['attendedSessions'].append(session_label)

        # Count speeches
        for name, count in speaking_speakers.items():
            if name in all_people:
                all_people[name]['totalSpeeches'] += count

        # Count motions proposed
        for motion in motions:
            proposer = motion.get('proposer', '')
            if proposer and proposer in all_people:
                all_people[name]['motionsProposed'] += 1

        session = {
            'label': session_label,
            'date': date,
            'presentCount': present_count,
            'totalMembers': len(attendees),
            'motions': motions,
            'topics': topics
        }
        sessions.append(session)

    # Sort sessions by date
    sessions.sort(key=lambda s: s['date'])

    # Build clean people list
    people_list = []
    for name, data in all_people.items():
        if data['attendedSessions'] or data['totalSpeeches'] > 0:
            people_list.append({
                'name': name,
                'attendedCount': len(data['attendedSessions']),
                'sessions': sorted(data['attendedSessions']),
                'speechCount': data['totalSpeeches'],
                'motionsProposed': data['motionsProposed']
            })

    people_list.sort(key=lambda p: (-p['attendedCount'], -p['speechCount']))

    # Aggregate all motions
    all_motions_list = []
    for s in sessions:
        for m in s['motions']:
            m['sessionLabel'] = s['label']
            m['sessionDate'] = s['date']
            all_motions_list.append(m)

    # Stats
    total_present = sum(s['presentCount'] for s in sessions)
    passed = sum(1 for m in all_motions_list if '通过' in m.get('result', ''))

    data = {
        'stats': {
            'totalSessions': len(sessions),
            'totalPeople': len(people_list),
            'totalMotions': len(all_motions_list),
            'passedMotions': passed,
            'pendingMotions': len(all_motions_list) - passed,
            'totalAttendance': total_present
        },
        'sessions': sessions,
        'people': people_list,
        'motions': all_motions_list
    }

    js_content = "const siteData = " + json.dumps(data, ensure_ascii=False, indent=2) + ";"
    OUTPUT.write_text(js_content, encoding='utf-8')
    print(f"OK: {len(sessions)} sessions, {len(people_list)} people, {len(all_motions_list)} motions")
    for s in sessions:
        ms = [f"{m['proposer']}:{m['result'][:3]}" for m in s['motions']] if s['motions'] else ['-']
        print(f"  {s['date']} {s['label']:12s} present={s['presentCount']:2d}/{s['totalMembers']:2d}  motions=[{', '.join(ms)}]")

if __name__ == '__main__':
    main()
