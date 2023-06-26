import os

import numpy as np
from PIL import Image
from pytoshop.enums import ColorMode
from pytoshop.user import nested_layers

from .TextureHelper import TextureHelper


class DecodeHelper(TextureHelper):
    def exec(self, dir: str):
        painting = []
        for k, v in self.layers.items():
            if k != "face":
                sub = self.decode(v.mesh, v.tex, v.rawSpriteSize)
                full = Image.new("RGBA", self.size)
                full.paste(sub.resize(v.sizeDelta, Image.Resampling.LANCZOS), v.offset)
                painting += [self.ps_layer(full, k)]

        face = []
        for k, v in sorted(self.faces.items()):
            full = Image.new("RGBA", self.size)
            full.paste(v, self.face_layer.offset)
            face += [self.ps_layer(full, k, False)]

        layers = [
            nested_layers.Group(name="paintingface", layers=face, closed=False),
            nested_layers.Group(name="painting", layers=painting[::-1], closed=False),
        ]
        psd = nested_layers.nested_layers_to_psd(layers, color_mode=ColorMode.rgb)
        path = os.path.join(dir, self.name + ".psd")
        for layer in face:
            a = layer.channels[-1]
            r = layer.channels[0]
            g = layer.channels[1]
            b = layer.channels[2]
            data = np.dstack((r, g, b, a))
            img = Image.fromarray(data, mode='RGBA')
            os.makedirs(dir+'face',exist_ok=True)
            img.save(os.path.join(dir+'face', layer.name + '.png'))
        for layer in painting:
            a = layer.channels[-1]
            r = layer.channels[0]
            g = layer.channels[1]
            b = layer.channels[2]
            data = np.dstack((r, g, b, a))
            img = Image.fromarray(data, mode='RGBA')
            os.makedirs(dir+'painting', exist_ok=True)
            img.save(os.path.join(dir+'painting', layer.name + '.png'))

        with open(path, "wb") as f:
            psd.write(f)

        return path

    def decode(self, mesh: dict, enc: Image.Image, rss: tuple) -> Image.Image:
        dec = Image.new("RGBA", rss)

        v, vt, f = mesh.values()
        for _ in f:
            lb1, ru1 = self._measure(v[_])
            lb2, ru2 = self._measure(vt[_] * enc.size)

            dec.paste(enc.crop((*lb2, *ru2)), (*lb1,))

        return dec

    def _measure(self, data):
        lb = np.round(np.stack(data, -1).min(-1)).astype(np.int32)
        ru = np.round(np.stack(data, -1).max(-1)).astype(np.int32)
        return lb, ru

    def ps_layer(self, img: Image.Image, name: str, visible: bool = True) -> nested_layers.Layer:
        r, g, b, a = img.transpose(Image.FLIP_TOP_BOTTOM).split()
        channels = {i - 1: np.array(x) for i, x in enumerate([a, r, g, b])}
        w, h = img.size
        layer = nested_layers.Image(
            name=name,
            visible=visible,
            opacity=255,
            top=0,
            left=0,
            bottom=h,
            right=w,
            channels=channels,
        )
        return layer
