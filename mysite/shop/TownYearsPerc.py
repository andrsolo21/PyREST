import numpy as np

class TownYearsPerc():

    """
    Class for fiveth request
    """

    def __init__(self):
        self.data = dict()
        self.out = np.zeros(3)
        self.mas = np.array([50,75,99])

    def add(self, town, age):

        """
        Function for adding information about new person
        :param town: town of person
        :param age: age of person
        :return: None
        """

        if town in self.data:
            self.data[town].append(age)
        else:
            self.data[town] = [age]

    def export(self):

        """
        Function return collect data
        :return: list of dictionaries
        """

        out = []
        for key in self.data:
            self.data[key].sort()
            np.percentile(self.data[key],self.mas,out = self.out,overwrite_input = True,interpolation='linear')

            out.append({
                "town" : key,
                "p50" : self.out[0],
                "p75" : self.out[1],
                "p99" : self.out[2]
            })
        return out
