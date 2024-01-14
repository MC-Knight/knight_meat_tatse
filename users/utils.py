from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_verification_email(email, pk, token):
    try:
        subject = "welcome to Mentor [Update]"
        message = "Hello"
        email_from = f"{settings.DISPLAY_NAME} <settings.EMAIL_HOST_USER>"
        recipient_list = [
            email,
        ]
        html_c = get_template("mail.html")
        context = {
            "token": token,
            "url": f"{settings.CLIENT_URL}/account/verify-email/{token}/",
        }
        html_content = html_c.render(context)
        # headers = {'X-Auto-Response-Suppress': 'Update',
        #            'List-Unsubscribe': '<mailto:unsubscribe@example.com>'
        # }
        msg = EmailMultiAlternatives(subject, message, email_from, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        print(e)
        return False

    return True


def send_reset_password_email(email, token):
    try:
        subject = "Reset your password [Update]"
        message = "Hello again"
        email_from = f"{settings.DISPLAY_NAME} <settings.EMAIL_HOST_USER>"
        recipient_list = [
            email,
        ]
        html_c = get_template("forget_password.html")
        context = {
            "token": token,
            "url": f"{settings.CLIENT_URL}/account/reset-password/{token}",
        }
        html_content = html_c.render(context)
        # headers = {'X-Auto-Response-Suppress': 'Update',
        #            'List-Unsubscribe': '<mailto:unsubscribe@example.com>'
        # }
        msg = EmailMultiAlternatives(subject, message, email_from, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        print(e)
        return False

    return True
