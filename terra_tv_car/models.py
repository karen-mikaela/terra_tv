import datetime
from flask import url_for
from terra_tv_car import db


class Car(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    year = db.StringField(max_length=4, required=True)
    model = db.StringField(max_length=100, required=True)
    manufacturer  = db.StringField(max_length=10, required=True)
    photo  = db.StringField(max_length=100, required=True)
    slug = db.StringField(max_length=255, required=True)

    def get_absolute_url(self):
        return url_for('car', kwargs={"slug ": self.slug})

    def __unicode__(self):
        return self.model

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }
