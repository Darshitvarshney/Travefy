from mongoengine import StringField, EmailField, Document


class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True)
    password = StringField(required=True)
    local_of = StringField(required=True)
