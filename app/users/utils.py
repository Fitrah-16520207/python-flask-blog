import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail


def simpan_foto(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pic',picture_fn)
    
    output_size = (125, 125)
    gambar = Image.open(form_picture)
    gambar.thumbnail(output_size)
    gambar.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Permintaan Ubah Password', sender='noreply@demo.com',recipients=[user.email])
    msg.body = f'''Untuk mengubah password anda, kunjungi link ini:
{url_for('users.reset_token',token=token, _external=True)}

Jika anda tidak ingin membuat permintaan ubah password abaikan email ini.
'''
    mail.send(msg)



