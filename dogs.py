#!/usr/bin/env python3
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
import requests
import sys
import os

# GLOBALS
PORT = 465
ADDRESS = "cute.dog.pics.daily@gmail.com"
NUM = 4
URL = f"https://dog.ceo/api/breeds/image/random/{NUM}"
DIR = os.path.dirname(os.path.realpath(__file__))

with open(f"{DIR}/template.html") as f:
    TEMPLATE = f.read()

# read password from file
with open(f"{DIR}/creds", "r") as f:
    PASSWORD = f.read().rstrip()

# get recepient addresses
with open(f"{DIR}/recipients.csv", "r") as f:
    CONTACTS = [ (x.split(',')[0], x.split(',')[1].strip()) for x in f.readlines()]

def get_dog_links(url=URL):
    data = requests.get(url).json()
    if data['status'] != 'success':
        print("Error getting dog links! :(")
        sys.exit(1)
    return data['message']

def construct_message(recipient, links):
    (name, r_addr) = recipient
    message = MIMEMultipart("alternative")
    message["Subject"] = "Daily Dog Dose -- {}".format(date.today().strftime("%m/%d/%y"))
    message["From"] = ADDRESS
    message["To"] = r_addr

    text = """\
            Good morning {name}!
            Here are our dogs of the day!!
            {link1}

            {link2}

            {link3}

            {link4}
            """.format(name=name, link1=links[0], link2=links[1], link3=links[2], link4=links[3])
    html = TEMPLATE.format(name=name, link1=links[0], link2=links[1], link3=links[2], link4=links[3])

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    return message

LINKS = get_dog_links()
# actually send the emails now
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
    server.login(ADDRESS, PASSWORD)
    for contact in CONTACTS:
        message = construct_message(contact, LINKS)
        server.sendmail(ADDRESS, contact[1], message.as_string())
