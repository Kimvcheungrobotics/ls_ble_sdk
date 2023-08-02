# ble_client.py

import asyncio
from bleak import BleakScanner, BleakClient
import os
from dotenv import load_dotenv

load_dotenv()

class BLEClient:
    def __init__(self, device_address):
        # self.device_name = device_name
        self.device_addr = device_address
        # self.char_uuid = characteristic_uuid
        self.characteristics = []
        self.main_service_uuid = os.environ['MAIN_SERVICE_UUID']  # Replace with your main service UUID

    async def discover_devices(self):
        devices = await BleakScanner.discover()
        return {d.name: d.address for d in devices}

    async def choose_device(self):
        addrs = await self.discover_devices()

        self.device_addr = addrs.get(self.device_address)
        print (addrs)
        '''
        if self.device_addr:
            print(f'Device address: {self.device_addr}')
        else:
            raise ValueError(f'Device {self.device_address} not found in discovered devices.')
        '''
    async def get_characteristics(self):
        chars_dict = {}
        async with BleakClient(self.device_addr) as client:
            svcs = await client.get_services()

            for svc in svcs:
                if svc.uuid == self.main_service_uuid:
                    self.characteristics = svc.characteristics
                    break

        if not self.characteristics:
            raise ValueError('No characteristics found in the main service.')

        """for char in self.characteristics:
            chars_dict[char.description] = char.uuid
            print(f'{char.description}: {char.uuid}')

        self.char_uuid = chars_dict.get(self.char_uuid)
        if self.char_uuid:
            print(f'Selected characteristic uuid: {self.char_uuid}')
        else:
            raise ValueError(f'Characteristic "{self.char_uuid}" not found.')"""

    async def connect(self):
        if not self.device_addr:
            await self.get_device()
        if not self.characteristics:
            await self.get_characteristics()

    async def write_characteristic(self, char_uuid, data_to_write):
        async with BleakClient(self.device_addr) as client:
            await client.write_gatt_char(char_uuid, data_to_write.encode('utf-8'), response=True)

    async def read_characteristic(self, char_uuid):
        async with BleakClient(self.device_addr) as client:
            data = await client.read_gatt_char(char_uuid)
            print(f'Data: {data.decode()}')

    """def callback(self, char, data):
        if ord(data.decode()[0]) != 0:
            print(f'Data received: {data.decode()}')"""

# Example Usage:
if __name__ == "__main__":
    device_address = os.environ['DEVICE_ADDRESS']
    characteristic_uuid = "0x0001"  # Replace with the actual characteristic UUID

    client = BLEClient(device_address)
    asyncio.run(client.connect())

    # Write to the specified characteristic.
    val = "Hello, BLE!"
    asyncio.run(client.write_characteristic(characteristic_uuid, val))

    # Read from the specified characteristic.
    asyncio.run(client.read_characteristic(characteristic_uuid))



"""import asyncio
from bleak import BleakScanner, BleakClient
import os
from dotenv import load_dotenv

load_dotenv()

class BLEClient:
    def __init__(self, device_address):
        #self.device_name = device_name
        self.device_addr = device_address
        #self.char_uuid = characteristic_uuid
        self.characteristics = []

    async def discover_devices(self):
        devices = await BleakScanner.discover()
        return {d.name: d.address for d in devices}

    async def choose_device(self):
        addrs = await self.discover_devices()

        self.device_addr = addrs.get(self.device_address)
        if self.device_addr:
            print(f'Device address: {self.device_addr}')
        else:
            raise ValueError(f'Device {self.device_address} not found in discovered devices.')

    async def choose_characteristic(self):
        chars_dict = {}
        async with BleakClient(self.device_addr) as client:
            svcs = await client.get_services()

            for svc in svcs: 
                if(svc != main_service):
                    break
                
                # add code to skip unneeded services
                self.characteristics = svc.characteristics

                '''
                for char in chars:
                    chars_dict[char.description] = char.uuid
                    print(char.description)
                '''
        self.char_uuid = chars_dict.get(self.char_uuid)
        if self.char_uuid:
            print(f'Characteristic uuid: {self.char_uuid}')
        else:
            raise ValueError(f'Characteristic "{self.char_uuid}" not found.')

    async def connect(self):
        if not self.device_addr:
            await self.choose_device()
        if not self.char_uuid:
            await self.choose_characteristic()

    async def write_characteristic(self, char_uuid, data_to_write):
        async with BleakClient(self.device_addr) as client:
            await client.write_gatt_char(self.char_uuid, data_to_write.encode('utf-8'), response=True)

    async def read_characteristic(self):
        async with BleakClient(self.device_addr) as client:
            data = await client.read_gatt_char(self.char_uuid)
            print(f'Data: {data.decode()}')

    def callback(self, char, data):
        if ord(data.decode()[0]) != 0:
            print(f'Data received: {data.decode()}')

# Example Usage:
if __name__ == "__main__":
    device_name = "LittleSophia"
    device_address = "00:11:22:33:AA:BB"  # Replace with the actual device address
    characteristic_uuid = "Your_Characteristic_UUID"  # Replace with the actual characteristic UUID

    client = BLEClient(device_name, device_address, characteristic_uuid)
    asyncio.run(client.connect())

    # Write to the specified characteristic.
    val = "Hello, BLE!"
    asyncio.run(client.write_characteristic(val))

    # Read from the specified characteristic.
    asyncio.run(client.read_characteristic())"""

"""import asyncio
from bleak import BleakScanner, BleakClient
import os
from dotenv import load_dotenv

load_dotenv()

class BLEClient:
    def __init__(self):
        self.device_addr = os.getenv("DEVICE_ADDRESS")
        self.char_uuid = os.getenv("CHARACTERISTIC_UUID")

    async def discover_devices(self):
        devices = await BleakScanner.discover()
        return {d.name: d.address for d in devices}

    async def choose_device(self):
        addrs = await self.discover_devices()

        while True:
            name = input('Enter device name: ')
            addr = addrs.get(name)

            if addr:
                print(f'Device address: {addr}')
                self.device_addr = addr
                break
            else:
                print('Invalid device name')

    async def choose_characteristic(self):
        chars_dict = {}

        async with BleakClient(self.device_addr) as client:
            svcs = await client.get_services()

            for svc in svcs:
                chars = svc.characteristics

                for char in chars:
                    chars_dict[char.description] = char.uuid
                    print(char.description)

        while True:
            c_char = input('Enter characteristic name: ')
            uuid = chars_dict.get(c_char)

            if uuid:
                print(f'Characteristic uuid: {uuid}')
                self.char_uuid = uuid
                break
            else:
                print('Invalid characteristic name')

    def callback(self, char, data):
        if ord(data.decode()[0]) != 0:
            print(f'Data received: {data.decode()}')

    async def read_characteristic(self):
        async with BleakClient(self.device_addr) as client:
            data = await client.read_gatt_char(self.char_uuid)
            print(f'Data: {data.decode()}')

    async def write_characteristic(self):
        data = input('Enter data to send: ')
        async with BleakClient(self.device_addr) as client:
            await client.write_gatt_char(self.char_uuid, data.encode('utf-8'), response=True)

    def run(self):
        loop = asyncio.get_event_loop()
        run = True

        print('Starting connection ...')
        while run:
            operation = input('Read (R) / Write (W) / Quit (Q): ')

            if operation == 'R':
                loop.run_until_complete(self.read_characteristic())
            elif operation == 'W':
                loop.run_until_complete(self.write_characteristic())
            elif operation == 'Q':
                run = False
            else:
                print('You must type W (write) or R (read) or Q (quit)')

        print('Ended connection')"""

        
