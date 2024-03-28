from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags
from bluez_peripheral.util import *
from bluez_peripheral.advert import Advertisement
from bluez_peripheral.agent import NoIoAgent
import asyncio

class TestService(Service):
    def __init__(self):
        super().__init__("1ce7ae9b-3dc0-48ce-ae2a-f91b729fd20e", True)

    @characteristic("832cb5ef-9b89-4ca1-bad2-7769f414fb80", CharFlags.WRITE).setter
    def cricNetWriteCharacteristic(self, value, options):
        print(value)

    @characteristic("29a98ca5-b3dc-45e5-94c1-4b119a2df7b3", CharFlags.READ)
    def cricNetSyncCharacteristic(self, options):
        print("IMPORT")
        # Just return some test data; this will be piped from the scoreboard in practice.
        data = '{"2":"56.0","4":789,"7":123,"25":4,"101":80,"102":"#00ff00","103":"true","104":"#ffa500","107":"false","108":"true","api":"CN"}'
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
