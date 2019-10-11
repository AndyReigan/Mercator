import math

DatumEqRad = [6378137.0,
              6378137.0,
              6378137.0,
              6378135.0,
              6378160.0,
              6378245.0,
              6378206.4,
              6378388.0,
              6378388.0,
              6378249.1,
              6378206.4,
              6377563.4,
              6377397.2,
              6377276.3]
DatumFlat = [298.2572236,
             298.2572236,
             298.2572215,
             298.2597208,
             298.2497323,
             298.2997381,
             294.9786982,
             296.9993621,
             296.9993621,
             293.4660167,
             294.9786982,
             299.3247788,
             299.1527052,
             300.8021499]

Item = 0  # default
a = DatumEqRad[Item]  # equatorial radius (meters)
f = 1 / DatumFlat[Item]  # polar flattening
drad = math.pi / 180  # convert degrees to radians

# Mor constants, extracted from the function:
k0 = 0.9996  # scale on central meridian
b = a * (1 - f)  # polar axis
e = math.sqrt(1 - (b / a) * (b / a))  # eccentricity
e0 = e / math.sqrt(1 - e * e)  # called e' in reference
esq = (1 - (b / a) * (b / a))  # e² for use in expansions
e0sq = e * e / (1 - e * e)  # e0² — always even powers


def utmToLatLon(x, y, utmz, north):
    zcm = 3 + 6 * (utmz - 1) - 180  # central meredian of zone
    e1 = (1 - math.sqrt(1 - e * e)) / (1 + math.sqrt(1 - e * e))  # call e1 in USGS PP1395
    M0 = 0  # in case origin other than zero lat - not needed for standard UTM

    if north:
        M = M0 + y / k0
    else:
        M = M0 + (y - 10000000) / k0

    mu = M / (a * (1 - esq * (1 / 4 + esq * (3 / 64 + 5 * esq / 256))))
    phi1 = mu + e1 * (3 / 2 - 27 * e1 * e1 / 32) * math.sin(2 * mu) + e1 * e1 * (
            21 / 16 - 55 * e1 * e1 / 32) * math.sin(4 * mu)
    phi1 = phi1 + e1 * e1 * e1 * (math.sin(6 * mu) * 151 / 96 + e1 * math.sin(8 * mu) * 1097 / 512)

    C1 = e0sq * pow(math.cos(phi1), 2)
    T1 = math.pow(math.tan(phi1), 2)
    N1 = a / math.sqrt(1 - pow(e * math.sin(phi1), 2))
    R1 = N1 * (1 - e * e) / (1 - pow(e * math.sin(phi1), 2))
    D = (x - 500000) / (N1 * k0)
    phi = (D * D) * (1 / 2 - D * D * (5 + 3 * T1 + 10 * C1 - 4 * C1 * C1 - 9 * e0sq) / 24)
    phi = phi + pow(D, 6) * (61 + 90 * T1 + 298 * C1 + 45 * T1 * T1 - 252 * e0sq - 3 * C1 * C1) / 720
    phi = phi1 - (N1 * math.tan(phi1) / R1) * phi
    # Output Latitude:
    outLat = math.floor(1000000 * phi / drad) / 1000000

    lng = D * (1 + D * D * ((-1 - 2 * T1 - C1) / 6 + D * D * (
            5 - 2 * C1 + 28 * T1 - 3 * C1 * C1 + 8 * e0sq + 24 * T1 * T1) / 120)) / math.cos(phi1)
    lngd = zcm + lng / drad

    # Output Longitude:
    outLon = math.floor(1000000 * lngd) / 1000000

    return [outLat, outLon]
211
print(utmToLatLon(269417.13, 1751581.85, 32, True))