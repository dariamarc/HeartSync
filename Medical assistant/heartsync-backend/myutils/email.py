from flask_mail import Message


def send_email(to, subject, template, app, mail):
    """
    Send email to recipients
    :param to: recipients list
    :param subject: subject of email
    :param template: template of email
    :param app: reference of flask server
    :param mail: reference of mail component of server
    :return:
    """
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
