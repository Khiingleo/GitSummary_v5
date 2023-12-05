import secrets
import os
from PIL import Image
from gitsummary import mail
from flask_mail import Message
from flask import url_for, current_app

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    pic_filename = random_hex + f_ext
    pic_path = os.path.join(current_app.root_path, 'static/profile_pics', pic_filename)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(pic_path)
    return pic_filename

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f""" To reset your password visit the following link
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not send this request then simply ignore this message.
    """
    mail.send(msg)