import colorsys

def create_hue(what):
    h = (what % 360) / 360.0
    s = 1
    v = 1
    (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))
