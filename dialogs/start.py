from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Format, Const

from database.utils import switch_to_enter_film, switch_to_get_films, switch_to_subscribes, switch_to_get_film_by_code
from getter import get_user
from states import StartSG

start_dialog = Dialog(
    Window(
        Format('Привет, {username}!'),
        Const('У тебя есть админские права, кайфуй, бро😎', when='admin'),
        Const('Никогда не пользовался этим ботом? Жми на кнопку и ищи понравившейся фильм🔥', when='new_user'),
        Const('С возвращением! Жми на кнопку и ищи понравившейся фильм🔥', when='old_user'),
        Row(
            Button(Const('Добавить фильм'), id='add_film_btn', when='admin', on_click=switch_to_enter_film),
            Button(Const('Посмотреть фильмы'), id='get_films_btn', when='admin', on_click=switch_to_get_films),
        ),
        Row(
            Button(Const('Подписки'), id='subscribes', when='admin', on_click=switch_to_subscribes),
            Button(Const('🔢Ввести код фильма'), id='enter_film_code', on_click=switch_to_get_film_by_code)
        ),

        getter=get_user,
        state=StartSG.start_check_auth
    )
)



