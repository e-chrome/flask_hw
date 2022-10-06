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
from flask import jsonify


engine = create_engine('postgresql://user:1234@127.0.0.1:5431/netology')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Advertisement(Base):
    __tablename__ = 'Advertisement'

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False, unique=True)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    owner = Column(String(64), nullable=False)
    email = Column(String(255), nullable=False)

    @classmethod
    def create(cls, session: Session, title: str, description: str, owner: str, email: str):
        new_advertisement = Advertisement(
                                          title=title,
                                          description=description,
                                          owner=owner,
                                          email=email,
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
            "email": self.email,
        }

