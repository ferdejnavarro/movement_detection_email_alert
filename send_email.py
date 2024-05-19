import os
import smtplib
from PIL import Image
from io import BytesIO
from email.message import EmailMessage
import os

# Your sender email & its app password go here:
SENDER = 'YOUR_SENDER_EMAIL'
PASSWORD = 'YOUR_APP_PASSWORD'

# Your desired receiver email goes here:
RECEIVER = 'YOUR_RECEIVER_EMAIL'


def send_email(image_path, timestamp):
    email_msg = EmailMessage()
    email_msg["Subject"] = f"Someone caught on camera!!! At {timestamp}"
    email_msg.set_content(f'Hey, look who showed up at {timestamp}')

    with open(image_path, 'rb') as file:
        content = file.read()
    image_data = BytesIO(content)
    img = Image.open(image_data)
    image_format = img.format

    email_msg.add_attachment(content, maintype='image',
                             subtype=image_format)

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_msg.as_string())
    gmail.quit()


if __name__ == '__main__':
    send_email(image_path='images/1.png')
