"""Tightly crop an independent asset; preserve transparency and soft edges."""
import argparse
import json
from pathlib import Path
from PIL import Image


def crop_asset(source, output, box=None, padding=12, threshold=0):
    if padding < 10:
        raise ValueError('Use at least 10px safety padding')
    if not 0 <= threshold <= 255:
        raise ValueError('Alpha threshold must be 0..255')
    im = Image.open(source)
    has_alpha = 'A' in im.getbands() or 'transparency' in im.info
    if box:
        l, t, r, b = box
        if not (0 <= l < r <= im.width and 0 <= t < b <= im.height):
            raise ValueError('Crop box is empty or outside image')
        im = im.crop(box)
    if has_alpha:
        im = im.convert('RGBA')
        bbox = im.getchannel('A').point(lambda a: 255 if a > threshold else 0).getbbox()
        if not bbox:
            raise ValueError('Asset is fully transparent')
        # Default threshold=0 keeps all soft gradient pixels.
        im = im.crop(bbox)
        result = Image.new('RGBA', (im.width + padding * 2, im.height + padding * 2))
        result.paste(im, (padding, padding))
        im = result
    else:
        bbox = None
        if not box:
            raise ValueError('Opaque image requires explicit --box; refusing automatic white removal')
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    im.save(target)
    return {'source': str(source), 'output': str(output), 'size': list(im.size),
            'alpha_crop_bbox': bbox, 'padding': padding if has_alpha else 0,
            'source_box': box, 'threshold': threshold}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source'); p.add_argument('output')
    p.add_argument('--box', nargs=4, type=int)
    p.add_argument('--padding', type=int, default=12)
    p.add_argument('--threshold', type=int, default=0)
    args = p.parse_args()
    print(json.dumps(crop_asset(args.source, args.output, args.box, args.padding, args.threshold), ensure_ascii=False))
