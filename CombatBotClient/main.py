import serial


def main():
    with serial.Serial('/dev/tty.usbserial-0001', 115200) as ser:
        x = ser.read(10)
        print(x)


if __name__ == "__main__":
    main()
