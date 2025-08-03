import numpy as np
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import random
from datetime import datetime
from worldgen.terrain import loadHeightMap
from worldgen.hexagon import world_to_hex, get_height_for_hex

# Path to save/load biome objects
SAVE_PATH = "data/biome_objects.npy"
DEBUG_LOG = "data/debug.log"
BIOME_MAP_PATH = "data/finalBiome.npy"  #

# Defining available assets per biome
BIOME_ASSETS = {
    "forest": ["BirchTree_1", "BirchTree_2", "BirchTree_3", "BirchTree_4", "TreeStump", "CommonTree_1"],
    "plains": ["Grass", "Grass_2", "Wheat", "Rock_1"],
    "beach": ["PalmTree_1", "Rock_1", "Rock_Moss_2"]
}

# Biome object density 
BIOME_DENSITY = {
    "forest": 0.6,  
    "plains": 0.4,  
    "beach": 0.2    
}

def log_debug(message):
    log_dir = "data"
    log_file_path = os.path.join(log_dir, "debug.log")
    
    # Create the directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    # Create the log file if it doesn't exist
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as f:
            pass

    with open(log_file_path, "a") as log_file:
        log_file.write(message + "\n")


def load_biome_objects():
    log_debug("Loading biome objects...")
    if os.path.exists(SAVE_PATH):
        log_debug("Biome objects loaded from file.")
        return np.load(SAVE_PATH, allow_pickle=True).item()
    log_debug("Biome file not found. Generating new biome objects...")
    return generate_biome_objects()

def generate_biome_objects():
    log_debug("Generating biome objects...")
    heightmap = loadHeightMap()
    biome_map = np.load(BIOME_MAP_PATH)  # Load biome distribution
    height, width = heightmap.shape
    object_positions = {}
    
    for y in range(height):
        for x in range(width):
            h = heightmap[y, x]
            if h < 0.3:
                continue
            
            q, r = world_to_hex(x, y)
            hex_key = (q, r)
            hex_height = get_height_for_hex(q, r, heightmap)
            
            if hex_key not in object_positions:
                object_positions[hex_key] = []
            
            biome_color = biome_map[y, x]
            biome_type = None
            
            if np.allclose(biome_color, [0.9, 0.8, 0.6]):
                biome_type = "beach"
            elif np.allclose(biome_color, [0, 0.5, 0]):
                biome_type = "forest"
            elif np.allclose(biome_color, [0.5, 0.7, 0.3]):
                biome_type = "plains"
            
            if biome_type and random.random() < BIOME_DENSITY[biome_type]:
                chosen_biome = random.choice([biome_type, random.choice(list(BIOME_ASSETS.keys()))])
                object_positions[hex_key].append({
                    "biome": chosen_biome,
                    "pos": (q, r, hex_height),
                    "rotation": random.uniform(0, 360),
                    "scale": random.uniform(0.8, 1.2)
                })
    
    np.save(SAVE_PATH, object_positions)
    log_debug("Biome objects successfully generated and saved.")
    return object_positions

def generate_mountain_objects():
    log_debug("Mountain object generation not implemented yet.")
    return {}

if __name__ == "__main__":
    biome_data = load_biome_objects()
    log_debug("Biome script execution completed successfully.")
