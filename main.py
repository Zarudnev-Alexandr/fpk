from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import DialogManager, StartMode, setup_dialogs
from environs import Env

from database.engine import drop_db, create_db, session_maker
from dialogs.add_film import enter_film_dialog, watch_all_films_dialog
from dialogs.get_film_by_code import get_film_by_code_dialog
from dialogs.start import start_dialog
from dialogs.subscribe import subscribe_dialog
from middlewares.db import DataBaseSession
from states import StartSG

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start_check_auth, mode=StartMode.RESET_STACK)


dp.include_router(start_dialog)
dp.include_router(enter_film_dialog)
dp.include_router(watch_all_films_dialog)
dp.include_router(subscribe_dialog)
dp.include_router(get_film_by_code_dialog)
setup_dialogs(dp)


async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('бот лег')


dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)

dp.update.middleware(DataBaseSession(session_pool=session_maker))
dp.callback_query.middleware(CallbackAnswerMiddleware())


dp.run_polling(bot)

