import os
from src.AssetManager import AssetManager
from src.DecodeHelper import DecodeHelper
from src.EncodeHelper import EncodeHelper
import multiprocessing as mp
import shutil
from src.utility import raw_name

asset_manager = AssetManager()
decoder = DecodeHelper(asset_manager)
encoder = EncodeHelper(asset_manager)
num_deps = len(asset_manager.deps)


def openMetadata(file: str, dst=''):
    __src_dir = file
    filename = os.path.basename(__src_dir)
    __dst_dir = (dst or 'test/output')+'/'+filename
    os.makedirs(__dst_dir, exist_ok=True)

    asset_manager.analyze(__src_dir)
    # print("[INFO] Metadata:", __src_dir)
    # print("[INFO] Dependencies:", [asset_manager.deps.keys()])


    decoder.exec(__dst_dir + "/")
    return __dst_dir


def movFile(src='test/painting'):
  __src_dir = src
  __dst_dir = os.path.dirname(os.path.abspath(__src_dir))
  moved_files = []
  for filename in os.listdir(__src_dir):
    # Check if the file name does not end with '_hx' or 'tex'
    if not filename.endswith('_hx') and not filename.endswith('tex'):
        # Construct the full path to the source and destination files
        # print(filename)
        src_path = os.path.join(__src_dir, filename)
        dst_path = os.path.join(__dst_dir, filename)

        # Move the file from the source to the destination
        shutil.copy(src_path, dst_path)
        moved_files.append(dst_path)
  return moved_files


def importPainting(src):
  paintingSrc = src+'/painting'
  paintingFiles = []
  for file in os.listdir(paintingSrc):
     paintingFiles.append(os.path.join(paintingSrc, file))
  if paintingFiles:
    # print("[INFO] Paintings:")
    # [print("      ", _) for _ in paintingFiles]
    for paintingFile in paintingFiles:
      if len(paintingFiles) > 0:
        asset_manager.load_painting(
            os.path.splitext(os.path.basename(paintingFile))[0], paintingFiles[0])


def importFace(src):
   dir=src+'/face'
   if dir:
      # print("[INFO] Paintingface folder:", dir)
      # print("[INFO] Paintingfaces:")
      asset_manager.load_face(dir)


# path = openMetadata('test/dafeng_h_n')





def main(filename):
    path = openMetadata(filename, 'D:/ClientExtract/CN/painting')
    # importPainting(path)
    # importFace(path)
    # path = encoder.exec('test' + "/")
    print('Done:',path)

if __name__ == '__main__':
    moved_files = movFile('C:/Users/LIU-S/Desktop/apk/AzurLaneTools/Assets/ClientAssets/CN/AssetBundles/painting')
    with mp.Pool(processes=mp.cpu_count()-1) as pool:
        for filename in moved_files:
            pool.apply_async(main, (filename,))
        # explicitly join pool
        # this causes the pool to wait for all asnyc tasks to complete
        pool.close()
        pool.join()