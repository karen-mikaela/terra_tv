# -*- coding: utf-8 -*-
import os
import unittest
import flask

# Set the path
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from terra_tv_car import app


class TerraTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        app.config["MONGODB_SETTINGS"] = {'DB': "terra_car_test"}
        app.config['TESTING'] = True
        app.config["USERNAME"] = "admin"
        app.config["PASSWORD"] = "admin"
        self.app = app.test_client()

    def login(self, username, password):
        data = {
            'username': username,
            'password': password,
        }
        return self.app.post('/login/', data=data, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def create_new_car(self,new_car):
        photo = open(os.path.join(app.config['UPLOAD_FOLDER'],'test.jpg'),'r')
        new_car['photo'] = photo
        return self.app.post("/admin/create/", data=new_car, follow_redirects=True)

    ###############################
    # testing functions
    ###############################

    def test_get_login(self):
        response = self.app.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Login' in response.data)


    def test_login_logout(self):
        response = self.login(app.config['USERNAME'],app.config['PASSWORD'])
        self.assertEqual(response.status_code, 200)
        response = self.logout()
        self.assertTrue('Login' in response.data)


    def test_login_wrong_credentials(self):
        response = self.login("xpto", "xpto")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Login' in response.data)


    def test_get_search(self):
        response = self.app.get("/search/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Buscar por' in response.data)


    def test_filter_search(self):
        data = {
            'model':"xyz",
            'year':"2000",
            'manufacturer':"xpto"
        }
        response = self.app.post("/search/", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Não foi encontrado nenhum carro.' in response.data)


    def test_list_cars_without_login(self):
        response = self.app.get("/admin/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Lista Carro' in response.data)


    def test_list_cars_with_login(self):
        response = self.login(app.config['USERNAME'],app.config['PASSWORD'])
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Olá admin' in response.data)
        response = self.app.get("/admin/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        #show car list
        self.assertTrue('Lista Carro' in response.data)


    def test_create_new_car(self):
        response = self.login(app.config['USERNAME'],app.config['PASSWORD'])
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Olá admin' in response.data)
        new_car = {
            'model':"my_model",
            'year':"2014",
            'manufacturer':"my_manufacturer"
        }
        response = self.create_new_car(new_car)
        self.assertEqual(response.status_code, 200)
        #show car list
        self.assertTrue('Lista Carro' in response.data)


    def test_delete_car_doesnt_exist(self):
        response = self.login(app.config['USERNAME'],app.config['PASSWORD'])
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Olá admin' in response.data)
        response = self.app.get("/admin/delete/53759235dc0b7d696f309bbc/",follow_redirects=True)
        self.assertEqual(response.status_code, 404)


    def test_edit_car_doesnt_exist(self):
        response = self.login(app.config['USERNAME'],app.config['PASSWORD'])
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Olá admin' in response.data)
        response = self.app.get("/admin/car/53759235dc0b7d696f309bbc/",follow_redirects=True)
        self.assertEqual(response.status_code, 404)



if __name__ == '__main__':
    unittest.main()
