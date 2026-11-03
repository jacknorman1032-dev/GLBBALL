# Remove a solid background by flood-filling from the image edges; keeps enclosed light areas (eyes, mouths)
import sys, numpy as np
from PIL import Image
from collections import deque
from scipy.ndimage import binary_dilation
def clean(src, dst, bgval=None, tol=14, erase=None, size=400, keep=None):
    im = np.array(Image.open(src).convert('RGBA')); h, w = im.shape[:2]; rgb = im[..., :3].astype(int)
    if bgval is None: bgval = rgb[2, 2]
    bg = (np.abs(rgb - np.array(bgval)).max(axis=2) <= tol) & (im[..., 3] > 0)
    seen = np.zeros((h, w), bool); q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if bg[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if bg[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and bg[ny, nx] and not seen[ny, nx]: seen[ny, nx] = True; q.append((ny, nx))
    if keep:  # keep=box (x0,y0,x1,y1) or polygon [(x,y),...]: background-colored area inside this box stays opaque (e.g. an open mouth)
        from PIL import ImageDraw
        m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).polygon(keep if len(keep) > 4 else [(keep[0], keep[1]), (keep[2], keep[1]), (keep[2], keep[3]), (keep[0], keep[3])], fill=1)
        box = np.array(m).astype(bool)
        seen &= ~(box & bg)
    im[seen, 3] = 0
    edge = binary_dilation(seen) & ~seen & (rgb.min(axis=2) > 200); im[edge, 3] = 60
    if erase:
        for (x0, y0, x1, y1) in erase: im[y0:y1, x0:x1, 3] = 0
    out = Image.fromarray(im); out = out.crop(out.getbbox()); out.thumbnail((size, size), Image.LANCZOS); out.save(dst, optimize=True)
    print(dst, out.size, 'bg removed', round(seen.mean(), 3))
if __name__ == '__main__':
    pass

def outline(path, px=5):
    """Add a white sticker outline around a transparent logo (for logos close to their school's header color)."""
    from scipy.ndimage import binary_dilation
    im = Image.open(path).convert('RGBA'); pad = px + 2
    base = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); base.paste(im, (pad, pad), im)
    a = np.array(base)[..., 3] > 40
    yy, xx = np.ogrid[-px:px + 1, -px:px + 1]; disk = xx * xx + yy * yy <= px * px
    ring = binary_dilation(a, structure=disk)
    out = np.zeros((base.height, base.width, 4), np.uint8); out[ring] = (255, 255, 255, 255)
    o = Image.fromarray(out); o.alpha_composite(base); o.save(path, optimize=True); print(path, o.size)
