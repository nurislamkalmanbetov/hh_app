from telethon.sync import TelegramClient

api_id = 21966096
api_hash = 'bb8a00f80511f8dbc54c2cc20d4d304b'

async def get_channel_id(channel_link):
    async with TelegramClient('anon', api_id, api_hash) as client:
        entity = await client.get_entity(channel_link)
        return entity.id

async def main():
    channel_link = 'https://t.me/+h77Bo1KdUBU0OWIy'  # замените на ссылку на свой канал
    channel_id = await get_channel_id(channel_link)
    print("ID канала:", channel_id)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
