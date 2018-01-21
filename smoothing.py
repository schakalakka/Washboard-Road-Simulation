import numpy as np

from road import Road
from wheel import Wheel
from utils import print_road_surface
import random

#Idea: pass as maxh the current maximum height of the road
def wind_smoothing(road: Road, maxh: int):
    while max(road) > maxh:
        for i in range(road.size):
            if road[i] > maxh:
                temp_minimum=min(road)
                for j in range(road.size):
                    if road[j] == temp_minimum:
                        road.remove_grain(i)
                        road.add_grain(j)
                        break

def random_wind_smoothing(road: Road, maxh: int):
    while max(road) > maxh:
        for i in range(road.size):
            if road[i] > maxh:
                temp_minimum=min(road)
                temp_minimum_indices = np.where(road.piles == temp_minimum)
                chosen_index = np.random.choice(temp_minimum_indices[0])
                road.remove_grain(i)
                road.add_grain(chosen_index)


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





def smoothing(road: Road, wheel: Wheel, iterations=1):
    """
    @TO DO THE SAME FORMAT AS digging.py, this would be the general function and then we
    can consider sub-smoothing procedures. This one would be one procedure, for example --->
    :param iterations:
    :param road:
    :return:
    """
    print("Before doing smoothing")
    print_road_surface(road, wheel.xf, wheel.diameter)
    #max_smoothing(road, (road.height+5) )
    #print_road_surface(road, wheel.xf, wheel.diameter)

   # for i in range(iterations):
   #      slope_smoothing(road)
    #max_smoothing(road, (road.height+2) )
    random_wind_smoothing(road, (road.height+2) )
    print("after doing smoothing")
    print_road_surface(road, wheel.xf, wheel.diameter)
    print("end smoothing iter")











######not working yet
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