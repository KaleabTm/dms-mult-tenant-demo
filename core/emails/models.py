from django.db import models

from core.common.models import BaseModel


class Email(BaseModel):
    class Status(models.TextChoices):
        READY = "READY", "Ready"
        SENDING = "SENDING", "Sending"
        SENT = "SENT", "Sent"
        FAILED = "FAILED", "Failed"

    class Type(models.TextChoices):
        OTP_VERIFICATION = "OTP_VERIFICATION", "OTP Verification"
        REGISTRATION = "REGISTRATION", "Registration"
        NOTIFICATION = "NOTIFICATION", "Notification"
        WELCOME = "WELCOME", "Welcome"
        LETTER = "LETTER", "Letter"

    status = models.CharField(max_length=255, db_index=True, choices=Status.choices, default=Status.READY)
    type = models.CharField(max_length=255, db_index=True, choices=Type.choices, default=Type.NOTIFICATION)
    to = models.EmailField()
    subject = models.CharField(max_length=255)
    html = models.TextField()
    plain_text = models.TextField()
    sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.type.upper()} - {self.subject} to {self.to}"
