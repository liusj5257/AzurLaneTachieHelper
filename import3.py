from copy import copy
import os
import random
import threading
import UnityPy
from PIL import Image
from UnityPy import Environment
from UnityPy.classes import Sprite, Texture2D
from UnityPy.enums import ClassIDType, TextureFormat


def exec(ab: str, tex_fmt: TextureFormat, img: str, OutPath: str, Up: int = 4):
    env = UnityPy.load(ab)
    mod = False
    img_name = os.path.splitext(os.path.basename(img))[0]
    if 1:
        for obj in env.objects:
            if obj.type.name == "AssetBundle":
                tree = obj.read_typetree()
                for i in range(len(tree['m_Container'])):
                    # 获取旧的元组
                    old_tuple = tree['m_Container'][i]
                    # 创建一个新的元组，替换第一个元素
                    new_tuple = (old_tuple[0].replace(
                        'bg_1', img_name), old_tuple[1])
                    # 替换原来的元组
                    tree['m_Container'][i] = new_tuple
                # 将字符串中的bg_1替换
                # print(tree['m_PreloadTable'],tree['m_Container'])
                obj.save_typetree(tree)
        for k, v in env.container.items():
            if v.type == ClassIDType.Sprite:
                sprite: Sprite = v.read()
                tex2d: Texture2D = sprite.m_RD.texture.read()
            elif v.type == ClassIDType.Texture2D:
                tex2d: Texture2D = v.read()
            else:
                raise ValueError(v.type)
            Img = Image.open(img)
            Img = Img.resize((tex2d.m_Width*Up, tex2d.m_Height*Up))
            if sprite is not None:
                sprite.m_Rect.width, sprite.m_Rect.height = Img.size
                sprite.m_RD.textureRect.width, sprite.m_RD.textureRect.height = Img.size
                sprite.m_PixelsToUnits = 100*Up
                sprite.m_Name = img_name
                sprite.save()
            tex2d.m_Width, tex2d.m_Height = Img.size
            tex2d.set_image(Img, tex_fmt)
            tex2d.m_Name = img_name
            tex2d.save()
            tree = tex2d.read_typetree()
            # print(tree)
            mod = True
        if mod:
            with open(os.path.join(OutPath, img_name), "wb") as f:
                f.write(env.file.save("original"))
                print(img_name, 'done')


TempBgAsset = os.path.join(os.path.dirname(__file__), 'bg_1')
ImgPath = os.path.join(os.path.dirname(__file__),
                       'loadingbg_up/upscayl_realesrgan-x4plus-anime_x4')
OutPath = os.path.join(os.path.dirname(__file__), 'loadingbg_out')

# for img in os.listdir(ImgPath):
#     if img.endswith('.png'):
#         bg_num = img.split('.')[0]
#         num = int(bg_num.split('_')[1])
#         print(num)
#         exec(TempBgAsset, TextureFormat.RGB24,
#              os.path.join(ImgPath, img), OutPath)
tasks = [threading.Thread(target=exec, args=(TempBgAsset, TextureFormat.ASTC_RGBA_6x6, os.path.join(ImgPath, _), OutPath))
         for _ in os.listdir(ImgPath)]
[_.start() for _ in tasks]
[_.join() for _ in tasks]

# os.system("pause")
