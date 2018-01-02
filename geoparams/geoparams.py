# -*- coding: utf-8 -*-
# Filename: geoparams.py

"""
Geo parameters calculation. Include local Earth radius, Earth rotatoin rate,
local gravity.
Created on 2017-09-12
@author: dongxiaoguang
"""

# import
import math
import numpy as np
#import scipy.linalg

# global
VERSION = '1.0'
GM = 3.986004418e14                 # m3/(s2)
Re = 6378137                        # m
FLATTENING = 0.00335281066475       # Earth flattening, f = (a-b)/a
ECCENTRICITY = 0.0818191908426215   # Earth eccentricy, e2 = 2*f-f^2
E_SQR = 0.00669437999014            # squared eccentricity
W_IE = 7292115e-11                  # Earth's rotation rate

def geo_param(pos):
    """
    Calculate local radius and gravity given the [Lat, Lon, Alt]
    Local radius include meridian radius rm and normal radius rn.
    Args:
        pos: [Lat, Lon, Alt], rad, m
    Returns:
        rm: meridian radius, m
        rn: normal radius, m
        g: gravity, m/s/s
        sl: sin(Lat)
        cl: cos(lat)
        w_ie: Earth's rotation rate w.r.t the inertial frame, rad/s
    """
    # some constants
    normal_gravity = 9.7803253359
    k = 0.00193185265241        # WGS-84 gravity model constant. For more details, refer to
                                # https://en.wikipedia.org/wiki/Gravity_of_Earth
    m = 0.00344978650684        # m = w*w*a*a*b/GM
    # calc
    sl = math.sin(pos[0])
    cl = math.cos(pos[0])
    sl_sqr = sl * sl
    h = pos[2]
    rm = (Re*(1 - E_SQR)) / (math.sqrt(1.0 - E_SQR*sl_sqr) * (1.0 - E_SQR*sl_sqr))
    rn = Re / (math.sqrt(1.0 - E_SQR*sl_sqr))
    g1 = normal_gravity * (1 + k*sl_sqr) / math.sqrt(1.0 - E_SQR*sl_sqr)
    g = g1 * (1.0 - (2.0/Re) * (1.0 + FLATTENING + m - 2.0*FLATTENING*sl_sqr)*h + 3.0*h*h/Re/Re)
    return rm, rn, g, sl, cl, W_IE

def earth_radius(lat):
    """
    Calculate Earth meridian radius and normal radius.
    Args:
        lat: Latitude, rad
    Returns:
        rm: meridian radius, m
        rn: normal radius, m
    """
    sl = math.sin(lat)
    sl_sqr = sl * sl
    rm = (Re*(1 - E_SQR)) / (math.sqrt(1.0 - E_SQR*sl_sqr) * (1.0 - E_SQR*sl_sqr))
    rn = Re / (math.sqrt(1.0 - E_SQR*sl_sqr))
    return rm, rn

def lla2xyz(lla):
    '''
    [Lat Lon Alt] position to xyz position
    Args:
        lla: [Lat, Lon, Alt], [rad, rad, meter], numpy array of size (3,)
    return:
        [x, y, z], [m, m, m], numpy array of size (3,)
    '''
    sl = math.sin(lla[0])
    cl = math.cos(lla[0])
    sl_sqr = sl * sl

    r = Re / math.sqrt(1.0 - E_SQR*sl_sqr)
    rho = (r + lla[2]) * cl
    x = rho * math.cos(lla[1])
    y = rho * math.sin(lla[1])
    z = (r*(1.0-E_SQR) + lla[2]) * sl

    return np.array([x, y, z])
