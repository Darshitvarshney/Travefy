from mongoengine import StringField, EmailField, DateTimeField, Document

class OTPModel(Document):
    email = EmailField(required=True, unique=True)
    otp = StringField(required=True)  # store hashed OTP
    expiry_time = DateTimeField(required=True)