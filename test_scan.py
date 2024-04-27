import board
import busio
from adafruit_pn532.i2c import PN532_I2C
import time

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
        print("Found card with UID:", [hex(i) for i in uid])
        
        # Attempt to read data from the card
        data = pn532.mifare_classic_read_block(4)  # Reading block 4, change as needed
        
        if data is not None:
            print("Data read successfully:", data)
        else:
            print("Failed to read data from the card")
            
            
        if data[0:2] !=  HEADER:
            print('Card is not written with proper block data!')

    # Parse out the block type and subtype
        print('User Id: {0}'.format(int(data[2:8].decode("utf-8"), 16)))
        time.sleep(DELAY)
            
        
        
    
  
        
       
    



# Main function
if __name__ == "__main__":
    try:
        while True:
            read_nfc_card()
    except KeyboardInterrupt:
        print("Exiting...")