import datetime
from flask import url_for
from terra_tv_car import db


class Car(db.Document):
    year = db.StringField(max_length=4, required=True)
    model = db.StringField(max_length=100, required=True)
    manufacturer  = db.StringField(max_length=10, required=True)
    photo  = db.StringField(max_length=100, required=True)

    def __unicode__(self):
        return self.model

    def get_photo_url(self):
        return url_for('cars.photos', filename=self.photo)

    meta = {
        'allow_inheritance': True,
        'indexes': ['model'],
        'ordering': ['model']
    }
