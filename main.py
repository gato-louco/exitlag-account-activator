import asyncio
import ssl
from random import randint
from hashlib import sha256
import websockets
from os import system

# exitlag's websocket server uses SSL, 
# but the certificate is expired,
# so we need to ignore the security checks

# todo kluge
# HIGHLY INSECURE
ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
# HIGHLY INSECURE
# todo kluge

print("Made by GatoLouco, check https://github.com/gato-louco for updates and a tutorial")
print("This script activates a 3 days trial account for exitlag")
print("This script supposes that the password of the exitlag account's is gatolouco")
print("version v1.0")
print("")
print("This script is created for educational purposes, I am not responsible for how the script is being used.")
print("")
email = input("Insert the account's email: ")
# it is a password hash, it means 'gatolouco'. do not change it, otherwise it won't work :)
password = "38cf4d8080c1a66172c4a91e76b822140f029e10a00e3615be6eb8a0f3331ffd"  # some_hash('gatolouco'+unknow_key)


# the endpoint to connect with the websocket
_uri = "wss://ws01.exitlag.com/exitlag_client"


# func to print beautifully an byte array
def pb(_bytes, stage):
    if stage == 0:
        logo = "[SENDING]"
    else:
        logo = "[RECEIVING]"
    print("\n" + logo, end=' ')
    for _x in _bytes:
        print(hex(_x), end=', ')



# PAYLOAD

# magicbytes@hwids@hash_email_password@number_request
magicbytes = bytearray([0x32, 0xDA, 0x01, 0x1A])

# hwid is just a bunch of random numbers
hwid_1 = bytearray([0]) * 64

# generating a random HWID
for x in range(0, 64):
    hwid_1[x] = randint(0x41, 0x41 + 0xd)

# part of the payload to activate the account
resto_hwid = bytearray(
    [0x22, 0x10, 0x42, 0x46, 0x45, 0x42, 0x46, 0x42, 0x46, 0x46, 0x30, 0x30, 0x30, 0x33, 0x30, 0x36, 0x43, 0x33, 0x2A,
     0x02, 0x70, 0x74, 0x3A, 0x06, 0x34, 0x2E, 0x39, 0x35, 0x2E, 0x32, 0x42, 0x1E, 0x57, 0x69, 0x6E, 0x64, 0x6F, 0x77,
     0x73, 0x20, 0x31, 0x30, 0x20, 0x56, 0x65, 0x72, 0x73, 0x69, 0x6F, 0x6E, 0x20, 0x32, 0x30, 0x30, 0x39, 0x20, 0x36,
     0x34, 0x2D, 0x62, 0x69, 0x74, 0x4A, 0x10, 0x57, 0x69, 0x6E, 0x64, 0x6F, 0x77, 0x73, 0x20, 0x44, 0x65, 0x66, 0x65,
     0x6E, 0x64, 0x65, 0x72, 0x52, 0x00, 0x58, 0x00, 0x62])
resto_hash = bytearray([0x68, 0x10])
number_request = bytearray([0x01])

# now we hash the email + password
# and convert to bytearray
hash_email_password = sha256(email.encode() + password.encode()).hexdigest().encode()

# this byte that means '@' split the things
split_byte = bytearray([0x40])

# now we merge all there bytes into a single bytearray
big_array = bytearray(magicbytes + split_byte + hwid_1 + resto_hwid + split_byte + hash_email_password + resto_hash + split_byte + number_request)


# send function
async def initialize_ws_and_send_request():
    # initializing websocket connection with exitlag's server
    async with websockets.connect(_uri, ssl=ssl_context) as ws:
        # printing our request
        pb(big_array, 0)
        # sending it
        await ws.send(big_array)
        # waiting for the response
        response = await ws.recv()
        # priting the response
        pb(response, 1)
        system("pause")


asyncio.get_event_loop().run_until_complete(initialize_ws_and_send_request())