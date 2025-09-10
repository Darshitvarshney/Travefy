from mongoengine import StringField, EmailField, ListField, EmbeddedDocumentField, EmbeddedDocument, ObjectIdField , Document

class Curr_log(EmbeddedDocument):
    place = StringField(required=True)
    rating = StringField(required=True)
    review = StringField()
    photos = ListField(StringField())
    expense = StringField()
    time = StringField(required=True)


class Log(EmbeddedDocument):
    curr_log = ListField(EmbeddedDocumentField(Curr_log))

    
class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True)
    password = StringField(required=True)
    local_of = StringField(required=True)
    DOB = StringField(required=True)
    phone = StringField(required=True)
    gender = StringField(required=True)
    log = ListField(EmbeddedDocumentField(Log))