from flask import  Blueprint, request, redirect, render_template, url_for, flash, session, g, abort
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

class AuthView(MethodView):

    def post(self, _session):
        error = None
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('cars.list'))
        if error:
            return redirect(url_for('admin.login'))

    def get(self, _session):
        error = None
        if _session:
            return render_template('admin/login.html', error=error, tab_active="login" )
        else:
            session.pop('logged_in', None)
            flash('You were logged out')
            return redirect(url_for('cars.list'))


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
                flash('foi deletado')
            return redirect(url_for('cars.list'))
        else:
            cars = Car.objects.all()
            return render_template('cars/list.html', cars=cars, tab_active= "admin")


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
            abort(401)
        if id:
            car = Car.objects.get_or_404(id=id)
        else:
            car = Car()

        context = {
            "car": car,
            "create": id is None,
            "tab_active" : "admin"
        }

        return render_template('cars/detail.html',**context)


    def post(self, id):
        if not session.get('logged_in'):
            abort(401)
        model = request.form['model']
        year = request.form['year']
        manufacturer = request.form['manufacturer']
        photo = request.files['photo']

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

        return redirect(url_for('cars.list'))

class SearchView(MethodView):

    def post(self):
        abort(404)

    def get(self):
        cars = Car.objects.all()
        return render_template('cars/search.html', cars=cars, tab_active= "car")

# Register the urls

admin.add_url_rule('/login/', defaults={'_session': "new"},view_func=AuthView.as_view('login'))
admin.add_url_rule('/logout/', defaults={'_session': None}, view_func=AuthView.as_view('logout'))
cars.add_url_rule('/admin/', defaults={'id': None}, view_func=ListView.as_view('list'))
cars.add_url_rule('/admin/delete/<id>/', view_func=ListView.as_view('delete'))
cars.add_url_rule('/admin/car/<id>/', view_func=DetailView.as_view('detail'))
cars.add_url_rule('/photo/<filename>/', 'photos', view_func=uploaded_file_name)
cars.add_url_rule('/admin/create/', defaults={'id': None}, view_func=DetailView.as_view('create'))
cars.add_url_rule('/', view_func=SearchView.as_view('search'))
