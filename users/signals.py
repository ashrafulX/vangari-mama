from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def account_activation_email(sender, instance, created, **kwargs):

    if created and not instance.is_active:

        token = default_token_generator.make_token(instance)

        activation_url = (
            f"{settings.BACKEND_URL}"
            f"/users/activate/{instance.id}/{token}/"
        )

        subject = "Activate Your Vangari Mama Account"

        html_message = render_to_string(
            "emails/account_activation.html",
            {
                "first_name": instance.first_name,
                "username": instance.username,
                "activation_url": activation_url,
            }
        )

        text_message = (
            f"Hi {instance.first_name},\n\n"
            f"Please activate your Vangari Mama account."
        )

        try:
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[instance.email],
            )

            email.attach_alternative(
                html_message,
                "text/html"
            )

            email.send()

        except Exception as e:
            print(
                f"Failed to send mail to "
                f"{instance.email}: {str(e)}"
            )