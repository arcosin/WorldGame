from PIL import Image
from Biomes import BIOME_COLORS


DEFAULT_IMAGE_WIDTH = 3000
DEFAULT_IMAGE_HEIGHT = 3000


def buildMapImage(world, filename):
    grid = world.coords.buildListGrid()
    gridHeight = len(grid)
    gridWidth = len(grid[0])
    imageHeight = DEFAULT_IMAGE_HEIGHT
    imageWidth = DEFAULT_IMAGE_WIDTH
    nodeHeight = imageHeight // gridHeight
    nodeWidth = imageWidth // gridWidth
    img = Image.new('RGB', (imageWidth, imageHeight))
    for i in range(0, gridHeight):
        for j in range(0, gridWidth):
            node = grid[i][j]
            rect = (i * nodeHeight, j * nodeWidth, ((i + 1) * nodeHeight) - 1, ((j + 1) * nodeWidth) - 1)
            if node == None:    biome = None
            else:               biome = node.getEnviroment().biome
            #print("color %s as RGB %s." % (rect, BIOME_COLORS[biome]))
            img.paste(BIOME_COLORS[biome], rect)
    img.save(filename)



def printMapGrid(world):
    grid = world.coords.buildListGrid()
    print("[\n")
    for row in grid:
        for entry in row:
            if entry == None:   print("*,\t", end='')
            else:   print("%d,\t" % entry.id, end='')
        print("\n")
    print("]\n")





#===============================================================================
