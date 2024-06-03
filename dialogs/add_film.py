from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Back, Next, Button, Row, Cancel, Group, Select, ScrollingGroup
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from database.utils import film_selection, del_film, switch_to_main_menu
from getter import get_film, save_film, get_films, get_film_info
from handlers.check import name_check, descr_check, photo_check
from handlers.correct import correct_film_name_handler, correct_film_description_handler, skip_input_descr
from handlers.error import error_film_handler, no_text, close_dialog
from states import EnterFilmSG, AllFilmsSG

enter_film_dialog = Dialog(
    Window(
        Const(text='Введите название фильма'),
        TextInput(
            id='name_input',
            type_factory=name_check,
            on_success=correct_film_name_handler,
            on_error=error_film_handler,
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        Button(Const('Отмена❌'), id='button_cancel', on_click=close_dialog),
        state=EnterFilmSG.enter_name,
    ),
    Window(
        Const(text='Введите описание фильма (не обязательно)'),
        TextInput(
            id='descr_input',
            type_factory=descr_check,
            on_success=correct_film_description_handler,
            on_error=error_film_handler
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        Row(
            Back(Const('◀ назад'), id='back1'),
            Button(Const('Пропустить ▶'), id='next1', on_click=skip_input_descr),
            Button(Const('Отмена❌'), id='button_cancel', on_click=close_dialog),
        ),
        state=EnterFilmSG.enter_description,
    ),
    Window(
        Const(text='Отправьте обложку фильма'),
        MessageInput(
            func=photo_check,
            content_types=ContentType.PHOTO,
        ),
        Row(
            Back(Const('◀️назад'), id='back2'),
            Button(Const('Отмена❌'), id='button_cancel', on_click=close_dialog),
        ),

        state=EnterFilmSG.enter_photo,
    ),
    Window(
        Format(text='<b>{film_name}</b>\n\n{film_descr}'),
        DynamicMedia("film_photo"),
        Row(
            Back(Const('◀️назад'), id='back3'),
            Button(Const('Отмена❌'), id='button_cancel', on_click=close_dialog),
            Next(Const('Сохранить✅'), id='button_save')
        ),
        getter=get_film,
        state=EnterFilmSG.enter_finish,
    ),
    Window(
        Format(text='<b>{film_name}</b>\n'
                    'Код: {film_id}\n\n'
                    '{film_descr}'),
        DynamicMedia("film_photo"),
        Button(Const('📃В главное меню'), id='to_main_menu', on_click=switch_to_main_menu),
        getter=save_film,
        state=EnterFilmSG.enter_after_finish
    )
)

watch_all_films_dialog = Dialog(
    Window(
        Const(text='Выбери фильм:'),
        ScrollingGroup(
            Select(
                Format('({item[1]}) | {item[0]}'),
                id='film',
                item_id_getter=lambda x: x[1],
                items='films',
                on_click=film_selection,
            ),
            width=1,
            id='films_scrolling_group',
            height=6,
        ),
        Button(Const('📃В главное меню'), id='to_main_menu', on_click=switch_to_main_menu),
        state=AllFilmsSG.all_films_start,
        getter=get_films
    ),
    Window(
        Format(text='<b>{film_name}</b>\n'
                    'Код: {film_id}\n\n'
                    '{film_descr}'),
        DynamicMedia("film_photo"),
        Row(
            Back(Const('◀️назад'), id='back2'),
            Button(Const(text='❌Удалить фильм'), id='del_film', on_click=del_film)
        ),
        getter=get_film_info,
        state=AllFilmsSG.film_info
    )
)
