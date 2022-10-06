import smtplib

from models import Session, Advertisement


if __name__ == '__main__':

    with open('email.txt') as f:
        user = f.readline().strip()
        password = f.readline().strip()

    server = "smtp.yandex.ru"
    port = 587
    charset = 'Content-Type: text/plain; charset=utf-8'
    mime = 'MIME-Version: 1.0'

    subject = 'Тест'
    text = 'Привет мир'

    with Session() as session:
        advertisements = session.query(Advertisement).all()

    for advertisement in advertisements:
        to = advertisement.email
        # формируем тело письма
        body = "\r\n".join((f"From: {user}", f"To: {to}",
                            f"Subject: {subject}", mime, charset, "", text))

        try:
            # подключаемся к почтовому сервису
            smtp = smtplib.SMTP(server, port)
            smtp.starttls()
            smtp.ehlo()
            # логинимся на почтовом сервере
            smtp.login(user, password)
            # пробуем послать письмо
            smtp.sendmail(user, to, body.encode('utf-8'))
        except smtplib.SMTPException as err:
            print('Что - то пошло не так...')
            raise err
        finally:
            smtp.quit()