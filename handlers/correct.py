from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from states import SubscribesSG, GetFilmByCodeSG


async def correct_film_name_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    dialog_manager.dialog_data['film_name'] = text
    await dialog_manager.next()


async def correct_film_description_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    dialog_manager.dialog_data['film_descr'] = text
    await dialog_manager.next()


async def skip_input_descr(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data['film_descr'] = ''
    await dialog_manager.next()


async def skip_input_photo(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data['film_photo'] = ''
    await dialog_manager.next()


async def correct_link_channel(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:

    ctx = dialog_manager.current_context()
    ctx.dialog_data.update(channel_link=text)

    await dialog_manager.switch_to(SubscribesSG.submit_add_channel)


async def correct_film_code_channel(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:

    ctx = dialog_manager.current_context()
    ctx.dialog_data.update(film_code=text)

    await dialog_manager.switch_to(GetFilmByCodeSG.film_info)
