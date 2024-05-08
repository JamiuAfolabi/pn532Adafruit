from pn532pi import Pn532, pn532

def read_card(pn532):
    print("Waiting for NFC card...")
    uid = pn532.read_passive_target()
    if uid is not None:
        print("Found card with UID:", ' '.join(format(x, '02x') for x in uid))
    return uid

def write_data_to_card(pn532, data, block_number):
    uid = read_card(pn532)
    if uid:
        print("Writing data to card:", data)
        try:
            # Authenticate with the card using default key A (0xFFFFFFFFFFFF)
            pn532.mifare_classic_authenticate_block(uid, block_number, pn532.KEY_A, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
            # Write data to the specified block
            pn532.mifare_classic_write_block(block_number, data)
            print("Data written successfully!")
        except pn532.Pn532Error as e:
            print("Failed to write data to card:", e)

def read_data_from_card(pn532, block_number):
    uid = read_card(pn532)
    if uid:
        print("Reading data from card...")
        try:
            # Authenticate with the card using default key A (0xFFFFFFFFFFFF)
            pn532.mifare_classic_authenticate_block(uid, block_number, pn532.KEY_A, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
            # Read data from the specified block
            data = pn532.mifare_classic_read_block(block_number)
            print("Data read from card:", data)
        except pn532.Pn532Error as e:
            print("Failed to read data from card:", e)

if __name__ == "__main__":
    try:
        pn532.begin()
        pn532.SAM_configuration()

        while True:
            print("\n1. Read data from NFC card")
            print("2. Write data to NFC card")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                block_number = int(input("Enter block number to read: "))
                read_data_from_card(pn532, block_number)
            elif choice == "2":
                block_number = int(input("Enter block number to write: "))
                data_to_write = input("Enter data to write to NFC card: ")
                write_data_to_card(pn532, data_to_write.encode(), block_number)
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    finally:
        pn532.close()
