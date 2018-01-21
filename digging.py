from road import Road
from wheel import Wheel
import numpy as np
import sys


def constant_dig_probability(h: np.array, args: list):
    if len(args) != 1:
        print('Error: incorrect number of arguments in constant_dig_probability, using default p = 1')
        p_constant = 1
    else:
        p_constant = args[0]
    return np.full(len(h), p_constant, dtype=np.float)


def quadratic_dig_probability(h: np.array, args: list) -> np.array:
    if len(args) != 1:
        print('Error: incorrect number of arguments in quadratic_dig_probability')
        sys.exit()
    h0 = args[0]

    p = np.full(len(h), 0, dtype=np.float)
    p[(h > 0) | (h <= h0)] = h[(h > 0) | (h <= h0)] ** 3 / h0 ** 3
    p[h > h0] = 1
    p[h <= 0] = 0

    return p


def non_tailed_exponential_dig_probability(h: np.array, args: list) -> np.array:
    if len(args) != 2:
        print('Error: incorrect number of arguments in exponential_dig_probability')
        sys.exit()
    h0 = args[0]
    alpha = args[1]

    p = np.full(len(h), 0, dtype=np.float)
    p[(h > 0) | (h <= h0)] = (np.exp(alpha * h[(h > 0) | (h <= h0)]) - 1) / (np.exp(alpha * h0) - 1)
    p[h > h0] = 1
    p[h <= 0] = 0

    return p


def tailed_exponential_dig_probability(h: np.array, args: list) -> np.array:
    if len(args) != 2:
        print('Error: incorrect number of arguments in tail_exponential_dig_probability')
        sys.exit()

    h0 = args[0]
    alpha = args[1]

    p = np.full(len(h), 0, dtype=np.float)
    p[(h > 0) | (h <= h0)] = np.exp(alpha * (h[(h > 0) | (h <= h0)] - h0))
    p[h > h0] = 1
    p[h <= 0] = 0

    return p


def digging(road: Road, wheel: Wheel, position: int, method='backwards uniform', dig_probability_args=list([1])):
    """
    Updates the road after a digging event.
    :param road: a Road
    :param wheel: a Wheel
    :param position: reference position from which start the digging event (usually it is the wheel's position)
    :param method: digging method, possible options: backwards uniform, backwards tailed exponential,
                    backwards non-tailed exponential, backwards quadratic
    :param dig_probability_args:
    :return: a call to a particular digging function depending on the value of the method parameter.
    """
    if method == 'backwards uniform':
        return dig_backwards_softness(road, wheel, position, constant_dig_probability, dig_probability_args)
    if method == 'backwards tailed exponential':
        return dig_backwards_softness(road, wheel, position, tailed_exponential_dig_probability, dig_probability_args)
    if method == 'backwards non-tailed exponential':
        return dig_backwards_softness(road, wheel, position, non_tailed_exponential_dig_probability,
                                      dig_probability_args)
    if method == 'backwards quadratic':
        return dig_backwards_softness(road, wheel, position, quadratic_dig_probability, dig_probability_args)


def dig_backwards_softness(road: Road, wheel: Wheel, position: int, dig_probability_function,
                           dig_probability_args: list):  # -> Tuple[np.ndarray, int]:
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

    random_probabilities = np.random.uniform(0, 1, wheel.diameter)

    dig_probabilities = dig_probability_function(road.piles[remove_from], dig_probability_args)
    # print(dig_probabilities)
    increments = (random_probabilities <= dig_probabilities).astype(int)

    # if len(remove_from) != len(put_on):
    # print("\nWe are going to remove or put more or less than put or remove grains\n")
    # sys.exit()

    road.piles[remove_from] -= increments
    road.piles[put_on] += increments
