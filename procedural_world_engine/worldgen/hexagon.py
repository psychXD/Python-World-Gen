import math
import numpy as np
from terrain import loadHeightMap  # ✅ Import heightmap

# 📌 Hexagonal Grid System
# This file handles converting (x, y) positions into hexagonal (q, r) coordinates.
# It will be used by `biome.py` and `main.py` to structure the world into hexagons.

# ✅ Constants for hex size & calculations
HEX_SIZE = 10  # Adjust this to control hexagon width
SQRT_3 = math.sqrt(3)  # Used for axial coordinate calculations

def world_to_hex(x, y):
    """
    📌 Converts (x, y) world coordinates into (q, r) hexagonal coordinates.
    - Uses axial coordinate system for hexagonal grids.
    """
    q = (2/3 * x) / HEX_SIZE
    r = (-1/3 * x + SQRT_3/3 * y) / HEX_SIZE
    return round(q), round(r)  # Snap to nearest hex

def hex_to_world(q, r):
    """
    📌 Converts (q, r) hexagonal coordinates back into (x, y) world coordinates.
    - Helps when rendering objects at correct positions.
    """
    x = HEX_SIZE * (3/2 * q)
    y = HEX_SIZE * (SQRT_3 * (r + q/2))
    return x, y

def get_height_for_hex(q, r, heightmap):
    """
    📌 Returns the height from the heightmap for a given hex (q, r).
    - Converts hex to (x, y) and finds the closest heightmap value.
    """
    x, y = hex_to_world(q, r)  # Convert hex to world coords
    x_idx = min(max(int(x), 0), heightmap.shape[1] - 1)  # Keep inside bounds
    y_idx = min(max(int(y), 0), heightmap.shape[0] - 1)
    return heightmap[y_idx, x_idx]  # Get height from heightmap

def get_neighboring_hexes(q, r):
    """
    📌 Returns a list of neighboring hexes for a given (q, r) coordinate.
    - Helps in biome blending & efficient world loading.
    """
    directions = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
    return [(q + dq, r + dr) for dq, dr in directions]

def distance_between_hexes(q1, r1, q2, r2):
    """
    📌 Returns the hex distance between two hexagonal coordinates.
    - Helps in field-of-view optimizations.
    """
    return max(abs(q1 - q2), abs(r1 - r2), abs(q1 + r1 - q2 - r2))

if __name__ == "__main__":
    heightmap = loadHeightMap()  # ✅ Load heightmap
    test_x, test_y = 15, 20
    q, r = world_to_hex(test_x, test_y)
    print(f"🌍 ({test_x}, {test_y}) → Hex ({q}, {r})")
    print(f"📍 Hex ({q}, {r}) → World {hex_to_world(q, r)}")
    print(f"🗻 Height at Hex ({q}, {r}): {get_height_for_hex(q, r, heightmap)}")
