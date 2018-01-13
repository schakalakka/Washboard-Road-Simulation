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
    increments = (road.piles[remove_from] > 0).astype(int)

    if len(remove_from) != len(put_on):
        print("\nWe are going to remove or put more or less than put or remove grains\n")
        sys.exit()

    road.piles[remove_from] -= increments
    road.piles[put_on] += increments