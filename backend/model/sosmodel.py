from mongoengine import Document, StringField, DateTimeField, BooleanField
from datetime import datetime

class EmergencyContact(Document):
    name = StringField(required=True)
    phone = StringField(required=True)
    result = StringField()   # e.g., message delivery result
    message = StringField()  # actual SMS content
    status = BooleanField(default=False)  # success/fail
    sent_at = DateTimeField(default=datetime.utcnow)
