




BIOME_DEFINITIONS = \
{
    "start_village":    ("The Village on the Plains", ""),
    "village":          ("The Village of ---", ""),
    "plains":           ("Rolling Plains", ""),
    "forest":           ("A Lush Forest", ""),
    "desert":           ("An Arid Desert", ""),
    "badlands":         ("Badlands", ""),
    "mountains":        ("Mountains", ""),
    "lake":             ("A Lake", "")
}


BIOME_TRANSFORMS = \
{
    "start_village":    ("plains"),
    "village":          ("plains", "forest", "desert", "badlands", "mountains", "lake"),
    "plains":           ("plains", "forest", "badlands", "mountains", "lake"),
    "forest":           ("plains", "forest", "badlands", "mountains", "lake"),
    "desert":           ("desert", "badlands", "mountains"),
    "badlands":         ("plains", "forest", "desert", "badlands", "mountains"),
    "mountains":        ("plains", "forest", "desert", "badlands", "mountains", "lake"),
    "lake":             ("plains", "badlands", "mountains", "lake")
}


BIOME_FREQ = \
{
    "plains":       0.3,
    "forest":       0.2,
    "desert":       0.1,
    "badlands":     0.2,
    "mountains":    0.1,
    "lake":         0.1
}


BIOME_COLORS = \
{
    None:               (255,255,255),
    "start_village":    (128,0,0),
    "village":          (139,69,19),
    "plains":           (50,205,50),
    "forest":           (34,139,34),
    "desert":           (240,230,140),
    "badlands":         (210,180,140),
    "mountains":        (128,128,128),
    "lake":             (0,191,255)
}


def buildBiomeFreqList(biomeList):
    ret = []
    t = 0.0
    for b in biomeList:
        ret.append(BIOME_FREQ[b])
        t = t + BIOME_FREQ[b]
    for i in range(len(ret)):   ret[i] = ret[i] / t
    return ret


#BIOMES = set(BIOME_DEFINITIONS.keys())
#BIOMES_PLAIN = set(BIOME_FREQ.keys())
#BIOMES_SPECIAL = BIOMES - BIOMES_PLAIN


#===============================================================================
