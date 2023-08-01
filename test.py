import os
import threading

import UnityPy
from PIL import Image
from UnityPy import Environment
from UnityPy.classes import Sprite, Texture2D
from UnityPy.enums import ClassIDType, TextureFormat

from src.utility import check_dir

def extract_textures(bundle_path: str, output_folder: str):
    env = UnityPy.load(bundle_path)
    for obj in env.objects:
        print(f"Processing object: {obj}")
        if obj.type == 28:
            print(f"  Texture2D found")
            print(f"    name: {obj.name}")
            print(f"    type: {obj.type}")
            print(f"    path: {obj.path}")
            print(f"    file: {obj.file}")
            print(f"    size: {obj.size}")
            print(f"    hash: {obj.hash}")
            print(f"    compressed: {obj.compressed}")
            print(f"    compressed_size: {obj.compressed_size}")
            print(f"    compressed_hash: {obj.compressed_hash}")
            print(f"    compressed_type: {obj.compressed_type}")
            print(f"    compressed_ext: {obj.compressed_ext}")
            print(f"    compressed_path: {obj.compressed_path}")
            print(f"    compressed_file: {obj.compressed_file}")
            print(f"    image_path: {obj.image_path}")
            print(f"    image_file: {obj.image_file}")
            texture = Texture2D(obj)
            data = texture.image
            save_path = f"{output_folder}/{texture.name}.png"
            print(f"Saving image to: {save_path}")
            data.save(save_path)

def replace_texture(bundle_path: str, image_path: str):
    choice = input("Enable compression (Y/N): ").lower()
    tex_fmt = TextureFormat.ETC2_RGB if choice == "y" else TextureFormat.ARGB32
    env: Environment = UnityPy.load(os.path.join("tmp", bundle_path))
    mod=False
    sprite = None
    for k, v in env.container.items():
      if v.type == ClassIDType.Sprite:
          sprite: Sprite = v.read()
          tex2d: Texture2D = sprite.m_RD.texture.read()
      elif v.type == ClassIDType.Texture2D:
          tex2d: Texture2D = v.read()
      else:
          continue
      file = tex2d.name + '_2.png'
      print(file)
      if os.path.exists(os.path.join("tmp", file)):
        img = Image.open(os.path.join("tmp", file))
        w, h = img.size
        img = img.resize((w // 4 * 4, h // 4 * 4))
        if sprite is not None:
            sprite.m_Rect.width, sprite.m_Rect.height = img.size
            sprite.m_RD.textureRect.width, sprite.m_RD.textureRect.height = img.size
            sprite.save()
        tex2d.m_Width, tex2d.m_Height = img.size
        tex2d.set_image(img, target_format=tex_fmt)
        tex2d.save()
        print(f"[INFO] Import")
        mod = True
        break
        # for obj in env.objects:
        #     if obj.type == 28:
        #         mod=True
        #         texture = Texture2D(obj)
        #         print(f"Replacing texture: {texture.name}")
        #         texture.image = Image.open(image_path)
        #         print(texture.image)
        #         texture.save()
    if mod:
      with open('tmp/test', "wb") as f:
              f.write(env.file.save("original"))
# 示例用法
# extract_textures("tmp/assets-_mx-spinecharacters-ch0175_spr-_mxdependency-2023-01-10_assets_all_2702761377.bundle", "tmp")
replace_texture("assets-_mx-spinecharacters-ch0175_spr-_mxdependency-2023-01-10_assets_all_2702761377.bundle", "tmp/CH0175_spr_2.png")
