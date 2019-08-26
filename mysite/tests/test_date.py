from django.test import TestCase



class YourTestClass(TestCase):

    tests = [['01.02.0289','0289-02-01','1'],
             ['dhfh.gfnhgf.fgf',None,'2'],
             ]

    printing = False

    @classmethod
    def setUpTestData(cls):
        #print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        #print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_goodDate(self):
        i = 0
        if self.printing:
            print(self.tests[i][2])
        self.assertEqual(parseDate(self.tests[i][0]), self.tests[i][1], self.tests[i][2])

    def test_badStriing(self):
        i = 1
        if self.printing:
            print(self.tests[i][2])
        self.assertEqual(parseDate(self.tests[i][0]), self.tests[i][1], self.tests[i][2])

    def test_bigYear(self):
        date = datetime.date.today() + datetime.timedelta(weeks=903)
        if self.printing:
            print(date)
        self.assertEqual(parseDate(str(date.day)+ '.' + str(date.month) + '.' + str(date.year)), None)

    def test_bigMonth(self):
        date = datetime.date.today() + datetime.timedelta(weeks=7)
        if self.printing:
            print(date)
        self.assertEqual(parseDate(str(date.day)+ '.' + str(date.month) + '.' + str(date.year)), None)

    def test_bigDay(self):
        date = datetime.date.today() + datetime.timedelta(days=1)
        if self.printing:
            print(date)
        self.assertEqual(parseDate(str(date.day)+ '.' + str(date.month) + '.' + str(date.year)), None)

    def test_Now(self):
        date = datetime.date.today()
        if self.printing:
            print(date)
        self.assertEqual(parseDate(str(date.day)+ '.' + str(date.month) + '.' + str(date.year)), str(date.year)+ '-' + str(date.month) + '-' + str(date.day))

    def test_lowDate(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        if self.printing:
            print(date)
        self.assertEqual(parseDate(str(date.day)+ '.' + str(date.month) + '.' + str(date.year)), str(date.year)+ '-' + str(date.month) + '-' + str(date.day))

    def test_lowMonth(self):
        date = datetime.date.today() - datetime.timedelta(weeks=5)
        if self.printing:
            print(date)
        self.assertEqual(parseDate(str(date.day)+ '.' + str(date.month) + '.' + str(date.year)), str(date.year)+ '-' + str(date.month) + '-' + str(date.day))

    def test_lowYear(self):
        date = datetime.date.today() - datetime.timedelta(weeks = 80)
        if self.printing:
            print(date)
        self.assertEqual(parseDate(str(date.day)+ '.' + str(date.month) + '.' + str(date.year)), str(date.year)+ '-' + str(date.month) + '-' + str(date.day))