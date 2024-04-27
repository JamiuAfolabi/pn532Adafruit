import board
import busio
from adafruit_pn532.i2c import PN532_I2C
import time
import sys
import binascii


HEADER = b'BG'

DELAY = 0.5

# Create the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create an instance of the PN532 class
pn532 = PN532_I2C(i2c, debug=False)

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

# Function to read data from NFC card
def read_nfc_card():
    print("Hold a card near the reader")

    # Check if a card is present
    while not pn532.read_passive_target():
        pass

    print("Card detected")

    # Read the UID of the card
    # uid = pn532.uid
    uid = pn532.read_passive_target(timeout=0.5)
    print("Card UID:", [hex(i) for i in uid])
    
    if uid is not None:
        print('')
        print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))
        print('')
        print('==============================================================')
        print('WARNING: DO NOT REMOVE CARD FROM PN532 UNTIL FINISHED WRITING!')
        print('==============================================================')
        print('')

        data_to_write = b"Hello, NFC!"
        
        success = pn532.mifare_classic_write_block(4, data_to_write)  # Writing to block 4, change as needed
        
        if success:
            print("Data written successfully to the tag:", data_to_write)
        else:
            print("Failed to write data to the tag")

        
        
    

# Main function
if __name__ == "__main__":
    try:
        
        read_nfc_card()
    except KeyboardInterrupt:
        print("Exiting...")

                    