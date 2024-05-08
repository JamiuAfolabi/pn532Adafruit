import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C

# Create I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create the PN532 object
pn532 = PN532_I2C(i2c, debug=False)

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

def read_card():
    print("Waiting for NFC card...")
    while True:
        uid = pn532.read_passive_target(timeout=0.5)
        if uid is not None:
            print("Found card with UID:", [hex(i) for i in uid])
            return uid

def write_data_to_card(data):
    uid = read_card()
    if uid:
        print("Writing data to card:", data)
        success = pn532.mifare_classic_write_block(4, data, uid)
        if success:
            print("Data written successfully!")
        else:
            print("Failed to write data to card.")
    else:
        print("No card found.")

def read_data_from_card():
    uid = read_card()
    if uid:
        data = pn532.mifare_classic_read_block(4, uid)
        if data:
            print("Data read from card:", data)
        else:
            print("Failed to read data from card.")
    else:
        print("No card found.")

if __name__ == "__main__":
    while True:
        print("\n1. Read data from NFC card")
        print("2. Write data to NFC card")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            read_data_from_card()
        elif choice == "2":
            data_to_write = input("Enter data to write to NFC card: ")
            write_data_to_card(data_to_write.encode())
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
