from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Button, SwitchTo, Back, Row
from aiogram_dialog.widgets.text import Format, Const

from database.utils import switch_to_main_menu, channel_selection, del_channel
from getter import get_channels, get_channel, save_channel, get_channel_info
from handlers.check import link_check
from handlers.correct import correct_link_channel
from handlers.error import error_film_handler, no_text, close_dialog
from states import SubscribesSG

subscribe_dialog = Dialog(
    Window(
        Const('Настройка каналов, на которые нужно подписаться'),
        ScrollingGroup(
            Select(
                Format('{item[0]}'),
                id='channel',
                item_id_getter=lambda x: x[1],
                items='channels',
                on_click=channel_selection,
            ),
            width=1,
            id='channels_scrolling_group',
            height=6,
        ),
        SwitchTo(Const('➕Добавить канал'), id='add_channel', state=SubscribesSG.add_channel),
        Button(Const('📃В главное меню'), id='to_main_menu', on_click=switch_to_main_menu),
        state=SubscribesSG.start,
        getter=get_channels
    ),
    Window(
        Const(text='Введите ссылку на канал в формате @something'),
        TextInput(
            id='link_input',
            type_factory=link_check,
            on_success=correct_link_channel,
            on_error=error_film_handler,
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        Button(Const('Отмена❌'), id='button_cancel', on_click=close_dialog),
        state=SubscribesSG.add_channel,
    ),
    Window(
        Format('Этот канал уже в обязательных подписках', when='now_using'),
        Row(
            Back(Const('◀️назад'), id='back3'),
            Button(Const('Отмена❌'), id='button_cancel', on_click=close_dialog),
            when='now_using'
        ),
        Format('Вы хотите добавить канал <b>{channel_name}</b>, находящийся по ссылке {channel_link} в обязательные '
               'подписки, '
               'все верно?', when='channel_response'),
        Row(
            Back(Const('◀️назад'), id='back3'),
            Button(Const('❌Отмена'), id='button_cancel', on_click=close_dialog),
            SwitchTo(Const('✅Сохранить'), id='button_save', state=SubscribesSG.final_submit_add_channel),
            when='channel_response'
        ),
        Format('Бот не является админом этого канала. Без этого он не сможет никак проверять подписки участников.',
               when='not_admin_or_not_channel'),
        Row(
            Back(Const('◀️назад'), id='back3'),
            Button(Const('Отмена❌'), id='button_cancel', on_click=close_dialog),
            when='not_admin_or_not_channel'
        ),

        getter=get_channel,
        state=SubscribesSG.submit_add_channel,
    ),
    Window(
        Format(text='<b>Канал {channel_name} успешно добавлен в обязательные подписки</b>\n'
                    'Ссылка: {channel_link}'),
        Button(Const('📃В главное меню'), id='to_main_menu', on_click=switch_to_main_menu),
        getter=save_channel,
        state=SubscribesSG.final_submit_add_channel
    ),

    Window(
        Format(text='<b>{channel_name}</b>\n'
                    'Ссылка: {channel_link}'),
        Row(
            SwitchTo(Const('◀️назад'), id='back_to_all_channels', state=SubscribesSG.start),
            Button(Const(text='❌Удалить канал'), id='del_channel', on_click=del_channel)
        ),
        getter=get_channel_info,
        state=SubscribesSG.change_one_channel
    )
)
