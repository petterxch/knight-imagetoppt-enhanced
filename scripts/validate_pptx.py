"""Targeted package, DrawingML, font and integer-coordinate checks; not full SDK validation."""
import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from pptx_xml_checks import validate, A


def check(path, font='宋体'):
    result = validate(path)
    texts = 0
    with ZipFile(path) as z:
        slides = sorted(n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n))
        for filename in slides:
            root = etree.fromstring(z.read(filename))
            for r in root.findall(f'.//{{{A}}}r'):
                t = r.find(f'{{{A}}}t')
                if t is None or not t.text:
                    continue
                texts += 1
                rp = r.find(f'{{{A}}}rPr')
                size = rp.get('sz') if rp is not None else None
                if not size or not re.fullmatch(r'\d+', size) or int(size) % 100:
                    result['errors'].append([filename, 'font size is missing or noninteger pt', t.text])
                if font:
                    for tag in ('latin', 'ea', 'cs'):
                        el = rp.find(f'{{{A}}}{tag}') if rp is not None else None
                        if el is None or el.get('typeface') != font:
                            result['errors'].append([filename, 'missing expected explicit typeface', tag, t.text])
            for pt in root.findall(f'.//{{{A}}}pt'):
                for attr in ('x', 'y'):
                    if not re.fullmatch(r'-?\d+', pt.get(attr, '')):
                        result['errors'].append([filename, 'noninteger geometry coordinate', dict(pt.attrib)])
    result.update(slide_count=len(slides), text_runs_checked=texts, expected_font=font,
                  powerpoint_open_test=False, ok=not result['errors'])
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('pptx'); p.add_argument('--font', default='宋体'); p.add_argument('--json')
    args = p.parse_args(); result = check(args.pptx, args.font)
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json:
        target = Path(args.json); target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding='utf-8')
    print(output)
    raise SystemExit(0 if result['ok'] else 1)
