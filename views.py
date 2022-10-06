import pydantic as pydantic
from celery.result import AsyncResult
from flask import jsonify, request
from flask.views import MethodView
from typing import Union

from app import app, celery
from models import Session, Advertisement
from tasks import send_emails


class CreateAdvertisementModel(pydantic.BaseModel):
    title: str
    description: str
    owner: str
    email: str


class HTTPError(Exception):
    def __init__(self, status_code: int, message: Union[str, list, dict]):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HTTPError)
def handle_invalid_usage(error):
    response = jsonify({"message": error.message})
    response.status_code = error.status_code
    return response


def validate(unvalidated_data: dict, validation_model):
    try:
        return validation_model(**unvalidated_data).dict()
    except pydantic.ValidationError as er:
        raise HTTPError(400, er.errors())


class AdvertisementView(MethodView):

    def get(self, advertisement_id: int):
        with Session() as session:
            advertisement = session.query(Advertisement).get(advertisement_id)
            if advertisement is None:
                response = jsonify({
                    'status': 'error',
                    'description': 'advertisement does not exist'
                })
                response.status_code = 404
                return response
            return jsonify(advertisement.to_dict())

    def post(self):
        with Session() as session:
            register_data = validate(request.json, CreateAdvertisementModel)
            return Advertisement.create(session, **register_data).to_dict()

    def delete(self, advertisement_id: int):
        with Session() as session:
            return Advertisement.delete(session, advertisement_id)


class SpamView(MethodView):

    def get(self, task_id):
        task = AsyncResult(task_id, app=celery)
        return jsonify({'status': task.status,
                        'result': task.result})
    def post(self):
        task = send_emails.delay()
        return jsonify(
            {'task_id': task.id}
        )

