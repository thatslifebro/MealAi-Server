import smtplib
import ssl
from email.message import EmailMessage

from starlette.config import Config

config = Config(".env")

SMTP_SERVER = config("SMTP_SERVER")
SMTP_SSL_PORT = config("SMTP_SSL_PORT")
SENDER_EMAIL = config("SENDER_EMAIL")
SENDER_PASSWORD = config("SENDER_PASSWORD")


def send_mail(mode: str, receiver_email: str, auth_num: str):
    sub, content = "", ""
    if mode == "find":
        sub = "MealAi 로그인 임시 비밀번호 발급"
        content = f"MealAi 로그인 임시 비밀번호 발급 \n 임시 비밀번호는 {auth_num}입니다. \n 개인 정보 보호를 위해 비밀번호를 꼭 변경해 주세요."
    elif mode == "register":
        sub = "MealAi 회원가입 이메일 인증"
        content = f"회원가입을 위한 이메일 인증번호는 {auth_num}입니다."

    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = sub
    msg.set_content(content)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_SSL_PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
