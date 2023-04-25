""" Get the photograph of the particle field
Edited according to the MICROSIG written by Rossy
2022-11-24 Rewritten by Dong Zhao
"""
from os import path

import numpy as np
import cv2
import imageio


def spiral_sphere(N):
    """get a sphere with a given number of points
    copy from Rossy's routine
    """
    gr = (1 + np.sqrt(5)) / 2  # golden ratio
    ga = 2 * np.pi * (1 - 1 / gr)  # golden angle

    ind_p = np.arange(0, N)  # particle (i.e., point sample) index
    lat = np.arccos(1 - 2 * ind_p / (
            N - 1))  # latitude is defined so that particle index is proportional to surface area between 0 and lat
    lon = ind_p * ga  # position particles at even intervals along longitude

    # Convert from spherical to Cartesian co-ordinates
    x = np.sin(lat) * np.cos(lon)
    y = np.sin(lat) * np.sin(lon)
    z = np.cos(lat)
    V = np.vstack((x, y, z))

    return V


def create_particle(D, Ns, Nr):
    """ Get particles with a given diameter
     D: diameter
     Ns: points per particle
     Nr: Number of rays per point
     """
    R = D / 2

    V = spiral_sphere(Ns)
    V[0:2, V[0, :] > 0] = -V[0:2, V[0, :] > 0]
    x = R * V[0, :]
    y = R * V[1, :]
    z = R * V[2, :]

    V0 = spiral_sphere(Nr + 2)
    V0 = V0[:, 1:-1]
    u = np.tile(x, (Nr, 1))
    v = np.tile(y, (Nr, 1))
    s = u * 0
    t = u * 0

    phs = np.random.uniform(-np.pi, np.pi, z.size)
    cs = np.cos(phs)
    sn = np.sin(phs)
    for k in range(0, Ns):
        Rot = np.array([[cs[k], -sn[k], 0],
                        [sn[k], cs[k], 0],
                        [0, 0, 1]])
        Vr = Rot @ V0
        Vr[0, :] = -abs(Vr[0, :])
        s[:, k] = Vr[1, :] / Vr[0, :]
        t[:, k] = Vr[2, :] / Vr[0, :]
        u[:, k] = y[k] - s[:, k] * x[k]
        v[:, k] = z[k] - t[:, k] * x[k]

    xp = np.vstack((u.flatten('F'), v.flatten('F'),
                    s.flatten('F'), t.flatten('F')))

    return xp


