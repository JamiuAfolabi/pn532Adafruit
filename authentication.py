import board
import busio
from adafruit_pn532.i2c import PN532_I2C

# Define MIFARE Classic authentication command
MIFARE_CMD_AUTH_B = 0x61

# Create I2C connection
i2c = busio.I2C(board.SCL, board.SDA)

# Create PN532 object
pn532 = PN532_I2C(i2c, debug=False)

# Configure PN532 to communicate with MIFARE cards
pn532.SAM_configuration()

# Define the key and block to authenticate
key = b'\xFF\xFF\xFF\xFF\xFF\xFF'
block_number = 4

# Authenticate with MIFARE Classic card
uid = pn532.read_passive_target()

if uid:
    print("Found card with UID:", [hex(i) for i in uid])

    # Try to authenticate with the card
    if pn532.mifare_classic_authenticate_block(uid, block_number, MIFARE_CMD_AUTH_B, key):
        print("Authentication successful!")
    else:
        print("Authentication failed.")
else:
    print("No card detected.")
