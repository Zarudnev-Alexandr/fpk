from typing import Any

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import SubscribeChannel


def name_check(text: Any) -> str:
    if 1 <= len(text) <= 150:
        return text
    raise ValueError


def descr_check(text: Any) -> Any | None:
    if 1 <= len(text) <= 500:
        if text == 'пропустить':
            return None
        else:
            return text
    raise ValueError


async def photo_check(message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager) -> None:
    if not message.photo[-1].file_id:
        await message.answer(text='Отпрвьте фото (не файл). Желательный формат - jpg')

    dialog_manager.dialog_data['film_photo'] = message.photo[-1].file_id
    await dialog_manager.next()


def link_check(text: Any):

    if 1 <= len(text) <= 150 and text[0] == '@':
        return text
    raise ValueError


def film_code_check(text: Any):

    if 1 <= len(text) <= 4 and int(text) < 99999:
        return text
    raise ValueError
