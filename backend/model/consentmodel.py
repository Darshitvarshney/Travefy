from mongoengine import Document, BooleanField

class location(Document):

    agreed = BooleanField(required=True)
