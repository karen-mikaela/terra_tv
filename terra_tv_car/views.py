# -*- coding: utf-8 -*-
from flask import  Blueprint, request, redirect, render_template, url_for, session, g, abort,jsonify
from flask.views import MethodView
from flask import send_from_directory

from werkzeug.utils import secure_filename
from terra_tv_car.models import Car
from terra_tv_car import app
from terra_tv_car import ALLOWED_EXTENSIONS

import os, datetime

cars = Blueprint('cars', __name__, template_folder='templates')
admin = Blueprint('admin', __name__, template_folder='templates')

def uploaded_file_name(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def delete_all_cars():
    pass

class AuthView(MethodView):

    def post(self, _session):
        error = None
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('admin.list'))
        if error:
            return redirect(url_for('admin.login'))

    def get(self, _session):
        error = None
        if _session:
            return render_template('admin/login.html', error=error, tab_active="login" )
        else:
            session.pop('logged_in', None)
            session.pop('username', None)
            return redirect(url_for('admin.list'))


class ListView(MethodView):

    def get(self, id):
        if not session.get('logged_in'):
            return redirect(url_for('admin.login'))
        if id:
            car = Car.objects.get_or_404(id=id)
            if car:
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], car.photo))
                except:
                    pass
                car.delete()
            return redirect(url_for('admin.list'))
        else:
            cars = Car.objects.all()
            return render_template('admin/list.html', cars=cars, tab_active= "admin")


class DetailView(MethodView):

    def verified_file(self,filename):
        extension = filename.split('.', 1)[1]
        allowed = '.' in filename and extension in ALLOWED_EXTENSIONS
        return {"extension":extension, "allowed":allowed}

    def upload_file(self, photo):
        verified = self.verified_file(filename=photo.filename)
        photo_name = "{0}.{1}".format(datetime.datetime.today().strftime("%Y%m%d%H%M%S"),
             verified['extension'])
        if verified['allowed']:
            try:
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(photo_name)))
                return photo_name
            except:
                return False



    def get(self,id):
        if not session.get('logged_in'):
            return redirect(url_for('admin.login'))
        if id:
            car = Car.objects.get_or_404(id=id)
        else:
            car = Car()

        context = {
            "car": car,
            "create": id is None,
            "tab_active" : "admin",
            "alert": "",
            "status": 0
        }

        return render_template('admin/detail.html',**context)


    def post(self, id):
        if not session.get('logged_in'):
            return redirect(url_for('admin.login'))
        model = request.form['model']
        year = request.form['year']
        manufacturer = request.form['manufacturer']
        photo = request.files['photo']

        if not model:
            context = {
                "car": Car(),
                "create": True,
                "tab_active" : "admin",
                "alert": u"O campo modelo é requerido.",
                "status": -1
                }
            return render_template('admin/detail.html',**context)

        if not manufacturer:
            context = {
                "car": Car(),
                "create": True,
                "tab_active" : "admin",
                "alert": u"O campo fabricante é requerido.",
                "status": -1
                }
            return render_template('admin/detail.html',**context)

        if not year:
            context = {
                "car": Car(),
                "create": True,
                "tab_active" : "admin",
                "alert": u"O campo ano é requerido.",
                "status": -1
                }
            return render_template('admin/detail.html',**context)

        if not photo and not id:
            context = {
                "car": Car(),
                "create": True,
                "tab_active" : "admin",
                "alert": u"O campo foto é requerido.",
                "status": -1
                }
            return render_template('admin/detail.html',**context)


        if photo:
            photo_name = self.upload_file(photo)
        if id:
            car = Car.objects.get_or_404(id=id)
            car.model = model
            car.year = year
            car.manufacturer = manufacturer
            if photo:
                #remove old photo
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], car.photo))
                except:
                    pass
                #update photo
                car.photo = photo_name
        else:
            car = Car(model=model, year=year, photo=photo_name, manufacturer=manufacturer)
        car.save()
        return redirect(url_for('admin.list'))

class SearchView(MethodView):

    def post(self):
        model = request.form['model']
        manufacturer = request.form['manufacturer']
        year = request.form['year']

        query = dict()
        if model:
            query['model'] = model
        if manufacturer:
            query['manufacturer'] = manufacturer
        if year:
            query['year'] = year

        cars = Car.objects(**query)

        return render_template('cars/search.html', cars=cars, tab_active= "car")

    def get(self):
        cars = Car.objects.all()
        return render_template('cars/search.html', cars=cars, tab_active= "car")

# Register the urls

admin.add_url_rule('/login/', defaults={'_session': "new"},view_func=AuthView.as_view('login'))
admin.add_url_rule('/logout/', defaults={'_session': None}, view_func=AuthView.as_view('logout'))
admin.add_url_rule('/admin/', defaults={'id': None}, view_func=ListView.as_view('list'))
admin.add_url_rule('/admin/delete/<id>/', view_func=ListView.as_view('delete'))
admin.add_url_rule('/admin/car/<id>/', view_func=DetailView.as_view('detail'))
admin.add_url_rule('/admin/create/', defaults={'id': None}, view_func=DetailView.as_view('create'))
cars.add_url_rule('/', view_func=SearchView.as_view('search'))
cars.add_url_rule('/photo/<filename>/', 'photos', view_func=uploaded_file_name)
cars.add_url_rule('/search/', view_func=SearchView.as_view('result'))


