# ble_client.py

import asyncio
from bleak import BleakScanner, BleakClient
import os


class BLEClient:
    def __init__(self, device_name, main_service):
        self.main_service = main_service  # uuid of main service
        self.device_name = device_name  # name of device to connect to
        self.characteristics = []  # list of all characteristics
        self.target_device_addr = None  # uuid of target device

    async def discover_devices(self):
        # list the device names and their addresses
        devices = await BleakScanner.discover()
        d_dict = {d.name: d.address for d in devices}
        return d_dict

    async def select_device(self, device_name):
        # select the device
        addrs = await self.discover_devices()
        target_addr = addrs.get(device_name)

        if target_addr:
            print(f'Device found. Device address: {target_addr}')
            return target_addr
        else:
            raise ValueError(
                f'Device {device_name} not found in discovered devices.')

    async def show_services(self):
        async with BleakClient(self.target_device_addr) as client:
            svcs = await client.get_services()

            for svc in svcs:
                print(svc.uuid, svc.description)

    async def get_characteristics(self):
        async with BleakClient(self.target_device_addr) as client:
            svcs = await client.get_services()
            found = False

            for svc in svcs:
                # skip uneeded services
                if (svc.uuid == self.main_service):
                    # get characteristics from main service
                    self.characteristics = [
                        [char.description, char.uuid, char.handle] for char in svc.characteristics]

                    print('Got characteristics')
                    found = True
                    break

            if not found:
                raise ValueError('Main service was not found')

    def show_chars(self):
        # show characteristics visible for main service
        print('\nCharacteristics available (description, uuid, handle)')

        for desc, uuid, handle in self.characteristics:
            print(desc, uuid, handle)

        print('\n\n')

    async def connect(self):
        if not self.target_device_addr:
            self.target_device_addr = await self.select_device(self.device_name)
            await self.get_characteristics()

        self.show_chars()

    async def write_characteristic(self, data, char_uuid):
        # char_uuid is the characteristic to write to
        async with BleakClient(self.target_device_addr) as client:
            await client.write_gatt_char(char_uuid, data.encode('utf-8'), response=True)

    async def read_characteristic(self, char_uuid):
        # char_uuid is the characteristic to write to
        async with BleakClient(self.target_device_addr) as client:
            data = await client.read_gatt_char(char_uuid)

            if type(data) == bytearray:
                data = int.from_bytes(data, byteorder='big')
                print(f'Data: {data}')
            else:
                print(f'Data: {data.decode()}')


async def get_services(device_name):
    # list the services of a device
    devices = await BleakScanner.discover()
    d_dict = {d.name: d.address for d in devices}
    target_addr = d_dict.get(device_name)

    print('Services available for device: ')
    async with BleakClient(target_addr) as client:
        svcs = await client.get_services()

        for svc in svcs:
            print(svc.description, svc.uuid)


# Example Usage:
if __name__ == "__main__":
    # name of device, you don't need the address if you have the name
    device_name = 'LS2045'
    main_service_uuid = '0000180f-0000-1000-8000-00805f9b34fb'  # uuid of the main service
    target_char = '00002a19-0000-1000-8000-00805f9b34fb'
    client = BLEClient(device_name, main_service_uuid)
    asyncio.run(client.connect())
    client.show_chars()
    asyncio.run(client.read_characteristic(target_char))
