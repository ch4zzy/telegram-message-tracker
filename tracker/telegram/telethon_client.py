import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from celery.signals import worker_process_init, worker_shutdown


class TelethonClient:
    def __init__(self, api_id, api_hash, session):
        """
        Init client
        :param api_id: ID API Telegram.
        :param api_hash: Hash API Telegram.
        :param session: StringSession Telegram.
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.session = session
        self.client = TelegramClient(StringSession(session), api_id, api_hash)
        self.loop = asyncio.get_event_loop()

    async def start(self):
        """Starts the Telegram client."""
        try:
            await self.client.connect()
        except Exception as e:
            raise e

    async def stop(self):
        """Disconnects the Telegram client."""
        try:
            await self.client.disconnect()
        except Exception as e:
            raise e

    @worker_process_init.connect
    def on_worker_start(self, *args, **kwargs):
        try:
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self.start())
        except Exception as e:
            raise e

    @worker_shutdown.connect
    def on_worker_shutdown(self, *args, **kwargs):
        try:
            self.loop.run_until_complete(self.stop())
        except Exception as e:
            raise e

    def get_client(self):
        """Returns the Telegram client instance if it is connected."""
        if self.client.is_connected():
            return self.client
        raise RuntimeError("Telegram client is not connected.")
    
    def set_client(self):
        self.on_worker_start()
    
    def get_loop(self):
        """Returns the event loop."""
        return self.loop
    

