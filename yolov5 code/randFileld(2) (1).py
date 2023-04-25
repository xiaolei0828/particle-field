""" To get the particle filed with random positions
    2022-11-29 Dong Zhao
"""
from refRoutines import *

""" Basic settings begin here for the same particles"""
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
"""To accelerate the process """
vecN = {}  # 定义字典元素，存储不同z值下的数据
rxN = {}
ryN = {}
vec0 = create_particle(diameter, int(numPoints), Nr=mic['numRays'])  # 物面四矢量
zPos = np.arange(30, -61, -15)  # 纵向离焦距离
# zPos = np.arange(-20, -31, -10)
for z in zPos:
    vec3 = singleParImg(di, df, z, vec0, lensRadius, rk, mic['nMedium'], mic['nLens'])
    vecN[z] = vec3
    X = np.round(vec3[0, :] / mic['pixelSize'])
    rx = np.ceil((X.max() - X.min()) / 2)
    # if z >= -20:
    #     rx = rx * (1 - (20 + z) / 50)
    Y = np.round((vec3[1, :] / mic['pixelSize']))
    ry = np.ceil((Y.max() - Y.min()) / 2)
    # if z >= -20:
    #     ry = ry * (1 - (20 + z) / 50)
    rxN[z] = rx
    ryN[z] = ry

for n1 in range(1, 5):
    numParticles = np.random.randint(1, 100)
    """For each n1, output an image"""
    filePathXML = 'home/w/yolov5-master/data/Annotations/'
    filePathImg = 'home/w/yolov5-master/data/images/'
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
    img0 = np.zeros((mic['pixelDimY'], mic['pixelDimX']))
    m = 0
    for m in range(0, numParticles):
        z1 = np.random.choice(zPos, 1).item()
        vec3 = vecN[z1]
        m = m + 1
        x = np.random.randint(60, mic['pixelDimX'] - 60)
        y = np.random.randint(60, mic['pixelDimY'] - 60)

        X = np.round(vec3[0, :] / mic['pixelSize'] + x)
        # rx = np.ceil((X.max() - X.min()) / 2)
        Y = np.round((vec3[1, :] / mic['pixelSize'] + y))
        # ry = np.ceil((Y.max() - Y.min()) / 2)
        rx = rxN[z1]
        ry = ryN[z1]
        """ 向xml中输入数据 """
        xmin = max(int(x - rx), 0)
        ymin = max(int(y - ry), 0)
        xmax = min(int(x + rx), mic['pixelDimX'] - 1)
        ymax = min(int(y + ry), mic['pixelDimY'] - 1)

        ind = np.all([X >= 0, X < mic['pixelDimX'],
                      Y >= 0, Y < mic['pixelDimY'], X.imag == 0, Y.imag == 0], axis=0)

        """count the number of rays in each pixel"""
        countXY = np.sort(Y[ind] + (X[ind]) * mic['pixelDimY'])
        indi, ia = np.unique(countXY, return_index=True)
        nCounts = np.hstack((ia[1:], countXY.size + 1)) - ia
        img = np.zeros((mic['pixelDimY'], mic['pixelDimX']))
        imgFr = img.flatten("F")
        imgFr[indi.astype(int) - 1] = nCounts
        img = imgFr.reshape((mic['pixelDimY'], mic['pixelDimX']), order='F')

        # img[ymin:ymax, xmin] = 2000
        # img[ymin:ymax, xmax] = 2000
        # img[ymin, xmin:xmax] = 2000
        # img[ymax, xmin:xmax] = 2000

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

    print(numParticles)
    img0 = img0 * mic['gain']
    # img0 = img0 + mic['backgroundMean']
    # img2 = np.log(1+ img0/5000)
    # img2[img2 == img2.min()] = 0
    img2 = np.log(1+img0)
    plt.imsave(filePathImg + str(n1) + ".jpg", img2, cmap='gray', vmax=9)
    print(str(n1) + " completed\n")
    print(str(np.max(img0)) + "\n")
    # plt.imshow(img2)
