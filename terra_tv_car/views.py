from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form
from terra_tv_car.models import Car

cars = Blueprint('cars', __name__, template_folder='templates')

class ListView(MethodView):

    def get(self, slug):
        if slug:
            car = Car.objects.get_or_404(slug=slug)
            print vars(car)
            if car:
                car.delete()
            return redirect(url_for('cars.list'))
        else:
            cars = Car.objects.all()
            return render_template('cars/list.html', cars=cars)


class DetailView(MethodView):
    form = model_form(Car, exclude=['created_at'])



    def get_context(self, slug=None):
        form_cls = model_form(Car, exclude=('created_at'))

        if slug:
            car = Car.objects.get_or_404(slug=slug)
            if request.method == 'POST':
                form = form_cls(request.form, inital=car._data)
            else:
                form = form_cls(obj=car)
        else:
            car = Car()
            form = form_cls(request.form)

        context = {
            "car": car,
            "form": form,
            "create": slug is None
        }
        return context


    def get(self, slug):
        context = self.get_context(slug)
        return render_template('cars/detail.html', **context)


    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            car = context.get('car')
            form.populate_obj(car)
            car.save()

            return redirect(url_for('cars.list'))
        return render_template('cars/list.html', **context)


# Register the urls
cars.add_url_rule('/', defaults={'slug': None}, view_func=ListView.as_view('list'))
cars.add_url_rule('/delete/<slug>/', view_func=ListView.as_view('delete'))
cars.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
cars.add_url_rule('/create/', defaults={'slug': None}, view_func=DetailView.as_view('create'))
