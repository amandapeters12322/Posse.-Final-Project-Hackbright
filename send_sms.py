import os
from twilio.rest import Client
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

if __name__ == '__main__':
    from server import app
    connect_to_db(app)

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def send_event_update(event_id):
    """Sends SMS updates to event guests when a new posting is made"""
    guest_phone_numbers = crud.get_guest_phone_numbers(event_id) #gets a list of phone numbers for guests for an event
    print(guest_phone_numbers)

    for guest_phone_number in guest_phone_numbers: #loops through the list of guest phone numbers
        print(guest_phone_number)
        message = client.messages \
        .create(
            body='There is  a new comment or update in your Posse. account. Log in to check it out!',
            from_='+16127127689',
            to=guest_phone_number)

    print(message.sid)



#################################################################

