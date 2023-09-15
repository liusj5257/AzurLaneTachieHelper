import os
import threading

import UnityPy
from PIL import Image
from UnityPy import Environment
from UnityPy.classes import Sprite, Texture2D, TextAsset
from UnityPy.enums import ClassIDType, TextureFormat

from src.utility import check_dir


def extract_textures(bundle: str, output_folder: str):
    check_dir(output_folder)
    env = UnityPy.load(os.path.join("tmp/src", bundle))
    for obj in env.objects:
        if obj.type == 28:
            texture = Texture2D(obj)
            data = texture.image
            save_path = f"{output_folder}/{texture.name}.png"
            print(f"Saving image to: {save_path}")
            data.save(save_path)


def import_texture(bundle: str, out_path: str, up=2):
    # choice = input("Enable compression (Y/N): ").lower()
    # tex_fmt = TextureFormat.ETC2_RGB if choice == "y" else TextureFormat.ASTC_RGB_5x5
    tex_fmt = TextureFormat.ETC2_RGBA8
    env: Environment = UnityPy.load(os.path.join("tmp/src", bundle))
    mod = False
    sprite = None
    for k, v in env.container.items():
        if v.type == ClassIDType.Sprite:
            sprite: Sprite = v.read()
            tex2d: Texture2D = sprite.m_RD.texture.read()
        elif v.type == ClassIDType.Texture2D:
            tex2d: Texture2D = v.read()
            file = os.path.join("tmp",'upimg','home',tex2d.name + f'.png')
            # print(file)
            if os.path.exists(file):
                # print('exists:',file)
                img = Image.open(file)
                w, h = img.size
                # img = img.resize((w // 4 * 4, h // 4 * 4))
                if sprite is not None:
                    sprite.m_Rect.width, sprite.m_Rect.height = img.size
                    sprite.m_RD.textureRect.width, sprite.m_RD.textureRect.height = img.size
                    sprite.save()
                tex2d.m_Width, tex2d.m_Height = img.size
                tex2d.set_image(img, target_format=tex_fmt)
                tex2d.m_TextureSettings.m_FilterMode = 1
                tex2d.m_TextureSettings.m_Aniso = 1
                tex2d.save()
                # print(f"[INFO] Import")
                mod = True
        elif v.type == ClassIDType.TextAsset:
            asset: TextAsset = v.read()
            if 'atlas' in asset.m_Name:
                lines = asset.text.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('size:'):
                        size = line.split(':')[-1].strip()
                        width, height = map(int, size.split(','))
                        width *= up
                        height *= up
                        lines[i] = f'size: {width},{height}'
                    elif line.startswith('  size:'):
                        size = line.split(':')[-1].strip()
                        width, height = map(int, size.split(','))
                        width *= up
                        height *= up
                        lines[i] = f'  size: {width},{height}'
                    elif line.startswith('  orig:'):
                        orig = line.split(':')[-1].strip()
                        width, height = map(int, orig.split(','))
                        width *= up
                        height *= up
                        lines[i] = f'  orig: {width},{height}'
                    elif line.startswith('  xy:'):
                        xy = line.split(':')[-1].strip()
                        x, y = map(int, xy.split(','))
                        x *= up
                        y *= up
                        lines[i] = f'  xy: {x},{y}'
                    elif line.startswith('  offset:'):
                        offset = line.split(':')[-1].strip()
                        x, y = map(int, offset.split(','))
                        x *= up
                        y *= up
                        lines[i] = f'  offset: {x},{y}'
                    # elif line.startswith('filter:'):
                    #     lines[i] = f'filter: Trilinear,Trilinear'
                asset.text = '\n'.join(lines)
                # print(asset.text)
                asset.save()
        else:
            continue
    if mod:
        check_dir(out_path)
        with open(f'{out_path}/{bundle}', "wb") as f:
            f.write(env.file.save("original"))
            print(f'{bundle}')
    else:
        print(f'{bundle} no mod')


def mult_extra():
    outdir = "tmp/img"
    check_dir(outdir)
    tasks = [threading.Thread(target=extract_textures, args=(_, outdir))
             for _ in os.listdir("tmp/src")]
    [_.start() for _ in tasks]
    [_.join() for _ in tasks]

    # os.system("pause")


def mult_import():
    outdir = "tmp/mod"
    check_dir(outdir)
    tasks = [threading.Thread(target=import_texture, args=(_, outdir, 2))
             for _ in os.listdir("tmp/src")]
    [_.start() for _ in tasks]
    [_.join() for _ in tasks]

    # os.system("pause")


# 示例用法
# extract_textures(
#     "home/assets-_mx-spinelobbies-wakamo_home-_mxdependency-2022-08-24_assets_all_2934114723.bundle", "tmp/img/home")

import_texture(
    "home/assets-_mx-spinelobbies-wakamo_home-_mxdependency-2022-08-24_assets_all_2934114723.bundle", "tmp/mod", 2)




# mult_import()
