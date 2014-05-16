Terra_tv_car
=================

The source code is a test using mongoengine and flask


Installation
------------

1. Install [pip](http://www.pip-installer.org/en/latest/installing.html)
2. Make a [virtualenv](http://docs.python-guide.org/en/latest/starting/install/osx/) for this project: 
``` $  virtualenv venv ```
3. Activate venv ```$ . venv/bin/activate ```
4. Install the required dependencies:
```
$   pip install -r requirements.txt
```
Run the terra_tv:

    python manage.py runserver

Goto: [http://localhost:5001](http://localhost:5001)

Use this credentials to login :
urs: admin , passwd: admin

Run testes:
````
    python tests/terra_tv_car_tests.py
````
Todos
------
* Resize photos
* improving login
* improving validate form
* Activate the testing config to use another db.


References
----------
[Write a Tumblelog Application with Flask and MongoEngine](http://docs.mongodb.org/manual/tutorial/write-a-tumblelog-application-with-flask-mongoengine/)
tutorial.

