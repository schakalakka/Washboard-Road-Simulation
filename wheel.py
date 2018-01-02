import sys


class Wheel:
    """
    Object that represents a vehicle wheel
    """

    def __init__(self, diameter: int, right_position: int, elevation: int, velocity: int, period: int):
        """
         Initalisation function for the Wheel class.
        :param diameter: diameter of the wheel.
        :param right_position: position of the right most part of the wheel (from 0 to period-1).
        :param elevation: wheel elevation with respect to the ground level of the road it is inside.
        :param velocity: velocity of the wheel (BETA).
        :param period: length of the road in which the wheel is.
        """
        self.diameter = diameter
        self.xf = right_position % period
        self.x0 = (self.xf - self.diameter + 1) % period  # Care, now it could be negative
        self.elevation = elevation
        self.period = period
        self.velocity = velocity
        self.number_of_passes = 0

    def set_diameter(self, new_diameter: int):
        """
        Change the current diameter of the wheel to another value
        :param new_diameter: new value of the wheel's diameter
        """
        if new_diameter <= 0:
            print('Error: Wheel diameter can not be set to a negative number nor zero.')
            sys.exit()
        self.diameter = new_diameter

    def set_elevation(self, new_elevation: int):
        """
         Change the current elevation of the wheel to another value
        :param new_elevation: new value for the wheel's elevation
        """
        if new_elevation < 0:
            print('Error: Wheel elevation can not be set to a negative number.')
            sys.exit()
        self.elevation = new_elevation

    def set_velocity(self, new_velocity: int):
        """
        Change the current velocity of the wheel to another value
        :param new_velocity: new value for the velocity
        """
        self.velocity = new_velocity

    def set_xf(self, new_xf: int):
        """
        Change the right-most (xf) position of the wheel to another value. At the same time the left-most
        part if the wheel (x0) is changed. PERIODIC CONDITIONS are applied.
        :param new_xf:
        """
        if new_xf >= self.period or new_xf < 0:
            print('Intent to set xf to a negative number or out of the road. Applying periodic', self.period,
                  'conditions.')
        self.xf = new_xf % self.period
        self.x0 = (self.xf - self.diameter + 1) % self.period

    def update_position(self, steps: int):
        """
        The position of the wheel is updated: incremented or decremented 'steps' times depending on the sign
        of the parameter steps.
        :param steps:
        """
        new_xf = self.xf + steps
        self.set_xf(new_xf)

    def update_velocity(self, steps: int):
        """
        The same as update_position but for the velocity
        :param steps:
        """
        new_velocity = self.velocity + steps
        self.set_velocity(new_velocity)

    def update_elevation(self, steps: int):
        """
        The same as update_position but for the elevation
        :param steps:
        """
        new_elevation = self.elevation + steps
        self.set_elevation(new_elevation)

    def update_diameter(self, steps: int):
        """
        The same as update_position but for the diameter
        :param steps:
        """
        new_diameter = self.diameter + steps
        self.set_diameter(new_diameter)
