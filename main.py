# main.py

from ble_client import BLEClient

if __name__ == "__main__":
    client = BLEClient()
    if not client.device_addr or not client.char_uuid:
        client.choose_device()
        client.choose_characteristic()
    client.run()

# main.py

import asyncio
from audio_player import AudioPlayer

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
    asyncio.run(main())
