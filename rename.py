# 遍历当前文件夹下所有png图片
import os
import shutil
# path = "C:/Users/LIU-S/Pictures/azur/loadingbg"

ResPath = os.path.join(os.path.dirname(__file__), 'loadingbg')

NewPath = os.path.join(os.path.dirname(__file__), 'loadingbg_img')
if not os.path.exists(NewPath):
    os.mkdir(NewPath)
num = 0
for file in os.listdir(NewPath):
    print("num")
    if file.endswith('.png'):
        bg_ = file.split('.')[0]
        num = int(bg_.split('_')[1])
        print(num)
for root, dirs, files in os.walk(ResPath):
    i = num+1
    for file in files:
        if file.endswith(".png"):
            # 获取原文件名
            oldname = os.path.join(root, file)
            # 并将其重命名为“new/bg_序号.png”
            newname = os.path.join(NewPath, "bg_" + str(i) + ".png")
            # 重命名，如果已经存在则覆盖原文件
            shutil.copy2(oldname, newname)
            i += 1
