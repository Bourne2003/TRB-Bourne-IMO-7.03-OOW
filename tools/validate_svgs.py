"""ตรวจว่าไฟล์ SVG ทุกไฟล์เป็น XML ที่ถูกต้อง (GitHub แสดงผล SVG แบบ XML เข้มงวด)"""
import glob, os, sys, xml.dom.minidom
bad = 0
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), '..', 'images', '*.svg'))):
    try:
        xml.dom.minidom.parse(f)
    except Exception as e:
        bad += 1
        print('INVALID', os.path.basename(f), e)
print('checked, invalid =', bad)
sys.exit(1 if bad else 0)
