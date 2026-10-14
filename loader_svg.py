"""Animated flower loader: petals open and close, built from the two Figma frames
("gif 01" closed / "gif 02" open). The petal paths share the same command structure,
so SVG <animate> morphs them point by point. Crisper and far smaller than a GIF."""

CLOSED = {
    'p2': 'M97.2444 82.8569C112.722 70.7029 142.074 69.5647 124.458 98.8534C110.709 121.712 74.3435 142.859 63.9413 134.981C53.5392 127.103 84.974 92.4927 97.2448 82.8569H97.2444Z',
    'p3': 'M65.565 135.053C48.0745 132.663 46.7322 88.6272 62.4097 64.6199C74.547 46.0338 95.0364 50.2593 91.3044 83.7361C87.5725 117.213 72.2156 135.961 65.565 135.052V135.053Z',
    'g1': (95.8888, 74.7998, 95.8888, 136.66),
    'g2': (71.622, 53.6641, 71.622, 135.084),
}
OPEN = {
    # Figma wrote these two with H/L where the closed frame has H/V; normalise to the same commands
    'p2': 'M105.696 85.8515C123.639 77.7689 152.406 83.7106 128.274 107.914C109.439 126.803 69.0599 138.6 60.8533 128.455C52.6467 118.311 91.4714 92.2596 105.697 85.8516H105.696Z',
    'p3': 'M74.317 134.953C56.9354 138.036 42.1679 96.528 49.7376 68.8724C55.5978 47.4617 76.3965 45.2075 83.099 78.2181C89.8015 111.229 80.9261 133.78 74.3169 134.952V134.953Z',
    'g1': (106.315, 77.7046, 91.4632, 137.756),
    'g2': (55.1509, 55.6212, 80.0924, 133.127),
}
P1 = 'M109.064 49.4703C119.513 56.1699 118.758 81.2221 101.738 107.583C86.737 130.819 75.2391 138.651 67.4387 136.244C40.7253 128.002 77.5887 29.2903 109.064 49.4703Z'
STEM = 'M91.9256 129.128C86.2157 136.321 70.1752 139.258 63.3844 135.778C57.3157 132.667 51.2116 121.935 51.46 110.524C57.0719 121.428 77.0557 129.456 91.9256 129.128Z'

DUR = '1.6s'
# closed → open (hold) → closed (hold)
KT = '0;0.38;0.55;0.93;1'
KS = '.45 0 .25 1;0 0 1 1;.45 0 .25 1;0 0 1 1'


def _anim(attr, a, b):
    return (f'<animate attributeName="{attr}" dur="{DUR}" repeatCount="indefinite" calcMode="spline" '
            f'keyTimes="{KT}" keySplines="{KS}" values="{a};{b};{b};{a};{a}"/>')


def _grad(gid, c, o):
    names = ('x1', 'y1', 'x2', 'y2')
    anims = ''.join(_anim(n, c[i], o[i]) for i, n in enumerate(names))
    return (f'<linearGradient id="{gid}" x1="{c[0]}" y1="{c[1]}" x2="{c[2]}" y2="{c[3]}" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="#FF0000"/><stop offset="1" stop-color="#FF89CF"/>{anims}</linearGradient>')


def flower_svg(cls='flower-loader'):
    return f'''<svg class="{cls}" viewBox="40 40 104 104" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Loading">
  <defs>
    <linearGradient id="fl-g0" x1="87.0821" y1="46.7568" x2="87.0821" y2="136.66" gradientUnits="userSpaceOnUse"><stop stop-color="#FF0000"/><stop offset="1" stop-color="#FF89CF"/></linearGradient>
    {_grad('fl-g1', CLOSED['g1'], OPEN['g1'])}
    {_grad('fl-g2', CLOSED['g2'], OPEN['g2'])}
  </defs>
  <g stroke="#000" stroke-width="1">
    <path d="{P1}" fill="url(#fl-g0)"/>
    <path d="{CLOSED['p2']}" fill="url(#fl-g1)">{_anim('d', CLOSED['p2'], OPEN['p2'])}</path>
    <path d="{CLOSED['p3']}" fill="url(#fl-g2)">{_anim('d', CLOSED['p3'], OPEN['p3'])}</path>
    <path d="{STEM}" fill="#B2D895"/>
  </g>
</svg>'''


if __name__ == '__main__':
    import re
    for k in ('p2', 'p3'):  # sanity: same command sequence in both frames
        a = re.sub(r'[^A-Za-z]', '', CLOSED[k]); b = re.sub(r'[^A-Za-z]', '', OPEN[k])
        assert a == b, (k, a, b)
        na = len(re.findall(r'-?\d*\.?\d+', CLOSED[k])); nb = len(re.findall(r'-?\d*\.?\d+', OPEN[k]))
        assert na == nb, (k, na, nb)
    open('/tmp/flower.svg', 'w').write(flower_svg())
    print('ok')
