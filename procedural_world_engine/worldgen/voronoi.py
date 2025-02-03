import numpy as np
import matplotlib.pyplot as plt
from terrain import loadHeightMap  # Load the generated heightmap

def generate_biome_map():
    heightmap = loadHeightMap()
    height, width = heightmap.shape
    biome_map = np.zeros((height, width, 3))  # RGB color map

    # Define biome colors
    COLORS = {
        "water": (0, 0, 0.5),        # Deep blue
        "shallow_water": (0, 0.3, 0.7), # Light blue
        "beach": (0.9, 0.8, 0.6),    # Sandy color
        "forest": (0, 0.5, 0),       # Dark green
        "plains": (0.5, 0.7, 0.3),   # Yellow-green
        "mountain": (0.5, 0.5, 0.5), # Gray for mountains
        "snow": (1, 1, 1),           # White for snow peaks
    }

    # Assign biomes based on height
    for y in range(height):
        for x in range(width):
            h = heightmap[y, x]
            if h < 0.15:
                biome_map[y, x] = COLORS["water"]
            elif h < 0.2:
                biome_map[y, x] = COLORS["beach"]
            elif h < 0.4:
                biome_map[y, x] = COLORS["plains"]
            elif h < 0.6:
                biome_map[y, x] = COLORS["forest"]
            elif h < 0.8:
                biome_map[y, x] = COLORS["mountain"]
            else:
                biome_map[y, x] = COLORS["snow"]

    return biome_map

if __name__ == "__main__":
    biome_map = generate_biome_map()
    plt.imshow(biome_map)
    plt.savefig("finalBiome.png")
    np.save("finalBiome.npy", biome_map)
    plt.title("Biome Map")
    plt.axis("off")
    plt.show()
