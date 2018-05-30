

BIOME_DEFINITIONS = {
                        "start_village":    ("The Village on the Plains", ""),
                        "village":          ("The Village of ---", ""),
                        "plains":           ("Rolling Plains", ""),
                        "forest":           ("A Lush Forest", ""),
                        "desert":           ("An Arid Desert", ""),
                        "badlands":         ("Badlands", ""),
                        "mountains":        ("Mountains", ""),
                        "lake":             ("A Lake", "")
                    }


BIOME_TRANSFORMS = {
                        "start_village":    ("plains"),
                        "village":          ("plains", "forest", "desert", "badlands", "mountains", "lake"),
                        "plains":           ("plains", "forest", "badlands", "mountains", "lake"),
                        "forest":           ("plains", "forest", "badlands", "mountains", "lake"),
                        "desert":           ("desert", "badlands", "mountains"),
                        "badlands":         ("plains", "forest", "desert", "badlands", "mountains"),
                        "mountains":        ("plains", "forest", "desert", "badlands", "mountains", "lake"),
                        "lake":             ("plains", "badlands", "mountains", "lake")
                    }


BIOMES = set(BIOME_DEFINITIONS.keys())



#===============================================================================
