import numpy as np


class Road:
    """
    Object that represents a Road.
    """

    def __init__(self, size: int, standard_height: int, irregularities='random', positions=list([1]),
                 n_grains=list([1])):
        """
        Initialisation function for the Road class.
        :param size: the length of the road (number of piles or columns that form the road)
        :param standard_height: the standard height, with respect to a 0 level, of the road.
        :param irregularities: method to initialise irregularities for the road
        :param positions: If the irregularities method requires it,
                          it is the list of positions where the irregularities have to be added.
        :param n_grains:  List containing the number of grains to be added in each position of
                          the :positions: list.
        """
        # Each pile of the road is filled with :standard_height: grains of sand
        # piles is an array with height at each position of the road
        self.piles = np.full(size, standard_height, dtype=np.int)
        self.size = size
        self.height = standard_height

        if irregularities == 'random':
            self.add_random_irregularities(n_grains[0])
        elif irregularities == 'specific':
            self.add_specific_irregularities(positions, n_grains)

        # Store the number of initial grains (the total number of sand grains) that the road contains.
        self.initial_number_of_grains = self.get_number_of_grains()

    def __getitem__(self, item: int):
        return self.piles[item]

    def __setitem__(self, key: int, value: int):
        self.piles[key] = value

    def get_number_of_grains(self) -> int:
        """
        :return: the number of current sand grains that the road contains
        """
        return np.sum(self.piles)

    def add_random_irregularities(self, nr_of_random_irregularities: int):
        """
        @TODO
        :param nr_of_random_irregularities: @TODO
        """
        irregular_positions = np.random.randint(0, len(self.piles), nr_of_random_irregularities)
        self.piles[irregular_positions] = [self.height + 1] * nr_of_random_irregularities

    def add_specific_irregularities(self, positions: list, n_grains: list):
        """
        :param positions: positions or pile numbers of the road where to add extra grains
        :param n_grains: numbers of grains to add in each position
        :return:
        """
        self.piles[positions] += n_grains

    def add_grain(self, position: int, n_grains=1):
        """
        @SO FAR NOT USED
        :param position:
        :param n_grains:
        """
        self.piles[position] += n_grains

    def remove_grain(self, position: int, n_grains=1):
        """
        @SO FAR NOT USED
        :param position:
        :param n_grains:
        """
        self.piles[position] -= n_grains

    def add_grains(self, positions: list, n_grains: list):
        """
        @ SO FAR NOT USED
        :param positions:
        :param n_grains:
        """
        counter = 0
        for position in positions:
            self.add_grain(positions[position], n_grains[counter])
            counter += 1

    def remove_grains(self, positions: list, n_grains: list):
        """
        @ SO FAR NOT USED
        :param positions:
        :param n_grains:
        """
        counter = 0
        for position in positions:
            self.remove_grain(positions[position], n_grains[counter])
            counter += 1
