from django.test import TestCase


import json

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
