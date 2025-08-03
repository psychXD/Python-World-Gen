from ursina import *
import numpy as np
import os

print("Current working directory:", os.getcwd())

app = Ursina() 

asset_path = Path('../assets/blend').resolve()
application.asset_folder = asset_path
print(f"Asset folder: {asset_path}")

# List files to verify
print("Files in asset folder:")
for f in asset_path.iterdir():
    print(f)

# Now load models by filename only
asset_models = {
    'PalmTree_1': load_model('PalmTree_1.glb'),
    'Rock_1': load_model('Rock_1.glb'),
    'Rock_3': load_model('Rock_3.glb'),
    'CommonTree_1': load_model('CommonTree_1.glb'),
    'Bush_1': load_model('Bush_1.glb'),
    'Grass': load_model('Grass.glb'),
    'Wheat': load_model('Wheat.glb'),
    'Plant_1': load_model('Plant_1.glb'),
    'BirchTree_1': load_model('BirchTree_1.glb'),
    'BirchTree_2': load_model('BirchTree_2.glb'),
    'BirchTree_3': load_model('BirchTree_3.glb'),
    'BirchTree_4': load_model('BirchTree_4.glb'),
    'BirchTree_5': load_model('BirchTree_5.glb'),
    'BushBerries_1': load_model('BushBerries_1.glb'),
    'Rock_Moss_2': load_model('Rock_Moss_2.glb'),
    'Grass_2': load_model('Grass_2.glb'),
    'Rock_4': load_model('Rock_4.glb'),
    'TreeStump': load_model('TreeStump.glb')
}

print("Loaded models:")
for name, model in asset_models.items():
    print(f"{name}: {model}")

# === Check loaded models ===
print("Loaded models:", asset_models)

import random

def place_assets(heightmap, terrain_entity):
    rows, cols = heightmap.shape
    scale_xz = terrain_entity.scale_x
    scale_y = terrain_entity.scale_y

    print(asset_models)

    for _ in range(500):  # Adjust as needed
        x = random.randint(0, rows - 1)
        z = random.randint(0, cols - 1)
        h = heightmap[x][z]

        world_x = x * scale_xz
        world_z = z * scale_xz
        world_y = h * scale_y

        if h < 0.1:
            continue
        elif h < 0.2:
            asset_choice = random.choice(['PalmTree_1', 'Rock_1', 'Rock_3'])
            scale = random.uniform(2, 4)
        elif h < 0.5:
            asset_choice = random.choice(['CommonTree_1', 'Bush_1', 'Grass', 'Wheat', 'Plant_1'])
            scale = random.uniform(1.5, 3)
        elif h < 0.7:
            asset_choice = random.choice(['BirchTree_1', 'BirchTree_2', 'BirchTree_3', 'BirchTree_4', 'BirchTree_5', 'BushBerries_1', 'Rock_Moss_2', 'Grass_2'])
            scale = random.uniform(2, 4)
        else:
            asset_choice = random.choice(['Rock_4', 'TreeStump', 'Rock_Moss_2'])
            scale = random.uniform(2, 3)

        Entity(
            model=asset_models[asset_choice],
            position=(world_x, world_y, world_z),
            scale=scale,
            rotation_y=random.uniform(0, 360)
        )


Sky()
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))

window.exit_button.visible = False

def input(key):
    if key == 'escape':
        application.quit()

# === Load heightmap ===
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
heightmap = np.load(os.path.join(CURRENT_DIR, 'heightMap.npy'))
heightmap = (heightmap - np.min(heightmap)) / (np.max(heightmap) - np.min(heightmap))

print(f"Heightmap min: {np.min(heightmap)}, max: {np.max(heightmap)}")


rows, cols = heightmap.shape

# === Color logic ===
def get_color_by_height(h):
    if h < 0.2: return color.rgb(0, 0, 128)          # more water (deep + shallow)
    elif h < 0.38: return color.rgb(0, 77, 153)       # shallow water / beach
    elif h < 0.4: return color.rgb(230, 204, 153)    # beach
    elif h < 0.48: return color.rgb(51, 153, 51)      # plains
    elif h < 0.75: return color.rgb(153, 204, 102)   # hills
    elif h < 0.9: return color.rgb(128, 128, 128)    # mountain
    else: return color.white                         # snow peak
                        # snow peak


# === Generate mesh ===
def create_terrain(heightmap):
    verts = []
    tris = []
    colors = []

    for x in range(rows):
        for y in range(cols):
            h = heightmap[x][y]
            verts.append(Vec3(x, h * 20, y))
            colors.append(get_color_by_height(h))

    for x in range(rows - 1):
        for y in range(cols - 1):
            i = x * cols + y
            tris += [i, i + cols, i + 1]
            tris += [i + 1, i + cols, i + cols + 1]

    mesh = Mesh(vertices=verts, triangles=tris, colors=colors, mode='triangle', static=True)
    SCALE_XZ = 500  # Try 5 or bigger if you want vast lands
    SCALE_Y = 100   # Keep vertical realistic
    return Entity(model=mesh, scale=(SCALE_XZ, SCALE_Y, SCALE_XZ), collider=None)


terrain = create_terrain(heightmap)
place_assets(heightmap, terrain)


# === Flying camera ===
class FlyCam(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.camera_pivot = Entity(parent=self, y=2)
        camera.parent = self.camera_pivot
        camera.position = (0, 0, 0)
        camera.rotation = (0, 0, 0)
        mouse.locked = True
        self.speed = 500  # 🔹 NEW: fast enough for 100x scale


    def update(self):
        SENSITIVITY = 10
        self.rotation_y += mouse.velocity[0] * SENSITIVITY
        self.camera_pivot.rotation_x -= mouse.velocity[1] * SENSITIVITY
        self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -90, 90)

        direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s']) +
            self.right * (held_keys['d'] - held_keys['a']) +
            self.up * (held_keys['e'] - held_keys['q'])
        ).normalized()

        self.position += direction * time.dt * self.speed

def find_plain_start(heightmap):
    rows, cols = heightmap.shape
    center_x = rows // 2
    center_y = cols // 2
    search_radius = min(rows, cols) // 4  # Search around center
    
    best_pos = (center_x, center_y)
    min_dist = float('inf')
    
    for x in range(center_x - search_radius, center_x + search_radius):
        for y in range(center_y - search_radius, center_y + search_radius):
            if 0 <= x < rows and 0 <= y < cols:
                h = heightmap[x, y]
                if 0.48 < h < 0.75:  # Plain biome range (tune as per your setup)
                    dist = (x - center_x)**2 + (y - center_y)**2
                    if dist < min_dist:
                        min_dist = dist
                        best_pos = (x, y)
    
    return best_pos

# === Spawn camera ===
start_x = (rows * 0.5) * 0.5
start_y = 30
start_z = (cols * 0.5) * 0.5
flycam = FlyCam(position=(start_x, start_y, start_z))


app.run()
