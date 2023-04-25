""" Get the photograph of the particle field
Edited according to the MICROSIG written by Rossy
2022-11-24 Rewritten by Dong Zhao
"""
from os import path

import numpy as np
import cv2
import imageio
import matplotlib.pyplot as plt
from refRoutines import *

"""Settings begin here"""
mic = {'magnification': 10,
       'numericalAperture': 0.3,
       'focalLength': 350,
       'nMedium': 1,  # 介质折射率
       'nLens': 1.5,  # 透镜折射率
       'pixelSize': 6.5,
       'pixelDimX': 1024,
       'pixelDimY': 1024,
       'backgroundMean': 500,
       'backgroundNoise': 0,
       'pointsPerPixel': 40,
       'numRays': 1000,  # 每个点的光线数
       'gain': 1,
       'cylFocalLength': 0
       }  # 字典结构，本显微结构主要参数

rk = mic['focalLength'] * (mic['nLens'] / mic['nMedium'] - 1) * 2  # 透镜曲率半径

diameter = 2  # the diameter of the particle is about 2 mu
""" Only the uniformed particles are taken account"""
numPoints = np.round(mic['pointsPerPixel'] * 2 * np.pi * (diameter * mic['magnification'] / mic['pixelSize']) ** 2)
vec0 = create_particle(diameter, int(numPoints), Nr=mic['numRays'])  # 物面四矢量
lensRadius = (np.tan(np.arcsin(mic['numericalAperture'])) *
              (1 + 1 / mic['magnification']) * mic['focalLength'])  # 透镜曲率半径

di = mic['focalLength'] * (mic['magnification'] + 1)  # 像距
df = mic['focalLength'] * (1 / mic['magnification'] + 1)  # 聚焦像对应物距

""" Get the coordinates """
xPos = np.linspace(100, 900, 10)  # 根据1024设置
yPos = xPos
# zPos = np.array([0])
zPos = np.arange(10, -61, -10)  # 纵向离焦距离

n1 = 0
for z in range(1, 2):
    n1 = n1 + 1
    """For each z, output an image"""
    filePathXML = '/home/w/yolov5-master/data/Annotations/'
    filePathImg = '/home/w/yolov5-master/data/images/'
    file = open(filePathXML + str(n1) + '.xml', "w")
    file.write("""<?xml version="1.0" ?>
<annotation>
<folder>{folder}</folder>
<filename>{fileName}</filename>
<path>{path}</path>
<source>
    <database>Unknown</database>
</source>
<size>
    <width>1024</width>
    <height>1024</height>
    <depth>{depth}</depth>
</size>
    
<segmented>0</segmented>
""".format(
        folder='zxl',
        fileName=str(n1) + '.jpg',
        path='/home/w/zxl/' + str(n1) + '.jpg',
        depth=n1
    ))
    Image = np.zeros((mic['pixelDimY'], mic['pixelDimX']))
    z1 = 15 # np.random.choice(zPos, 1).item()
    vec3 = singleParImg(di, df, z1, vec0,lensRadius, rk, mic['nMedium'], mic['nLens'])
    img0 = np.zeros((mic['pixelDimY'], mic['pixelDimX']))
    for x in xPos:
        for y in yPos:
            # z1 = np.random.choice(zPos, 1).item()
            # z1 = -15
            # vec3 = singleParImg(di, df, z1, vec0, lensRadius, rk, mic['nMedium'], mic['nLens'], )
            X = np.round(vec3[0, :] / mic['pixelSize'] + x)
            rx = np.ceil((X.max() - X.min()) / 2)
            Y = np.round((vec3[1, :] / mic['pixelSize'] + y))
            ry = np.ceil((Y.max() - Y.min()) / 2)
            """ 向xml中输入数据 """
            xmin = max(int(x - rx), 0)
            ymin = max(int(y - ry), 0)
            xmax = min(int(x + rx), mic['pixelDimX'] - 1)
            ymax = min(int(y + ry), mic['pixelDimY'] - 1)
            ind = np.all([X >= 0, X < mic['pixelDimX'], Y >= 0, Y < mic['pixelDimY'],
                          X.imag == 0, Y.imag == 0], axis=0)

            """count the number of rays in each pixel"""
            countXY = np.sort(Y[ind] + (X[ind]) * mic['pixelDimY'])
            indi, ia = np.unique(countXY, return_index=True)
            nCounts = np.hstack((ia[1:], countXY.size + 1)) - ia
            img = np.zeros((mic['pixelDimY'], mic['pixelDimX']))
            imgFr = img.flatten("F")
            imgFr[indi.astype(int) - 1] = nCounts
            img = imgFr.reshape((mic['pixelDimY'], mic['pixelDimX']), order='F')

            img[ymin:ymax, xmin] = 2000
            img[ymin:ymax, xmax] = 2000
            img[ymin, xmin:xmax] = 2000
            img[ymax, xmin:xmax] = 2000

            img0 = img + img0

            file.write("""   <object>
    <name>depth:{depth}</name>
    <pose>Unspecified</pose>
    <truncated>0</truncated>
    <difficult>0</difficult>
    <bndbox>
        <xmin>{xmin}</xmin>
        <ymin>{ymin}</ymin>
        <xmax>{xmax}</xmax>
        <ymax>{ymax}</ymax>
    </bndbox>
</object>
 """.format(
                depth=z1,
                xmin=xmin,
                ymin=ymin,
                xmax=xmax,
                ymax=ymax
            ))
    file.write("\n")
    file.write('''</annotation>''')
    file.close()

    img0 = img0 * mic['gain']
    img0 = img0 + mic['backgroundMean']
    img2 = np.log(1+img0/6000)
    img2 = img0
    plt.imsave(filePathImg+str(n1) + ".jpg", img2)
    print(str(z) + " completed\n")
    print(str(np.max(img0)) + "\n")

    # with open("C0000" + str(z) + ".txt", "w") as f:
    #     for n in range(0, mic['pixelDimY']):
    #         for m in range(0, mic['pixelDimX']):
    #             f.write(str(img0[n, m]) + "  ")
    #         f.write('\n')
    # f.close()
