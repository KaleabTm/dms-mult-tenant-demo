from datetime import timezone

from celery import shared_task
from celery.utils.log import get_task_logger

from .models import Email
from .services import email_failed, email_send_attachment, email_send_type

logger = get_task_logger(__name__)


def _email_send_failure(self, exc, task_id, args, kwargs, einfo):
    email_id = kwargs.get("email_id")  # Fetch email ID
    if email_id:
        try:
            email = Email.objects.get(id=email_id)
            email_failed(email)  # Handle failure properly
        except Email.DoesNotExist:
            logger.warning(f"Email with ID {email_id} not found in failure handler.")
        except Exception as e:
            logger.warning(f"Failed to mark email ID {email_id} as failed: {e}")


# @shared_task(bind=True, on_failure=_email_send_failure)
# def email_send(self, to, subject):
#     try:
#         email_send(to, subject)
#     except Exception as exc:
#         # https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
#         logger.warning(f"Exception occurred while sending email: {exc}")
#         self.retry(exc=exc, countdown=5)


# @shared_task(bind=True)
# def email_send_all(self, tos):
#     """
#     Sends emails to multiple recipients.

#     :param tos: List of email IDs to send
#     """
#     for to in tos:
#         try:
#             email = Email.objects.get(id=to)
#             email_send(email)  # Call the existing email_send service
#         except Email.DoesNotExist:
#             self.retry(exc=Exception(f"Email with ID {to} does not exist."), countdown=5)
#         except Exception as exc:
#             logger.warning(f"Failed to send email ID {to}: {exc}")
#             self.retry(exc=exc, countdown=5)


@shared_task(bind=True, on_failure=_email_send_failure)
def email_send_task(self, to: str, subject: str, template_name: str, context: dict, email_id=None):
    try:
        html_content = email_send_type(to, subject, template_name, context)

        # Update the existing email record instead of creating a new one
        if email_id:
            Email.objects.filter(id=email_id).update(
                status=Email.Status.SENT,
                html=html_content,
                sent_at=timezone.now(),
            )

    except Exception as exc:
        logger.warning(f"Exception occurred while sending email: {exc}")
        self.retry(exc=exc, countdown=5, kwargs={"email_id": email_id})


@shared_task(bind=True, on_failure=_email_send_failure)
def email_send_with_attahcment_task(
    self,
    to: str,
    subject: str,
    template_name: str,
    context: dict,
    file_path: str,
    file_name,
    email_id=None,
):
    try:
        html_content = email_send_attachment(
            to,
            subject,
            template_name,
            context,
            file_path,
            file_name,
        )
        # Update the existing email record instead of creating a new one
        if email_id:
            Email.objects.filter(id=email_id).update(
                status=Email.Status.SENT,
                html=html_content,
                sent_at=timezone.now(),
            )

    except Exception as exc:
        logger.warning(f"Exception occurred while sending email: {exc}")
        self.retry(exc=exc, countdown=5)
