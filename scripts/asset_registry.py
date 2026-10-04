"""Index explicitly authorized local asset roots without claiming provenance."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image


def scan(root):
    root = Path(root).resolve()
    entries = []
    for f in sorted(root.rglob('*')):
        if not f.is_file() or f.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp'}:
            continue
        # Refuse symlinks which escape the approved root.
        if not f.resolve().is_relative_to(root):
            continue
        with Image.open(f) as im:
            alpha = im.convert('RGBA').getchannel('A').getbbox() if 'A' in im.getbands() or 'transparency' in im.info else None
            entries.append({'id': hashlib.sha256(f.read_bytes()).hexdigest()[:16],
                            'path': str(f.relative_to(root)), 'size': list(im.size),
                            'mode': im.mode, 'alpha_bbox': alpha, 'classification': 'unclassified',
                            'provenance_verified': False, 'source': None, 'tags': []})
    return {'root': str(root), 'assets': entries}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', required=True); p.add_argument('--output', required=True)
    a = p.parse_args(); result = scan(a.root)
    target = Path(a.output); target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Indexed {len(result["assets"])} assets; provenance requires manual verification')
