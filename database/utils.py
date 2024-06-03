from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Film, SubscribeChannel
from states import EnterFilmSG, AllFilmsSG, StartSG, SubscribesSG, GetFilmByCodeSG


async def switch_to_enter_film(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.done()
    await dialog_manager.start(state=EnterFilmSG.enter_name)


async def switch_to_get_films(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.done()
    await dialog_manager.start(state=AllFilmsSG.all_films_start)


async def film_selection(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        item_id: str
):
    ctx = manager.current_context()
    ctx.dialog_data.update(selected_film_id=item_id)
    await manager.switch_to(AllFilmsSG.film_info)


async def del_film(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager):

    ctx = dialog_manager.current_context()
    film_id = int(ctx.dialog_data['selected_film_id'])

    session: AsyncSession = dialog_manager.middleware_data.get('session')
    stmt = (delete(Film).where(Film.id == film_id))

    await session.execute(stmt)
    await session.commit()

    ctx.dialog_data.update(selected_film_id='')
    await dialog_manager.back()


async def switch_to_main_menu(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.done()
    await dialog_manager.start(state=StartSG.start_check_auth)


async def switch_to_subscribes(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.done()
    await dialog_manager.start(state=SubscribesSG.start)


async def channel_selection(
        callback: CallbackQuery,
        widget: Select,
        manager: DialogManager,
        item_id: str
):
    ctx = manager.current_context()
    ctx.dialog_data.update(selected_channel_id=item_id)
    await manager.switch_to(SubscribesSG.change_one_channel)


async def del_channel(callback: CallbackQuery,
                   button: Button,
                   dialog_manager: DialogManager):

    ctx = dialog_manager.current_context()
    channel_id = int(ctx.dialog_data['selected_channel_id'])

    session: AsyncSession = dialog_manager.middleware_data.get('session')
    stmt = (delete(SubscribeChannel).where(SubscribeChannel.id == channel_id))

    await session.execute(stmt)
    await session.commit()

    ctx.dialog_data.update(selected_channel_id='')
    await dialog_manager.switch_to(SubscribesSG.start)


async def switch_to_get_film_by_code(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.done()
    await dialog_manager.start(state=GetFilmByCodeSG.start)

