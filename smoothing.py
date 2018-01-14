import numpy as np

from road import Road


def max_smoothing(road: Road, maxh: int):
    #maxh = 7
    while max(road) > maxh:
        for i in range(road.size):
            if road[i] > maxh:
                for n in range(1, road.size):
                    right = (i + n) % road.size
                    left = (i - n) % road.size
                    rightr = road[right]
                    leftr = road[left]
                    if rightr < leftr and rightr < maxh:
                        road.add_grain(right)
                        road.remove_grain(i)
                        break
                    elif rightr > leftr and leftr < maxh:
                        road.add_grain(left)
                        road.remove_grain(i)
                        break
                    elif rightr == leftr and rightr < maxh:
                        uniran = np.random.uniform(0, 1)
                        if uniran >= 0.5:
                            road.add_grain(right)
                            road.remove_grain(i)
                            break
                        else:
                            road.add_grain(left)
                            road.remove_grain(i)
                            break


def slope_smoothing(road: Road):
    for i in range(road.size):
        i2 = (i+1) % road.size
        height1 = road[i]
        height2 = road[i2]
        diff = height1 - height2
        if diff > 1:
            road.add_grain(i2)
            road.remove_grain(i)
        elif diff < -1:
            road.add_grain(i)
            road.remove_grain(i2)

def cellular_automata_smoothing(road: Road, iterations: int,
                                D: float, gamma: float,
                                v: float, S_c: int, d: int ):
    #FOR US d = 1? width of columns

    N = road.size
    R = road.piles.astype(float)
    h = np.maximum(R-2,0)

    #h = road.piles.astype(float)
    #R = np.maximum(h-2,0)

    dR = np.full(N, 0, dtype=np.float)
    dh = np.full(N, 0, dtype=np.float)

    for i in range(N):
        # im = (i-1) % N
        ip = (i + 1) % N
        dh[i] = (h[ip] - h[i]) / d
        dR[i] = (R[ip] - R[i]) / d

    for iter in range(iterations):
        for i in range(N):
            #im = (i-1) % N
            ip = (i+1) % N

            dh[i] = (h[ip]-h[i])/d
            dR[i] = (R[ip] - R[i])/d

            R[i] = R[i] + (-v*R[i] + D*dR[i]) - R[i]*gamma*(dh[i]-abs(S_c))
            h[i] = h[i] + R[i]*gamma*(dh[i] - abs(S_c))
            R[ip] = R[ip] - (-v*R[i] + D*dR[i])

    road.piles = np.round(R).astype(int)