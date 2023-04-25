import numpy as np
import cv2
import imageio
import matplotlib.pyplot as plt

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

def getXYZ(numParLine, pixelDimX=1024, pixelDimY=1024):
    xPos = np.linspace(60, pixelDimX-60, 10)



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


def singleParImg(di, df, z, vec0,  lensRadius, rk, nMedium=1.0, nLens=1.5):
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
    th11 = np.arcsin(nMedium / nLens *
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
