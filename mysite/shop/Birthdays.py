class Birthdays():

    def __init__(self):
        #self.sets = dict()
        self.DRs = dict()

        for i in range(12):
            #self.sets[str(i+1)] = set()
            self.DRs[str(i+1)] = dict()

    def add(self, month, cit):
        if cit in self.DRs[month]:
            self.DRs[month][cit] += 1
        else:
            self.DRs[month][cit] = 1

    def generate(self):
        otv = dict()
        for key in self.DRs:
            otv[key] = []
            for key2 in self.DRs[key]:
                otv[key].append(dict(
                    citizen_id = key2,
                    presents = self.DRs[key][key2]
                ))
        return otv
