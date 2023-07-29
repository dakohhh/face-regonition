from typing import List
from mongoengine import Document, StringField, DecimalField,  EmailField, ReferenceField, CASCADE, ListField, IntField, BooleanField, DateTimeField, FloatField, EmbeddedDocumentField, EmbeddedDocument, ObjectIdField



class Users(Document):

    firstname = StringField(required=True, min_lenght=3, max_length=50)

    lastname = StringField(required=True, min_lenght=3, max_length=50)

    matric_no = IntField(required=True)

    is_blacklisted = BooleanField(required=True, default=False)


    meta = {"collection": "users", "strict": False}


    def to_dict(self) -> dict:
        return {
            "_id": str(self.id),
            "firstname": self.firstname,
            "lastname": self.lastname,
            "matric_no": self.matric_no,
            "is_blacklisted": self.is_blacklisted
        }





















