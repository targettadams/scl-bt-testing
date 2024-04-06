from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags
from bluez_peripheral.util import *
from bluez_peripheral.advert import Advertisement
from bluez_peripheral.agent import NoIoAgent
import asyncio
import json

command_label_mapping = {}
command_label_mapping["0x07"] = "Total"
command_label_mapping["0x19"] = "Wickets"
command_label_mapping["0x02"] = "Over"
command_label_mapping["0x09"] = "To Win"
command_label_mapping["0x0B"] = "Batter 1 Score"
command_label_mapping["0x0F"] = "Batter 2 Score"
command_label_mapping["0x65"] = "Brightness"
command_label_mapping["0x66"] = "Default colour"
command_label_mapping["0x68"] = "To Win colour"
command_label_mapping["0x6C"] = "Wickets switched on"
command_label_mapping["0x6B"] = "To Win switched on"
command_label_mapping["0x67"] = "To Win colour enabled"

class TestService(Service):
    def __init__(self):
        super().__init__("1ce7ae9b-3dc0-48ce-ae2a-f91b729fd20e", True)

    @characteristic("832cb5ef-9b89-4ca1-bad2-7769f414fb80", CharFlags.WRITE).setter
    def cricNetWriteCharacteristic(self, value, options):
        try:
            json_data = json.loads(value.decode('utf-8'))
        except:
            print("Problem parsing JSON data.")
            raise
        print("*******")
        for key in json_data:
            if (key not in command_label_mapping):
                raise NotImplementedError(f"Unsupported command: {key}")
            else:
                print(f"{command_label_mapping[key]} set to {json_data[key]}")

    @characteristic("29a98ca5-b3dc-45e5-94c1-4b119a2df7b3", CharFlags.READ)
    def cricNetSyncCharacteristic(self, options):
        print("IMPORT")
        # Just return some test data; this will be piped from the scoreboard in practice.
        data = '{"0x07":"123","0x19":"4","0x02":"89","0x09":"567","0x0B":"12","0x0F":"34","0x65":"50","0x66":"#ffffff","0x68":"#0000ff","0x6C":"true","0x6B":"true","0x67":"true"}'
        return data.encode('utf-8')

async def main():
    bus = await get_message_bus()

    service = TestService()
    await service.register(bus)

    agent = NoIoAgent()
    await agent.register(bus)

    adapter = await Adapter.get_first(bus)

    advert = Advertisement("ScoreLite-Link", [], 0x0140, 0)
    await advert.register(bus, adapter)

    while True:
        await asyncio.sleep(5)

    await bus.wait_for_disconnect()

if __name__ == "__main__":
    asyncio.run(main())