def singleParImg(di, df, z, vec0, nMedium, nLens):
    """
    :param di: the distance between the object and the lens
    :param df: the distance between the focused image and the lens with di
    :param z: the distance off df
    :param vec0: a given spherical surface with a set of 4-D vectors (position and rays direction)
    :param nMedium: the refractive index of the medium. We set 1 for the air
    :param nLens: the refractive index of the lens. We set 1.5 for the lens
    :return: vec3, the 4-D vectors at the camera surface
    """
    do = z + df  # 物距
    """ Linear transformation from the object plane to the lens plane """
    T2 = np.array([[1, 0, do, 0],
                   [0, 1, 0, do],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    vec1 = np.linalg.inv(T2) @ vec0
    """
                 T2 的逆 = np.array([[1, 0, -di, 0],
                    [0, 1, 0, -di],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
     """

    """ Remove rays outside the lens aperture"""
    ind = vec1[0, :] ** 2 + vec1[1, :] ** 2 <= lensRadius ** 2
    vec1 = vec1[:, ind]

    """ Transformation of the light field with the lens spherical surface"""
    u = vec1[0, :]
    v = vec1[1, :]
    s = vec1[2, :]
    t = vec1[3, :]  # 四位坐标，uv表示位置，st表示方向

    dum = u * 0
    """ Rays before lens """
    vec = np.vstack((1 + dum, s, t))  # 光线的方向， s 是光线方向和x轴夹角的正切， t是其和y轴方向的正切
    vec = vec / np.tile(np.sqrt(sum(vec ** 2)), (3, 1))

    """ Normal vector to the lens surface"""
    vec_n = np.vstack((rk + dum, u, v))
    vec_n = vec_n / np.tile(np.sqrt(sum(vec_n ** 2)), (3, 1))

    """ Tangent vector on the lens surface"""
    vec_t = np.cross(vec, vec_n, axisa=0, axisb=0)
    vec_t = np.cross(vec_t, vec_n, axisa=1, axisb=0).transpose()
    vec_t = vec_t / np.tile(np.sqrt(sum(vec_t ** 2)), (3, 1))

    """ Angle after Snell law"""
    vn = np.sum(vec * vec_n, axis=0)  # dot product! 光线矢量法向分量
    vt = np.sum(vec * vec_t, axis=0)  # dot product! 光线矢量切向分量
    th11 = np.arcsin(mic['nMedium'] / mic['nLens'] *
                     np.sin(np.arctan(vt / vn)))

    """ new ray inside the lens"""
    vec_in = (vec_n * np.tile(np.cos(th11), (3, 1)) +
              vec_t * np.tile(np.sin(th11), (3, 1)))
    vec_in = vec_in / np.tile(vec_in[0, :], (3, 1))

    """ Normal-vector on the back surface of the lens"""
    vec_nB = np.vstack((vec_n[0, :], -vec_n[1:, :]))
    """ Tangent-vector on the back surface of the lens"""
    vec_tB = np.cross(vec_in, vec_nB, axisa=0, axisb=0)
    vec_tB = np.cross(vec_tB, vec_nB, axisa=1, axisb=0).transpose()
    vec_tB = vec_tB / np.tile(np.sqrt(sum(vec_tB ** 2)), (3, 1))

    """ Angle after Snell law correction at the Back surface of the lens"""
    vnB = np.sum(vec_in * vec_nB, axis=0)
    vtB = np.sum(vec_in * vec_tB, axis=0)
    th_B = np.arcsin(nLens / nMedium * np.sin(np.arctan(vtB / vnB)))
    """ ray-vector outside the lens"""
    vecB = (vec_nB * np.tile(np.cos(th_B), (3, 1)) +
            vec_tB * np.tile(np.sin(th_B), (3, 1)))
    vecB = vecB / np.tile(vecB[0, :], (3, 1))

    """ light field after the spherical lens"""
    vec2 = vec1  # 此处采用薄透镜假设，位移不变，但方向变化
    vec2[2, :] = vecB[1, :]
    vec2[3, :] = vecB[2, :]

    """ From the lens plane to the camera plane """
    T1 = np.array([[1, 0, di, 0],
                   [0, 1, 0, di],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    vec3 = np.linalg.inv(T1) @ vec2
    return vec3


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

""" Get the coordinates """

numParticles = 100  # 设定所产生的粒子数
xPos = np.linspace(62, 962, 10)  # 962 根据1024设置
yPos = xPos
zPos = np.array([0])
zPos = np.arange(0, -101, -10)  # 纵向离焦距离
rk = mic['focalLength'] * (mic['nLens'] / mic['nMedium'] - 1) * 2  # 透镜曲率半径

diameter = 2  # the diameter of the particle is about 2 miu
""" Only the uniformed particles are taken account"""
numPoints = np.round(mic['pointsPerPixel'] * 2 * np.pi * (diameter * mic['magnification'] / mic['pixelSize']) ** 2)
vec0 = create_particle(diameter, int(numPoints), Nr=mic['numRays'])  # 物面四矢量
lensRadius = (np.tan(np.arcsin(mic['numericalAperture'])) *
              (1 + 1 / mic['magnification']) * mic['focalLength'])  # 透镜曲率半径

di = mic['focalLength'] * (mic['magnification'] + 1)  # 像距
df = mic['focalLength'] * (1 / mic['magnification'] + 1)  # 聚焦像对应物距

for z in zPos:
    """For each z, output an image"""
    file = open(str(z) + '.xml', "w")
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
        fileName=str(z) + '.jpg',
        path='/home/w/zxl/' + str(z) + '.jpg',
        depth=z
    ))
    Image = np.zeros((mic['pixelDimY'], mic['pixelDimX']))
    vec3 = singleParImg(di, df, z, vec0, mic['nMedium'], mic['nLens'])
    img0 = np.zeros((mic['pixelDimY'], mic['pixelDimX']))
    for x in xPos:
        for y in yPos:
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
                depth=z,
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
    img2 = img0 / 4000 * 255
    cv2.imwrite(str(z) + ".jpg", img2)
    print(str(z) + "closed\n")
    print(str(np.max(img0))+"\n")

    # with open("C0000" + str(z) + ".txt", "w") as f:
    #     for n in range(0, mic['pixelDimY']):
    #         for m in range(0, mic['pixelDimX']):
    #             f.write(str(img0[n, m]) + "  ")
    #         f.write('\n')
    # f.close()
