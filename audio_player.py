# audio_player.py

import asyncio
from bleak import BleakScanner, BleakClient

class AudioPlayer:
    def __init__(self, device_name, device_addr):
        self.device_addr = device_addr
        self.audio_cmd_uuid = "0001"
        self.audio_data_uuid = "0004"
        self.client = None

    async def connect(self):
        self.client = BleakClient(self.device_addr)
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()

    async def audio_write_cmd(self, data_byte):
        if self.client.is_connected:
            await self.client.write_gatt_char(self.audio_cmd_uuid, bytes([data_byte]), response=True)

    async def audio_write_data(self, data_byte):
        if self.client.is_connected:
            await self.client.write_gatt_char(self.audio_data_uuid, bytes([data_byte]), response=True)

async def main():
    device_name = "Your Device Name"
    device_addr = "XX:XX:XX:XX:XX:XX"

    audio_player = AudioPlayer(device_name, device_addr)
    await audio_player.connect()

    # For demonstration purposes, let's send some example audio data
    example_data = b'\x01\x02\x03'  # Replace this with your actual audio data
    for data_byte in example_data:
        await audio_player.audio_write_data(data_byte)

    await audio_player.disconnect()

if __name__ == "__main__":
    asyncio.run(main())




"""import asyncio
from bleak import BleakClient

class AudioPlayer:
    def __init__(self):
        self.device_addr = None
        self.audio_cmd_uuid = "0001"
        self.audio_data_uuid = "0004"
        self.client = None

    async def choose_device(self):
        devices = await BleakScanner.discover()
        addrs = {}

        print('==== Device names ====')
        for d in devices:
            print(d.name)
            addrs[d.name] = d.address

        while self.device_addr is None:
            name = input('Enter device name: ')
            self.device_addr = addrs.get(name)

            if self.device_addr:
                print(f'Device address: {self.device_addr}')
            else:
                print('Invalid device name')

    async def connect(self):
        self.client = BleakClient(self.device_addr)
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()

    async def audio_write_cmd(self, data_byte):
        if self.client.is_connected:
            await self.client.write_gatt_char(self.audio_cmd_uuid, bytes([data_byte]), response=True)

    async def audio_write_data(self, data_byte):
        if self.client.is_connected:
            await self.client.write_gatt_char(self.audio_data_uuid, bytes([data_byte]), response=True)

async def main():
    audio_player = AudioPlayer()
    await audio_player.choose_device()
    await audio_player.connect()

    # For demonstration purposes, let's send some example audio data
    example_data = b'\x01\x02\x03'  # Replace this with your actual audio data
    for data_byte in example_data:
        await audio_player.audio_write_data(data_byte)

    await audio_player.disconnect()

if __name__ == "__main__":
    asyncio.run(main())"""


"""import asyncio
from bleak import BleakScanner, BleakClient

class AudioPlayer:
    def __init__(self):
        self.device_addr = None
        self.audio_cmd_uuid = 0x0001
        self.audio_data_uuid = 0x0004

    async def choose_device(self):
        devices = await BleakScanner.discover()
        addrs = {}

        print('==== Device names ====')
        for d in devices:
            print(d.name)
            addrs[d.name] = d.address

        while self.device_addr is None:
            name = input('Enter device name: ')
            self.device_addr = addrs.get(name)

            if self.device_addr:
                print(f'Device address: {self.device_addr}')
            else:
                print('Invalid device name')

    async def connect(self):
        self.client = BleakClient(self.device_addr)
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()

    async def audio_write_cmd(self, data_byte):
        if self.client.is_connected:
            await self.client.write_gatt_char(self.audio_cmd_uuid, bytes([data_byte]), response=True)

    async def audio_write_data(self, data_byte):
        if self.client.is_connected:
            await self.client.write_gatt_char(self.audio_data_uuid, bytes([data_byte]), response=True)

    def callback(self, char, data):
        if ord(data.decode()[0]) != 0:
            print(f'Data received: {data.decode()}')

    async def run(self):
        await self.choose_device()
        await self.connect()

        run = True
        print('Starting connection ...')

        while run:
            operation = input('Send audio command (C) / Send audio data (D) / Quit (Q)')

            if operation == 'C':
                data_byte = int(input('Enter audio command (as a byte): '))
                await self.audio_write_cmd(data_byte)
            elif operation == 'D':
                data_byte = int(input('Enter audio data (as a byte): '))
                await self.audio_write_data(data_byte)
            elif operation == 'Q':
                run = False
            else:
                print('Invalid option')

        await self.disconnect()
        print('Ended connection')

if __name__ == "__main__":
    asyncio.run(AudioPlayer().run())"""
