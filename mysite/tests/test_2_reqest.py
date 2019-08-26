from django.test import TestCase


import json

class YourTestClass96(TestCase):


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

        print(type(data))

        self.assertFalse((data.get('data')) == None)

        if 'data' in data:
            self.assertFalse((data['data'].get('import_id')) == None)

            if 'import_id' in data['data']:
                imp_id = data['data']['import_id']

                with open("tests/data/2/person_2.json", "r",encoding="utf-8") as f:
                    data = json.load(f)

                resp = self.client.patch('/imports/' + str(imp_id) + '/citizens/1',data = data['data'], content_type='application/json')
                self.assertEqual(resp.status_code, 400)