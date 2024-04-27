import board
import busio
from adafruit_pn532.i2c import PN532_I2C

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
    



# Main function
if __name__ == "__main__":
    try:
        while True:
            read_nfc_card()
    except KeyboardInterrupt:
        print("Exiting...")
