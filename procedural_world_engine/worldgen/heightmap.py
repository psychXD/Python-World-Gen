import random
import numpy as np
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt

width = 512
height = 512
scale = 50.0
octaves = 4  # Must be an integer for tiling
persistence = 0.5
lacunarity = 2.0
tile_sizes = None # (2, 2)  # Uncomment for tiling; set to None for no tiling

heightmap = np.zeros((width, height))

noise = PerlinNoise(octaves=octaves, seed=random.randint(0, 100))

for x in range(width):
    for y in range(height):
        nx = x / scale
        ny = y / scale
        total = 0
        frequency = 1
        amplitude = 1
        for _ in range(octaves):
            if tile_sizes:
                value = noise([nx * frequency, ny * frequency], tile_sizes=tile_sizes)
            else:
                value = noise([nx * frequency, ny * frequency])
            total += value * amplitude
            frequency *= lacunarity
            amplitude *= persistence
        heightmap[x][y] = total

# heightmap = (heightmap - np.min(heightmap)) / (np.max(heightmap) - np.min(heightmap))

plt.imshow(heightmap, cmap='gray')
plt.savefig("heightMap.png")
np.save("heightMap.npy", heightmap)
print("heightMap generated and saved.")


