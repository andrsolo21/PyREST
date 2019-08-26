from django.test import TestCase

from shop.views import parseDate
import datetime

import json

class YourTestDate(TestCase):

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

class YourTestClass_1(TestCase):

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

    def test_import_1_1(self):

        """good test"""

        with open("tests/data/1/persons_1.json", "r",encoding="utf-8") as f:
            data = json.load(f)

        resp = self.client.post('/imports/',data = data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)

    def test_import_1_2(self):

        """test without one field"""

        with open("tests/data/1/persons_2.json", "r",encoding="utf-8") as f:
            data = json.load(f)

        resp = self.client.post('/imports/',data = data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)

class YourTestClass_2(TestCase):


    printing = False

    @classmethod
    def setUpTestData(cls):
        #print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        #print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_import_2_1(self):

        """good test"""

        with open("tests/data/1/persons_1.json", "r",encoding="utf-8") as f:
            data1 = json.load(f)

        resp = self.client.post('/imports/',data = data1, content_type='application/json')
        self.assertEqual(resp.status_code, 201)

        data = resp.json()

        self.assertFalse((data.get('data')) == None)

        if 'data' in data:
            self.assertFalse((data['data'].get('import_id')) == None)

            if 'import_id' in data['data']:
                imp_id = data['data']['import_id']

                with open("tests/data/2/person_1.json", "r",encoding="utf-8") as f:
                    data = json.load(f)

                resp = self.client.patch('/imports/' + str(imp_id) + '/citizens/1',data = data['data'], content_type='application/json')
                self.assertEqual(resp.status_code, 200)

                dataR = resp.json()

                self.assertFalse((dataR.get('data')) == None)


    def test_import_2_2(self):

        """test with field citizen_id"""

        with open("tests/data/1/persons_1.json", "r",encoding="utf-8") as f:
            data1 = json.load(f)

        resp = self.client.post('/imports/',data = data1, content_type='application/json')
        self.assertEqual(resp.status_code, 201)

        data = resp.json()

        self.assertFalse((data.get('data')) == None)

        if 'data' in data:
            self.assertFalse((data['data'].get('import_id')) == None)

            if 'import_id' in data['data']:
                imp_id = data['data']['import_id']

                with open("tests/data/2/person_2.json", "r",encoding="utf-8") as f:
                    data = json.load(f)

                resp = self.client.patch('/imports/' + str(imp_id) + '/citizens/1',data = data['data'], content_type='application/json')
                self.assertEqual(resp.status_code, 400)

class YourTestClass_3(TestCase):


    printing = False

    @classmethod
    def setUpTestData(cls):
        #print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        #print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_import_3_1(self):

        """good test"""

        with open("tests/data/1/persons_1.json", "r",encoding="utf-8") as f:
            data1 = json.load(f)

        resp = self.client.post('/imports/',data = data1, content_type='application/json')
        self.assertEqual(resp.status_code, 201)

        data = resp.json()

        self.assertFalse((data.get('data')) == None)

        if 'data' in data:
            self.assertFalse((data['data'].get('import_id')) == None)

            if 'import_id' in data['data']:
                imp_id = data['data']['import_id']

                resp = self.client.get('/imports/' + str(imp_id) + '/citizens/')
                self.assertEqual(resp.status_code, 200)

                dataR = resp.json()

                self.assertFalse((dataR.get('data')) == None)

    def test_import_3_1(self):

        """big import id"""

        with open("tests/data/1/persons_1.json", "r",encoding="utf-8") as f:
            data1 = json.load(f)

        resp = self.client.post('/imports/',data = data1, content_type='application/json')
        self.assertEqual(resp.status_code, 201)

        data = resp.json()

        self.assertFalse((data.get('data')) == None)

        if 'data' in data:
            self.assertFalse((data['data'].get('import_id')) == None)

            if 'import_id' in data['data']:
                imp_id = data['data']['import_id']

                resp = self.client.get('/imports/' + str(imp_id + 200) + '/citizens/')
                self.assertEqual(resp.status_code, 400)

class YourTestClass_4(TestCase):


    printing = False

    @classmethod
    def setUpTestData(cls):
        #print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        #print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_import_4_1(self):

        """good test"""

        with open("tests/data/1/persons_1.json", "r",encoding="utf-8") as f:
            data1 = json.load(f)

        resp = self.client.post('/imports/',data = data1, content_type='application/json')
        self.assertEqual(resp.status_code, 201)

        data = resp.json()

        self.assertFalse((data.get('data')) == None)

        if 'data' in data:
            self.assertFalse((data['data'].get('import_id')) == None)

            if 'import_id' in data['data']:
                imp_id = data['data']['import_id']

                resp = self.client.get('/imports/' + str(imp_id) + '/citizens/birthdays')
                self.assertEqual(resp.status_code, 200)

                dataR = resp.json()

                self.assertFalse((dataR.get('data')) == None)

                for i in range(1,12):
                    self.assertFalse((dataR['data'].get(str(i))) == None)

class YourTestClass_5(TestCase):


    printing = False

    @classmethod
    def setUpTestData(cls):
        #print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        #print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_import_5_1(self):

        """good test"""

        with open("tests/data/1/persons_1.json", "r",encoding="utf-8") as f:
            data1 = json.load(f)

        resp = self.client.post('/imports/',data = data1, content_type='application/json')
        self.assertEqual(resp.status_code, 201)

        data = resp.json()

        self.assertFalse((data.get('data')) == None)

        if 'data' in data:
            self.assertFalse((data['data'].get('import_id')) == None)

            if 'import_id' in data['data']:
                imp_id = data['data']['import_id']

                resp = self.client.get('/imports/' + str(imp_id) + '/towns/stat/percentile/age/')
                self.assertEqual(resp.status_code, 200)

                dataR = resp.json()

                self.assertFalse((dataR.get('data')) == None)