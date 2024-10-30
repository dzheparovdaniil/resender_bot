from bot import dp, bot
from handlers import send_echo, forward_channel_messages
import asyncio
from handlers.publish_vk import router
from handlers.publish_threads import router_threads
from handlers.media_handler import router_media
from handlers.channel_messages import router_channel

async def main():
    dp.include_router(router_channel)
    dp.include_router(router)
    dp.include_router(router_threads)
    dp.include_router(router_media)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())