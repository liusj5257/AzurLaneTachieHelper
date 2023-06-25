import os
import pprint
from src.AssetManager import AssetManager
from src.DecodeHelper import DecodeHelper
from src.EncodeHelper import EncodeHelper


file = 'test/dafeng'

asset_manager = AssetManager()
decoder = DecodeHelper(asset_manager)
encoder = EncodeHelper(asset_manager)

asset_manager.analyze(file)
print(asset_manager.metas)
print("[INFO] Dependencies:", asset_manager.deps)
num_deps = len(asset_manager.deps)
for i, x in enumerate(asset_manager.deps):
    path = os.path.join(os.path.dirname(file) + "/", x)
    if os.path.exists(path):
        print("[INFO] Discovered:", path)
        asset_manager.extract(x, path)

paintingface = "paintingface/" + os.path.basename(file).strip("_n")
path = os.path.join(os.path.dirname(file) + "/", paintingface)
if os.path.exists(path):
    asset_manager.extract(x, path, True)
dir='test/output'
decoder.exec(dir + "/")
