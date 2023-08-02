import asyncio
from bleak import BleakScanner, BleakClient
import os
from dotenv import load_dotenv

load_dotenv()

class BLEClient:
    def __init__(self, device_name):
        self.device_name = device_name
        #self.device_addr = device_address
        # self.char_uuid = characteristic_uuid
        self.characteristics = []
        self.main_service_uuid = os.environ['MAIN_SERVICE_UUID']  # Replace with your main service UUID

    async def discover_devices(self):
        devices = await BleakScanner.discover()
        return {d.name: d.address for d in devices}

    async def get_device(self):
        addrs = await self.discover_devices()

        self.device_addr = addrs.get(self.device_name)
        print (addrs)
        '''
        if self.device_addr:
            print(f'Device address: {self.device_addr}')
        else:
            raise ValueError(f'Device {self.device_address} not found in discovered devices.')
        '''
    async def get_characteristics(self):
        chars_dict = {}
        async with BleakClient(self.device_name) as client:
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
        if not self.device_name:
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
    device_name = os.environ['DEVICE_NAME']
    characteristic_uuid = "0x0001"  # Replace with the actual characteristic UUID

    client = BLEClient(device_name)
    asyncio.run(client.connect())

    # Write to the specified characteristic.
    val = "Hello, BLE!"
    asyncio.run(client.write_characteristic(characteristic_uuid, val))

    # Read from the specified characteristic.
    asyncio.run(client.read_characteristic(characteristic_uuid))
