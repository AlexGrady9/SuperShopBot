

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from handlers.user_handlers import router as user_router
# from handlers.order_handlers import router as order_router
# from handlers.feedback_handlers import router as feedback_router
# from admin.admin_handlers import router as admin_router

# Temporary for testing: insert your real token below
API_TOKEN = '8358839439:AAFULVaqcCAsQ_Qzvmtddq0lHB41uIY96fM'

logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Register routers
dp.include_router(user_router)
# dp.include_router(order_router)
# dp.include_router(feedback_router)
# dp.include_router(admin_router)


async def set_commands():
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="menu", description="Show main menu"),
        BotCommand(command="orders", description="My orders"),
        BotCommand(command="feedback", description="Leave feedback")
    ]
    await bot.set_my_commands(commands)


async def main():
    print("SuperShopBot is starting... Press Ctrl+C to stop.")
    await set_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
