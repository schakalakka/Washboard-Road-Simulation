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

    def __getitem__(self, key: int):
        """
        Getter function to make subscripting available.
        Use: road[key]
        :param key:
        :return: height at key position, road.piles[key]
        """
        return self.piles[key]

    def __setitem__(self, key: int, value: int):
        """
        Setter function to make assignable subscripting available.
        Use: road[key] = foo
        :param key: position on the road
        :param value: assigned height
        :return:
        """
        self.piles[key % self.size] = value

    def get_number_of_grains(self) -> int:
        """
        :return: the number of current sand grains that the road contains
        """
        return np.sum(self.piles)

    def add_random_irregularities(self, nr_of_random_irregularities: int, in_segment=None):
        """
        This methods adds random irregularities to the road.
        If in_segment is None it will consider the whole road
        if in_segment is a tuple of two integers it will
        :param nr_of_random_irregularities: int
        :param in_segment: Tuple(int,int) or None
        """
        if not in_segment:
            in_segment = (0, self.size)
        elif type(in_segment) is not tuple or in_segment[0] < in_segment[1]:
            return
        irregular_positions = np.random.randint(in_segment[0], in_segment[1], nr_of_random_irregularities)
        self.add_grains(irregular_positions, [1] * nr_of_random_irregularities)

    def add_specific_irregularities(self, positions: list, n_grains: list):
        """
        TODO  kind of useless with the add_grain/add_grains methods
        :param positions: positions or pile numbers of the road where to add extra grains
        :param n_grains: numbers of grains to add in each position
        :return:
        """
        self.piles[positions] += n_grains

    def add_grain(self, position: int, n_grains=1):
        """
        Adds n_grains to position on the road.
        Catches out of bounds positions with modulo operator.
        :param position: positive integer
        :param n_grains: number of grains to add at position
        """
        self.piles[position % self.size] += n_grains

    def remove_grain(self, position: int, n_grains=1):
        """
        Removes n_grains from position on the road.
        Catches out of bounds positions with modulo operator.
        :param position: positive integer
        :param n_grains: number of grains to remove from position
        """
        self.piles[position % self.size] -= n_grains

    def add_grains(self, positions: list, n_grains: list):
        """
        Convenience function, gets a list of positions and a list of number of grains and adds them to the specific
        positions
        :param positions: list of positions
        :param n_grains: list of number of grains to add
        """
        for i, position in enumerate(positions):
            self.add_grain(position, n_grains[i])

    def remove_grains(self, positions: list, n_grains: list):
        """
        Convenience function, gets a list of positions and a list of number of grains and removes them from the specific
        positions
        :param positions: list of positions
        :param n_grains: list of number of grains to remove
        """
        for i, position in enumerate(positions):
            self.remove_grain(positions[position], n_grains[i])
