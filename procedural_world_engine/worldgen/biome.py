# import numpy as np
# import os
# import random
# from datetime import datetime  # ✅ For timestamps
# from terrain import loadHeightMap

# # Path to save/load biome objects
# SAVE_PATH = "data/biome_objects.npy"
# DEBUG_LOG = "data/debug.log"  # ✅ Moved to `data/` so it's easy to find
# print("🚀 biome.py has started running...")

# # Define available assets per biome
# BIOME_ASSETS = {
#     "forest": ["BirchTree_1", "BirchTree_2", "BirchTree_3", "BirchTree_4", "TreeStump", "CommonTree_1"],
#     "plains": ["Grass", "Grass_2", "Wheat", "Rock_1"],
#     "beach": ["PalmTree_1", "Rock_1", "Rock_Moss_2"]
# }

# # Biome object density (higher values = more objects)
# BIOME_DENSITY = {
#     "forest": 0.6,  
#     "plains": 0.4,  
#     "beach": 0.2    
# }

# # ✅ Debug Logging
# def log_debug(message):
#     """Writes debug messages to both a log file and prints to the console."""
#     timestamp = f"[{datetime.now()}] {message}"
#     print(timestamp)  # ✅ Show in terminal
#     with open(DEBUG_LOG, "a") as log_file:
#         log_file.write(timestamp + "\n")

# def load_biome_objects():
#     print("✅ load_biome_objects() function was called!")  # Debug print

#     if os.path.exists(SAVE_PATH):
#         print(f"ℹ Found existing {SAVE_PATH}, loading...")
#         return np.load(SAVE_PATH, allow_pickle=True).item()

#     print("🚀 Biome file not found, generating new biome objects...")
#     return generate_biome_objects()


# def generate_biome_objects():
#     """
#     📌 Generates biome objects based on the heightmap and saves them.
#     """
#     heightmap = loadHeightMap()
#     height, width = heightmap.shape

#     log_debug(f"🌍 Generating biome objects for {width}x{height} terrain.")

#     object_positions = {
#         "forest": [],
#         "plains": [],
#         "beach": []
#     }
#     object_count = {"forest": 0, "plains": 0, "beach": 0}  

#     for y in range(height):
#         for x in range(width):
#             h = heightmap[y, x]  # Get terrain height at (x, y)

#             # 🌊 Skip water areas
#             if h < 0.3:
#                 continue
            
#             # 🏝 Beach biome
#             elif h < 0.35:
#                 if np.random.rand() < BIOME_DENSITY["beach"]:
#                     object_positions["beach"].append({
#                         "pos": (x, y, h),  
#                         "rotation": np.random.uniform(0, 360),
#                         "scale": np.random.uniform(0.8, 1.2)
#                     })
#                     object_count["beach"] += 1  

#             # 🌲 Forest biome
#             elif h < 0.6:
#                 if np.random.rand() < BIOME_DENSITY["forest"]:
#                     object_positions["forest"].append({
#                         "pos": (x, y, h),
#                         "rotation": np.random.uniform(0, 360),
#                         "scale": np.random.uniform(0.8, 1.2)
#                     })
#                     object_count["forest"] += 1  

#             # 🌾 Plains biome
#             elif h < 0.8:
#                 if np.random.rand() < BIOME_DENSITY["plains"]:
#                     object_positions["plains"].append({
#                         "pos": (x, y, h),
#                         "rotation": np.random.uniform(0, 360),
#                         "scale": np.random.uniform(0.8, 1.2)
#                     })
#                     object_count["plains"] += 1  

#     log_debug(f"✅ Biome objects generated: {object_count}")

#     # 📝 Save the biome objects
#     np.save(SAVE_PATH, object_positions)
#     log_debug("💾 Biome objects saved successfully.")
#     log_debug("🎉 Process Completed Successfully!")

#     return object_positions

# # 🏔 Placeholder for future mountain biome logic
# def generate_mountain_objects():
#     log_debug("⚠ generate_mountain_objects() called, but not yet implemented.")
#     return {}

# if __name__ == "__main__":
#     print("🚀 Running biome.py directly...")
#     biome_data = load_biome_objects()
#     print("✅ Biome data successfully loaded or generated!")


import numpy as np
import os
import random
from datetime import datetime
from terrain import loadHeightMap
from hexagon import world_to_hex, get_height_for_hex

# Path to save/load biome objects
SAVE_PATH = "data/biome_objects.npy"
DEBUG_LOG = "data/debug.log"
BIOME_MAP_PATH = "data/finalBiome.npy"  # Load precomputed biome distribution

# Define available assets per biome
BIOME_ASSETS = {
    "forest": ["BirchTree_1", "BirchTree_2", "BirchTree_3", "BirchTree_4", "TreeStump", "CommonTree_1"],
    "plains": ["Grass", "Grass_2", "Wheat", "Rock_1"],
    "beach": ["PalmTree_1", "Rock_1", "Rock_Moss_2"]
}

# Biome object density (higher values = more objects)
BIOME_DENSITY = {
    "forest": 0.6,  
    "plains": 0.4,  
    "beach": 0.2    
}

def log_debug(message):
    """Writes debug messages to both a log file and prints to the console."""
    timestamp = f"[{datetime.now()}] {message}"
    print(timestamp)
    with open(DEBUG_LOG, "a") as log_file:
        log_file.write(timestamp + "\n")

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
