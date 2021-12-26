from PIL import Image
from pathlib import Path


def combin_image(imageArr, targetName):
    imageFile = [Image.open(i) for i in imageArr]
    width = imageFile[0].width
    target_height = 0
    for i in imageFile:
        target_height += i.height
    hiddenArr = [
        index
        for [index, image] in enumerate(imageFile)
        if 0 != index and index != len(imageFile) - 1
    ]
    target_height+= -50*len(hiddenArr)

    targetFile = Image.new("RGB", (width, target_height))

    lastHeight = 0
    for [index, image] in enumerate(imageFile):
        if index in hiddenArr:
            lastHeight = lastHeight - 50  # 50是uplot,x轴坐标的常量
        targetFile.paste(image, (0, lastHeight, image.width, lastHeight + image.height))
        targetFile.save(targetName)
        lastHeight += image.height
        



if __name__ == "__main__":
    storeIdx = 14
    targetName = f"all_{storeIdx}.png"
    imageArr = [
        i for i in Path("./image").glob(f"*_{storeIdx }.png") if i.name != targetName
    ]

    combin_image(imageArr, targetName)
