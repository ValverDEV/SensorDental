import serial

# configuración serial
serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = 'COM3'
serialInst.open()


def serial_get_temp():
    packet = serialInst.readline()
    packet = float(packet.decode('utf')[:-2])
    print(packet)
    return packet
