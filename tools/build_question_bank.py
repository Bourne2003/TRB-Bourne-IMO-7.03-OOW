#!/usr/bin/env python3
"""รวบรวมคำถามสอบปากเปล่าจากทุกบท แล้วสร้าง appendices/B-oral-exam-question-bank.md

ส่วนหัวและส่วนท้าย (คำแนะนำการสอบ คำถามสถานการณ์ คำถามสัมภาษณ์) เขียนไว้ใน tools/qbank/
รันใหม่ทุกครั้งที่แก้คำถามท้ายบท:  python3 tools/build_question_bank.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, 'chapters')
OUT = os.path.join(ROOT, 'appendices', 'B-oral-exam-question-bank.md')
QB = os.path.join(ROOT, 'tools', 'qbank')

GROUPS = [
    ('00-intro', 'บทนำ — STCW และ Model Course 7.03'),
    ('01-navigation', 'Function 1 — Navigation at the operational level'),
    ('02-cargo', 'Function 2 — Cargo handling and stowage at the operational level'),
    ('03-ship-operation', 'Function 3 — Controlling the operation of the ship and care for persons on board at the operational level'),
]
QHEAD = re.compile(r'^## .*คำถามสอบปากเปล่า')
QLINE = re.compile(r'^\*\*(ถาม|Q)[^*]*\*\*')


def extract(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    title = lines[0].lstrip('# ').strip()
    start = next((i for i, l in enumerate(lines) if QHEAD.match(l)), None)
    if start is None:
        return title, []
    body = []
    for l in lines[start + 1:]:
        if l.strip() == '---' or l.startswith('## '):
            break
        body.append('#' + l if l.startswith('### ') else l)
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    return title, body


def main():
    head = open(os.path.join(QB, 'head.md'), encoding='utf-8').read().rstrip() + '\n'
    tail = open(os.path.join(QB, 'tail.md'), encoding='utf-8').read().rstrip() + '\n'
    parts, toc, total = [], [], 0
    for folder, gname in GROUPS:
        files = sorted(f for f in os.listdir(os.path.join(CH, folder)) if f.endswith('.md'))
        parts.append(f'\n## {gname}\n')
        for f in files:
            title, body = extract(os.path.join(CH, folder, f))
            n = sum(1 for l in body if QLINE.match(l))
            if not n:
                continue
            total += n
            anchor = f.replace('.md', '')
            toc.append(f'| {title} | {n} | [ไปยังชุดคำถาม](#q-{anchor}) · [อ่านบทเต็ม](../chapters/{folder}/{f}) |')
            parts.append(f'\n<a id="q-{anchor}"></a>\n\n### {title}\n\n*จากบท [{f}](../chapters/{folder}/{f}) — {n} ข้อ*\n')
            parts.append('\n'.join(body) + '\n')
    summary = ['\n## สารบัญชุดคำถามรายบท\n', f'รวมคำถามท้ายบททั้งหมด **{total} ข้อ** (นับเฉพาะคำถามท้ายบท ไม่รวมคำถามสถานการณ์และคำถามสัมภาษณ์ในส่วนท้าย)\n',
               '| บท | จำนวนข้อ | ลิงก์ |', '|---|---|---|'] + toc
    text = head + '\n'.join(summary) + '\n\n---\n' + ''.join(parts) + '\n---\n\n' + tail
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(text)
    print(f'wrote {OUT}: {total} chapter questions')


if __name__ == '__main__':
    main()
