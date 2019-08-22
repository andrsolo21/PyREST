from django.test import TestCase

from shop.views import parseDate
import datetime
import json

class YourTestClass2(TestCase):

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

        #with open("tests/persons_1.json", "r") as f:
        #    data = f.readlines()

        #dataJ = json.loads('.'.join(data))
        #print(type(dataJ))

        #print(dataJ)
        pass

        #i = 0
        #if self.printing:
        #    print(self.tests[i][2])
        #self.assertEqual(parseDate(self.tests[i][0]), self.tests[i][1], self.tests[i][2])

    def test_import_1(self):

        """good test"""

        with open("tests/data/persons_1.json", "r",encoding="utf-8") as f:
            data = json.load(f)

        resp = self.client.post('/imports/',data = data, content_type='application/json')
        #resp = self.client.get('/catalog/authors/')
        self.assertEqual(resp.status_code, 201)

    def test_import_2(self):

        """test without one field"""

        with open("tests/data/persons_2.json", "r",encoding="utf-8") as f:
            data = json.load(f)

        resp = self.client.post('/imports/',data = data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_import_3(self):

        """string in place int"""

        with open("tests/data/persons_3.json", "r",encoding="utf-8") as f:
            data = json.load(f)

        resp = self.client.post('/imports/',data = data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)