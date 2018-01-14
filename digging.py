from road import Road
from wheel import Wheel
import numpy as np
import sys

def digging(road: Road, wheel: Wheel, position: int, method='backwards'):
    """
    Updates the road after a digging event.
    :param road: a Road
    :param wheel: a Wheel
    :param position: reference position from which start the digging event (usually it is the wheel's position)
    :param method: digging method
    :return: a call to a particular digging function depending on the value of the method parameter.
    """
    if method == 'backwards':
        return dig_backwards(road, wheel, position)
    if method == 'backwards_softness':
        return dig_backwards_softness(road, wheel, position)

def dig_backwards(road: Road, wheel: Wheel, position: int):  # -> Tuple[np.ndarray, int]:
    """
    @TODO
    (MODIFY)Returns the after a backwards digging event, i.e. all the sand is put back behind the wheel
    :param road: a Road
    :param wheel: a Wheel
    :param position: position from which start the digging event
    :return: void
    """
    remove_from = np.mod(np.arange(position - wheel.diameter + 1, position + 1), road.size)
    put_on = np.mod(np.arange(position - 2 * wheel.diameter + 1, position - wheel.diameter + 1), road.size)
    increments = (road.piles[remove_from] > 0).astype(int)

    if len(remove_from) != len(put_on):
        print("\nWe are going to remove or put more or less than put or remove grains\n")
        sys.exit()

    road.piles[remove_from] -= increments
    road.piles[put_on] += increments


def quadratic_dig_probability(h: np.array, h0: int) -> np.array:
    p = h
    p[h < 0] = 0
    p[(h>=0) | (h <= h0)] = p[(h>=0) | (h <= h0)]**3/h0**3
    p[h>h0] = 1
    return(p)

def exponential_dig_probability(h: np.array, h0: int, alpha: float) -> np.array:
    p = h
    p[h < 0] = 0
    p[(h>=0) | (h <= h0)] = (np.exp(alpha * p[(h>=0) | (h <= h0)]) -1)/ (np.exp(alpha * h0) -1)
    p[h > h0] = 1
    return(p)

def dig_backwards_softness(road: Road, wheel: Wheel, position: int):  # -> Tuple[np.ndarray, int]:
    """
    @TODO
    (MODIFY)Returns the after a backwards digging event, i.e. all the sand is put back behind the wheel
    :param road: a Road
    :param wheel: a Wheel
    :param position: position from which start the digging event
    :return: void
    """
    remove_from = np.mod(np.arange(position - wheel.diameter + 1, position + 1), road.size)
    put_on = np.mod(np.arange(position - 2 * wheel.diameter + 1, position - wheel.diameter + 1), road.size)

    random_probs = np.random.uniform(0, 1, wheel.diameter)
    #dig_probs = quadratic_dig_probability(road.piles[remove_from], road.height)
    alpha = 0.005
    dig_probs = exponential_dig_probability(road.piles[remove_from], road.height, alpha)

    increments = (random_probs <= dig_probs).astype(int)

    if len(remove_from) != len(put_on):
        print("\nWe are going to remove or put more or less than put or remove grains\n")
        sys.exit()

    road.piles[remove_from] -= increments
    road.piles[put_on] += increments