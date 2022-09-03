import pydantic as pydantic
from flask import Flask, jsonify, request
from flask.views import MethodView

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    create_engine,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from typing import Union


engine = create_engine('postgresql://app:1234@127.0.0.1:5431/netology')
Base = declarative_base()
Session = sessionmaker(bind=engine)
app = Flask('app')


class Advertisement(Base):
    __tablename__ = 'Advertisement'

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False, unique=True)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    owner = Column(String(64), nullable=False)

    @classmethod
    def create(cls, session: Session, title: str, description: str, owner: str):
        new_advertisement = Advertisement(
                                          title=title,
                                          description=description,
                                          owner=owner,
                                          )
        session.add(new_advertisement)
        try:
            session.commit()
            return new_advertisement
        except IntegrityError:
            session.rollback()

    @classmethod
    def delete(cls, session: Session, advertisement_id: int):
        advertisement = session.query(Advertisement).get(advertisement_id)
        if advertisement is None:
            return jsonify({
                    'status': 'error',
                    'description': 'advertisement does not exist'
                })
        session.delete(advertisement)
        session.commit()
        return jsonify({
                    'status': 'OK',
                    'description': 'advertisement removed'
                })

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": int(self.created_at.timestamp()),
            "owner": self.owner,
        }


class CreateAdvertisementModel(pydantic.BaseModel):
    title: str
    description: str
    owner: str


Base.metadata.create_all(engine)


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


app.add_url_rule(
    "/advertisement/<int:advertisement_id>/",
    view_func=AdvertisementView.as_view("get_advertisement"),
    methods=["GET"]
)
app.add_url_rule(
    "/advertisement/",
    view_func=AdvertisementView.as_view("create_advertisement"),
    methods=["POST"]
)
app.add_url_rule(
    "/advertisement/<int:advertisement_id>/",
    view_func=AdvertisementView.as_view("delete_advertisement"),
    methods=["DELETE"]
)

app.run()
