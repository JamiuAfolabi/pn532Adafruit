import nfc
import time

# Create an instance of the PN532 connected via I2C
clf = nfc.ContactlessFrontend('tty:S0:pn532')

# Main loop to continuously poll for NFC tags
try:
    while True:
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        if tag:
            print("NFC Tag detected:")
            print(tag)
            # Print UID of the tag
            print("UID:", tag.identifier.hex())
            # Print the type of tag
            print("Type:", tag.type)
            # Print the data on the tag (if any)
            try:
                print("Data:", tag.ndef.message.pretty())
            except nfc.tag.tt3.Type3TagCommandError:
                print("No NDEF data found on the tag.")
            except Exception as e:
                print("Error reading tag data:", e)
        time.sleep(1)  # Pause for 1 second before polling again

except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    clf.close()
