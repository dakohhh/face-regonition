import datetime
from typing import List
import pytz
from mongoengine import Document, StringField, DecimalField,  EmailField, ReferenceField, CASCADE, ListField, IntField, BooleanField, DateTimeField, FloatField, EmbeddedDocumentField, EmbeddedDocument, ObjectIdField



class Users(Document):
    username = StringField(required=True, min_lenght=3, max_length=50, unique=True)

    firstname = StringField(required=True, min_lenght=3, max_length=50)

    lastname = StringField(required=True, min_lenght=3, max_length=50)

    password = StringField(required=True)

    email = EmailField(required=True, unique=True)

    role = StringField(required=True, choices=["user", "vendor", "superAdmin"])


    meta = {"collection": "users", "strict": False}


    def to_dict(self) -> dict:
        return {
            "_id": str(self.id),
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "role": self.role
        }





















