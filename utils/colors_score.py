import colorsys

# https://www.nngroup.com/articles/color-enhance-design/


def rgb_to_hsl(color):
    r, g, b = color
    r /= 255.0
    g /= 255.0
    b /= 255.0
    h, s, l = colorsys.rgb_to_hls(r, g, b)
    h *= 360.0
    return h, s, l

def get_harmony_score(color1, color2, color3):
    h1, s1, l1 = rgb_to_hsl(color1)
    h2, s2, l2 = rgb_to_hsl(color2)
    h3, s3, l3 = rgb_to_hsl(color3)
    
    # sorting hues
    hues = sorted([h1, h2, h3])
    
    # calculating differences
    diff1 = abs(hues[1] - hues[0])
    diff2 = abs(hues[2] - hues[1])
    
    # we assume the maximum difference for analogous colors is 60 degrees (1/6 of the color wheel)
    max_diff = 60.0
    
    # we normalize differences to the range 0-100
    score1 = (1.0 - min(diff1, max_diff) / max_diff) * 100
    score2 = (1.0 - min(diff2, max_diff) / max_diff) * 100
    
    # average score
    harmony_score = (score1 + score2) / 2.0
    return harmony_score

def get_analogous_score(color1, color2, color3):
    h1, s1, l1 = rgb_to_hsl(color1)
    h2, s2, l2 = rgb_to_hsl(color2)
    h3, s3, l3 = rgb_to_hsl(color3)
    
    # sorting hues
    hues = sorted([h1, h2, h3])
    
    # calculating differences
    diff1 = abs(hues[1] - hues[0])
    diff2 = abs(hues[2] - hues[1])
    
    # we assume the maximum difference for analogous colors is 30 degrees (1/12 of the color wheel)
    max_diff = 30.0
    
    # we normalize differences to the range 0-100
    score1 = (1.0 - min(diff1, max_diff) / max_diff) * 100
    score2 = (1.0 - min(diff2, max_diff) / max_diff) * 100
    
    # average score
    analogous_score = (score1 + score2) / 2.0
    return analogous_score


def get_complementary_score(color1, color2, color3):
    h1, s1, l1 = rgb_to_hsl(color1)
    h2, s2, l2 = rgb_to_hsl(color2)
    h3, s3, l3 = rgb_to_hsl(color3)
    
    # we assume the complementary colors are 180 degrees apart
    diff1 = abs(h1 - (h2 + 180) % 360)
    diff2 = abs(h2 - (h3 + 180) % 360)
    diff3 = abs(h3 - (h1 + 180) % 360)
    
    # we normalize differences to the range 0-100
    score1 = (1.0 - min(diff1, 180.0) / 180.0) * 100
    score2 = (1.0 - min(diff2, 180.0) / 180.0) * 100
    score3 = (1.0 - min(diff3, 180.0) / 180.0) * 100
    
    # average score
    complementary_score = (score1 + score2 + score3) / 3.0
    return complementary_score


def get_split_complementary_score(color1, color2, color3):
    h1, s1, l1 = rgb_to_hsl(color1)
    h2, s2, l2 = rgb_to_hsl(color2)
    h3, s3, l3 = rgb_to_hsl(color3)
    
    # we assume the complementary colors are 150 degrees apart
    diff1 = abs(h1 - (h2 + 150) % 360)
    diff2 = abs(h2 - (h3 + 150) % 360)
    diff3 = abs(h3 - (h1 + 150) % 360)
    
    # we normalize differences to the range 0-100
    score1 = (1.0 - min(diff1, 150.0) / 150.0) * 100
    score2 = (1.0 - min(diff2, 150.0) / 150.0) * 100
    score3 = (1.0 - min(diff3, 150.0) / 150.0) * 100
    
    # average score
    split_complementary_score = (score1 + score2 + score3) / 3.0
    return split_complementary_score


def get_triadic_score(color1, color2, color3):
    h1, s1, l1 = rgb_to_hsl(color1)
    h2, s2, l2 = rgb_to_hsl(color2)
    h3, s3, l3 = rgb_to_hsl(color3)
    
    # we assume the triadic colors are 120 degrees apart
    diff1 = abs(h1 - (h2 + 120) % 360)
    diff2 = abs(h2 - (h3 + 120) % 360)
    diff3 = abs(h3 - (h1 + 120) % 360)
    
    # we normalize differences to the range 0-100
    score1 = (1.0 - min(diff1, 120.0) / 120.0) * 100
    score2 = (1.0 - min(diff2, 120.0) / 120.0) * 100
    score3 = (1.0 - min(diff3, 120.0) / 120.0) * 100
    
    # average score
    triadic_score = (score1 + score2 + score3) / 3.0
    return triadic_score


def get_monochromatic_score(color1, color2, color3):
    h1, s1, l1 = rgb_to_hsl(color1)
    h2, s2, l2 = rgb_to_hsl(color2)
    h3, s3, l3 = rgb_to_hsl(color3)
    
    # we assume the monochromatic colors have the same hue
    hue = (h1 + h2 + h3) / 3.0
    
    # we calculate the differences in lightness and saturation
    diff1 = abs(l1 - l2)
    diff2 = abs(l2 - l3)
    diff3 = abs(l3 - l1)
    diff4 = abs(s1 - s2)
    diff5 = abs(s2 - s3)
    diff6 = abs(s3 - s1)
    
    # we normalize differences to the range 0-100
    score1 = (1.0 - min(diff1, 50.0) / 50.0) * 100
    score2 = (1.0 - min(diff2, 50.0) / 50.0) * 100
    score3 = (1.0 - min(diff3, 50.0) / 50.0) * 100
    score4 = (1.0 - min(diff4, 50.0) / 50.0) * 100
    score5 = (1.0 - min(diff5, 50.0) / 50.0) * 100
    score6 = (1.0 - min(diff6, 50.0) / 50.0) * 100
    
    # average score
    monochromatic_score = (score1 + score2 + score3 + score4 + score5 + score6) / 6.0
    return monochromatic_score

def analyse_colors(color1, color2, color3):
    harmony_score = get_harmony_score(color1, color2, color3)
    analogous_score = get_analogous_score(color1, color2, color3)
    complementary_score = get_complementary_score(color1, color2, color3)
    split_complementary_score = get_split_complementary_score(color1, color2, color3)
    triadic_score = get_triadic_score(color1, color2, color3)
    monochromatic_score = get_monochromatic_score(color1, color2, color3)

    return harmony_score, analogous_score, complementary_score, split_complementary_score, triadic_score, monochromatic_score
