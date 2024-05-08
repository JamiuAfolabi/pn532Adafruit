import board
import busio
from adafruit_pn532.i2c import PN532_I2C
import time
import binascii
import sys

key = b'\xFF\xFF\xFF\xFF\xFF\xFF'
MIFARE_CMD_AUTH_B = 0x61
block_number = 4

HEADER = b'BG'

DELAY = 0.5

# Create the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create an instance of the PN532 class
pn532 = PN532_I2C(i2c, debug=False)

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

# Step 1, wait for card to be present.
print('PN532 NFC Module Writer')
print('')
print('== STEP 1 =========================')
print('Place the card to be written on the PN532...')
uid = pn532.read_passive_target()
while uid is None:
    uid = pn532.read_passive_target()
print('')
print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))
print('')
print('==============================================================')
print('WARNING: DO NOT REMOVE CARD FROM PN532 UNTIL FINISHED WRITING!')
print('==============================================================')
print('')

# Step 2, pick a block type.
print('== STEP 2 =========================')
block_choice = None
while block_choice is None:
    print('')
    block_choice = input('Enter user ID: ')
    try:
        block_choice = int(block_choice)
    except ValueError:
        print('Error! Unrecognized option.')
        continue
    # Decimal value not greater than hex number with 6 digits
    if not (0 <= block_choice < 16777215):
        print('Error! User ID must be within 0 to 4294967295.')
        continue
    print('')
print('You chose the block type: {0}'.format(block_choice))
print('')

# Confirm writing the block type.
print('== STEP 3 =========================')
print('Confirm you are ready to write to the card:')
print('User ID: {0}'.format(block_choice))
choice = input('Confirm card write (Y or N)? ')
if choice.lower() != 'y' and choice.lower() != 'yes':
    print('Aborted!')
    sys.exit(0)
print('Writing card (DO NOT REMOVE CARD FROM PN532)...')

# Write the card!
# First authenticate block 4.
if pn532.mifare_classic_authenticate_block(uid, block_number, MIFARE_CMD_AUTH_B, key):
            print("Authentication successful!")
else:
    print("Authentication failed.")
# Next build the data to write to the card.
# Format is as follows:
# - 2 bytes 0-1 store a header with ASCII value, for example 'BG'
# - 6 bytes 2-7 store the user data, for example user ID
data = bytearray(16)
# Add header
data[0:2] = HEADER
# Convert int to hex string with up to 6 digits
value = format(block_choice, 'x')
while (6 > len(value)):
    value = '0' + value
data[2:8] = value
# Finally write the card.
if not pn532.mifare_classic_write_block(4, data):
    print('Error! Failed to write to the card.')
    sys.exit(-1)
print('Wrote card successfully! You may now remove the card from the PN532.')