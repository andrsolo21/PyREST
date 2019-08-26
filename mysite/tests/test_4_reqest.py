from django.test import TestCase


import json

class YourTestClass4(TestCase):


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



