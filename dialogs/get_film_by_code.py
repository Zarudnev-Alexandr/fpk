from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import ScrollingGroup, Url, SwitchTo, ListGroup, Button, Row, Back
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from database.utils import switch_to_main_menu
from getter import get_film_by_code
from handlers.check import film_code_check
from handlers.correct import correct_film_code_channel
from handlers.error import error_film_code_handler, no_text, close_dialog
from states import GetFilmByCodeSG

get_film_by_code_dialog = Dialog(
    Window(
        Const(text='Введи код фильма:'),
        TextInput(
            id='film_code_input',
            type_factory=film_code_check,
            on_success=correct_film_code_channel,
            on_error=error_film_code_handler,
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        Button(Const('Отмена❌'), id='button_cancel', on_click=close_dialog),
        state=GetFilmByCodeSG.start,
    ),
    Window(
        Const(text='Вы не подписаны на эти каналы.\nПодпишитесь и введите код фильма', when='not_subscribe'),
        ListGroup(
            Url(
                Format('{item[name]}'),
                Format('{item[url]}'),
                id='url'
            ),
            id='channels_list_group',
            item_id_getter=lambda item: item["id"],
            items='channels',
            when='not_subscribe'
        ),
        SwitchTo(Const('Я подписался👍'), id='i_subscribe', state=GetFilmByCodeSG.start, when='not_subscribe'),
        Button(Const('📃В главное меню'), id='to_main_menu', on_click=switch_to_main_menu, when='not_subscribe'),

        Const('🎦Результат по запросу:\n', when='subscribe'),
        Format(text='<b>{film_name}</b>\n\n'
                    '{film_descr}',
               when='subscribe'),
        DynamicMedia("film_photo", when='subscribe'),
        Row(
            SwitchTo(Const('🎞Найти еще фильм'), id='find_more_films', state=GetFilmByCodeSG.start),
            Button(Const('📃В главное меню'), id='to_main_menu', on_click=switch_to_main_menu),
            when='subscribe'
        ),

        Const('По этому коду фильмов не найдено', when='code_not_found'),
        Back(Const('🔄Попробовать с другим кодом'), id='back', when='code_not_found'),
        state=GetFilmByCodeSG.film_info,
        getter=get_film_by_code
    )
)
