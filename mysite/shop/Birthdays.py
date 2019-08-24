class Birthdays():

    """Class help to deal with 4 request in SfYBS(ship for yandex backend school)"""

    def __init__(self):

        """
        Function generate dictionary
        """

        #self.sets = dict()
        self.DRs = dict()

        for i in range(12):
            #self.sets[str(i+1)] = set()
            self.DRs[str(i+1)] = dict()

    def add(self, month, cit):

        """This function registrate new relative in dictionary

        INPUT: month of birthday, num of citizen
        OUTPUT: None
        """

        if cit in self.DRs[month]:
            self.DRs[month][cit] += 1
        else:
            self.DRs[month][cit] = 1

    def generate(self):

        """
        Function get and remade dictionary from self.

        :return:
        dictionary for rendering to JSON
        """
        otv = dict()
        for key in self.DRs:
            otv[key] = []
            for key2 in self.DRs[key]:
                otv[key].append(dict(
                    citizen_id = key2,
                    presents = self.DRs[key][key2]
                ))
        return otv
