import matplotlib.pyplot as plt
import numpy as np


def loadHeightMap():
    return np.load("/home/harsh/procedural_world_engine/data/heightMap.npy")

def vissuliseTerrain():
    heightmap = loadHeightMap()
    plt.imshow(heightmap, cmap='gray')
    plt.colorbar()
    plt.title("Loaded Terrain Heightmap")
    plt.show()

if __name__ == "__main__":
    vissuliseTerrain()