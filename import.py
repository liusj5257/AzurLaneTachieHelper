import os

import UnityPy
from PIL import Image
from UnityPy import Environment
from UnityPy.classes import Sprite, Texture2D
from UnityPy.enums import TextureFormat

from src.utility import check_dir

# for file in os.listdir("loadingbg_img"):
#     name, ext = file.split(".")
#     os.system(f"cd loadingbg_img && rename {file} {name[:-1]}.{ext}")

outdir = "AssetBundles/loadingbg"
check_dir(outdir)
for file in os.listdir("loadingbg"):
    env: Environment = UnityPy.load(os.path.join("loadingbg", file))
    mod = False
    for k, v in env.container.items():
        sprite: Sprite = v.read()
        if hasattr(sprite, 'm_RD'):
            tex2d: Texture2D = sprite.m_RD.texture.read()
        else:
            continue
        name = sprite.name
        img: Image.Image = sprite.image
        names = [f"{name}.png", f"{name}_jp.png", f"{name}_h.png"]
        src = None
        for n in names:
            path = os.path.join("loadingbg_img", n)
            if os.path.exists(path):
                src = path
                break

        if os.path.exists(src):
            print(src)
            img = Image.open(src)
            sprite.m_RD.textureRect.width *= 2
            sprite.m_RD.textureRect.height *= 2
            sprite.m_PixelsToUnits *=2
            sprite.m_Rect.width *= 2
            sprite.m_Rect.height *= 2
            tex2d.m_Width *= 2
            tex2d.m_Height *= 2
            tex2d.set_image(img, target_format=TextureFormat.RGBA32, in_cab=True)
            mod = True
        tex2d.save()
        sprite.save()
    if mod:
        print(f"[INFO] Packing: {os.path.join(outdir, file)}")
        with open(os.path.join(outdir, file), "wb") as f:
            f.write(env.file.save("lz4"))
