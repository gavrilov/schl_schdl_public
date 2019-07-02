import configparser
import datetime
import os
import webbrowser
from time import sleep

import serial

"""
This is separate module to connect external analog usb modem as USRobotics 5637 to use CallerID of landline and open url of user's profile
To create exe file:
pip install pyserial
pip install pyinstaller
pyinstaller --onefile modem.py
"""

# Print copyright information
print("\r\n\r\n")
print("****************************************************************************")
print("*   Trex Technologies LLC (c) 2019 - Konstantin Gavrilov info@trxtch.com   *")
print("****************************************************************************")
print("\r\n\r\n")

# Create default Config file or load if we already have one
config = configparser.ConfigParser()
config.read('config.ini')

if not os.path.exists('config.ini'):
    print("Creating new config file... Please edit config.ini and restart to apply")
    config['DEFAULT'] = {'DEBUG': False, 'DO_NOT_OPEN_BROWSER': False, 'LOGGING': True, 'LOGGING_LEVEL': 'WARNING',
                         'PORT': 'COM3', 'SPEED': '9600',
                         'BASE_URL': 'https://registration.enrichmentservices.com/user/phone/'}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

print("Reading from config file...\r\n")

DEBUG = config['DEFAULT']['DEBUG']
print(f"Debug mode: {DEBUG}")

# TODO Logging to file
LOGGING = config['DEFAULT']['LOGGING']
LOGGING_LEVEL = config['DEFAULT']['LOGGING_LEVEL']
DO_NOT_OPEN_BROWSER = config['DEFAULT']['DO_NOT_OPEN_BROWSER']

PORT = config['DEFAULT']['PORT']
SPEED = config['DEFAULT']['SPEED']
BASE_URL = config['DEFAULT']['BASE_URL']
print(f"Looking for modem at {PORT}:{SPEED}")

# Initial Modem
ser = serial.Serial(PORT, SPEED, timeout=0, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS)
ser.flushInput()
ser.flushOutput()

print(f"Connected to {ser.name}")

if DEBUG == 'True':
    print(f"Base url: {BASE_URL}<phone_number>")
    print('List of commands for US5637 https://support.usr.com/support/5637/5637-ug/ref_data.html')

# Show modem version
ser.write(b'AT+FMM\r\n')


# Enables unformatted Caller ID.
# ser.write(b'AT#CID=2\r\n')


def getCommands(data):
    data = data.decode('ascii')
    commands = data.split('\r\n')
    for command in commands:
        if command:
            # TODO if CALLERID in command call open_url(number) to proceed
            now = datetime.datetime.now().isoformat()
            print(f"{now} == {command}")
    commands = ""


def open_url(number):
    if DO_NOT_OPEN_BROWSER == "False":
        webbrowser.open_new_tab(str(BASE_URL) + str(number))


# Main loop - we are waiting for modem response
while True:
    try:
        data = None
        queue = ser.inWaiting()

        if queue > 0:
            data = ser.read(1000)
        sleep(0.2)

        # if we got data, try to find commands
        if data:
            getCommands(data)

        if DEBUG == 'True':
            req = input('Enter Command: ')
            req_bytes = req.encode('ascii')
            ser.write(req_bytes + b'\r\n')
        else:
            pass
    except Exception as e:
        # TODO ADD TO LOGGER
        print(e)
