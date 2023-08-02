import asyncio
from bleak import BleakScanner, BleakClient

# pre-set the device and characteristic uuids if you know them
device_addr = None
char_uuid = None


async def choose_device():
    # allow user to choose device dynamically
    devices = await BleakScanner.discover()
    addrs = {}

    print('==== Device names ====')
    for d in devices:
        print(d.name)
        addrs[d.name] = d.address

    addr = None

    while addr == None:
        name = input('Enter device name: ')
        addr = addrs.get(name)

        if addr:
            print(f'Device address: {addr}')
        else:
            print('Invalid device name')

    return addr


async def choose_char(device):
    # allow user to choose characteristic dynamically
    chars_dict = {}
    print('==== Characteristic names ====')

    async with BleakClient(device) as client:
        svcs = await client.get_services()

        for svc in svcs:
            chars = svc.characteristics

            for char in chars:
                chars_dict[char.description] = char.uuid
                print(char.description)

    uuid = None

    while uuid == None:
        c_char = input('Enter characteristic name: ')
        uuid = chars_dict.get(c_char)

        if uuid:
            print(f'Characteristic uuid: {uuid}')
        else:
            print('Invalid characteristic name')

    return uuid


def callback(char, data):
    if ord(data.decode()[0]) != 0:
        print(f'Data recived: {data.decode()}')


async def main():
    global device_addr, char_uuid

    if device_addr == None and char_uuid == None:
        # if device address and char uuid are not known set them manually
        device = await choose_device()
        char = await choose_char(device)

        device_addr = device
        char_uuid = char

    run = True

    print('Starting connection ...')
    async with BleakClient(device_addr) as client:
        while run:
            operation = input('Read (R) / Write (W) / Quit (Q)')

            if operation == 'R':
                data = await client.read_gatt_char(char_uuid)
                print(f'Data: {data.decode()}')
            elif operation == 'W':
                data = input('Enter data to send: ')
                await client.write_gatt_char(char_uuid, data.encode('utf-8'), response=True)
            elif operation == 'Q':
                run = False
            else:
                print('You must type W (write) or R (read) or Q (quit)')

    print('Ended connection')

asyncio.run(main())
