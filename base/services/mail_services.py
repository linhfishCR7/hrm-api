from django.core.mail import EmailMessage

def email_service(subject, message, email_from, recipient_list):
    msg = EmailMessage(subject, message, email_from, recipient_list)
    msg.content_subtype = 'html'
    msg.send()
