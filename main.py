import os
from src.AssetManager import AssetManager
from src.DecodeHelper import DecodeHelper
from src.EncodeHelper import EncodeHelper
import shutil
from src.utility import raw_name

asset_manager = AssetManager()
decoder = DecodeHelper(asset_manager)
encoder = EncodeHelper(asset_manager)
num_deps = len(asset_manager.deps)

def outputPng(file:str):
    __src_dir = file
    filename = os.path.basename(__src_dir)
    __dst_dir = f'test/output/{filename}'
    os.makedirs(__dst_dir, exist_ok=True)

    asset_manager.analyze(__src_dir)
    print(asset_manager.metas)
    print("[INFO] Dependencies:", asset_manager.deps)
    num_deps = len(asset_manager.deps)
    for i, x in enumerate(asset_manager.deps):
        path = os.path.join(os.path.dirname(__src_dir) + "/", x)
        if os.path.exists(path):
            print("[INFO] Discovered:", path)
            asset_manager.extract(x, path)
    paintingface = "paintingface/" + os.path.basename(__src_dir).strip("_n")
    path = os.path.join(os.path.dirname(__src_dir) + "/", paintingface)
    if os.path.exists(path):
        asset_manager.extract(x, path, True)
    decoder.exec(__dst_dir + "/")
    return __dst_dir
def movFile():
  __src_dir = 'test/painting'
  __dst_dir = 'test'
  moved_files = []
  for filename in os.listdir(__src_dir):
    # Check if the file name does not end with '_hx' or 'tex'
    if not filename.endswith('_hx') and not filename.endswith('tex'):
        # Construct the full path to the source and destination files
        print(filename)
        src_path = os.path.join(__src_dir, filename)
        dst_path = os.path.join(__dst_dir, filename)

        # Move the file from the source to the destination
        shutil.copy(src_path, dst_path)
        moved_files.append(dst_path)
  return moved_files

def importPng(src):
  paintingSrc = src+'/painting'
  paintingFiles = []
  for file in os.listdir(paintingSrc):
     paintingFiles.append(os.path.join(paintingSrc, file))
  if paintingFiles:
    print("[INFO] Paintings:")
    [print("      ", _) for _ in paintingFiles]

  #     for i in range(num_deps):
  #         name = raw_name(tReplacer.item(i, 0).text()).lower()
  #         match = [_ for _ in paintingFiles if name in _]
  #         if len(match) > 0:
  #             tReplacer.setItem(i, 1, QTableWidgetItem(match[0]))
  #             asset_manager.load_painting(name, match[0])


moved_files = movFile()
for filename in moved_files:
    importPng(outputPng(filename))
