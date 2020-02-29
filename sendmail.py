#!/usr/bin/env python3
import smtplib, ssl

# GLOBALS
PORT = 465
ADDRESS = "cute.dog.pics.daily@gmail.com"

password = input("Type password and press enter: ")
receiver_address = "bencl1998@gmail.com"

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
    server.login(email_address, password)
    server.sendmail(email_address, receiver_address, message)
