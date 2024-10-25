from bot import dp, bot
from handlers import send_echo, forward_channel_messages
import asyncio
from handlers.publish_vk import router
from handlers.publish_threads import router_threads

async def main():
    dp.channel_post.register(forward_channel_messages)
    dp.message.register(send_echo)
    dp.include_router(router)
    dp.include_router(router_threads)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())