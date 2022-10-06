from celery import Celery
from flask import Flask


app_name = 'app'
app = Flask(app_name)
app.config['UPLOAD_FOLDER'] = 'files'

celery = Celery(
    app_name,
    backend='redis://localhost:6379/1',
    broker='redis://localhost:6379/2',
    imports=['tasks']
)

celery.conf.update(app.config)


# class ContextTask(celery.Task):
#     def __call__(self, *args, **kwargs):
#         with app.app_context():
#             return self.run(*args, **kwargs)
#
# celery.Task = ContextTask


