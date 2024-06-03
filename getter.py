from aiogram.enums import ContentType
from aiogram.types import User, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Film, BotUser, SubscribeChannel
from states import SubscribesSG, GetFilmByCodeSG


async def get_film(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    return {'film_name': dialog_manager.dialog_data['film_name'],
            'film_descr': dialog_manager.dialog_data['film_descr'] or '',
            'film_photo': MediaAttachment(ContentType.PHOTO,
                                          file_id=MediaId(dialog_manager.dialog_data['film_photo']))}


async def save_film(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    data = {'film_name': dialog_manager.dialog_data['film_name'],
            'film_descr': dialog_manager.dialog_data['film_descr'] or '',
            'film_photo': dialog_manager.dialog_data['film_photo']}

    obj = Film(
        name=data['film_name'],
        description=data['film_descr'],
        image=data['film_photo']
    )

    session.add(obj)
    await session.commit()

    return {'film_name': obj.name,
            'film_id': obj.id,
            'film_descr': obj.description or '',
            'film_photo': MediaAttachment(ContentType.PHOTO,
                                          file_id=MediaId(obj.image))}


async def get_user(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    tg_id = event_from_user.id

    session: AsyncSession = dialog_manager.middleware_data.get('session')
    user = await session.get(BotUser, tg_id)

    if not user:
        obj = BotUser(
            tg_id=tg_id,
            fio=f'{event_from_user.first_name} {event_from_user.last_name}',
            username=event_from_user.username,
            is_admin=False,
        )

        session.add(obj)
        await session.commit()

        if obj:
            return {'new_user': True, 'username': event_from_user.username}

    if user.is_admin:
        return {'admin': True, 'username': event_from_user.username}
    return {'old_user': True, 'username': event_from_user.username}


async def get_films(dialog_manager: DialogManager, **kwargs):
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    result = await session.execute(
        select(Film)
    )
    films = result.scalars().all()

    films_data = [
        (item.name, int(item.id)) for item in films
    ]
    print(films_data)
    return {'films': films_data}


async def get_film_info(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    film_id = int(ctx.dialog_data['selected_film_id'])

    session: AsyncSession = dialog_manager.middleware_data.get('session')
    film = await session.get(Film, film_id)

    return {'film_name': film.name,
            'film_id': film.id,
            'film_descr': film.description or '',
            'film_photo': MediaAttachment(ContentType.PHOTO,
                                          file_id=MediaId(film.image))}


async def get_channels(dialog_manager: DialogManager, **kwargs):
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    result = await session.execute(
        select(SubscribeChannel)
    )
    channels = result.scalars().all()

    channels_data = [
        (item.name, int(item.id)) for item in channels
    ]
    return {'channels': channels_data}


async def get_channel(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    channel_link = ctx.dialog_data['channel_link']

    session: AsyncSession = dialog_manager.middleware_data.get('session')

    result = await session.execute(
        select(SubscribeChannel).where(SubscribeChannel.link == channel_link)
    )
    channel = result.scalars().first()

    if channel:
        # await callback.message.answer('Этот канал уже в обязательных подписках')
        ctx.dialog_data.update(channel_link='')
        ctx.dialog_data.update(channel_title='')
        await dialog_manager.switch_to(SubscribesSG.start)
        return {'now_using': True}

    bot = dialog_manager.middleware_data['bot']
    try:
        # user_channel_status = await bot.get_chat_member(chat_id=channel_link, user_id=event_from_user.id)
        channel = await bot.get_chat(chat_id=channel_link)
        ctx.dialog_data.update(channel_name=channel.title)

        return {'channel_name': channel.title, 'channel_link': channel_link, 'channel_response': True}
    except:
        return {'not_admin_or_not_channel': True}


async def save_channel(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    session: AsyncSession = dialog_manager.middleware_data.get('session')
    data = {'channel_name': dialog_manager.dialog_data['channel_name'],
            'channel_link': dialog_manager.dialog_data['channel_link'],
            }

    obj = SubscribeChannel(
        name=data['channel_name'],
        link=data['channel_link'],
    )

    session.add(obj)
    await session.commit()

    return {'channel_name': obj.name,
            'channel_link': obj.link,
            }


async def get_channel_info(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    channel_id = int(ctx.dialog_data['selected_channel_id'])

    session: AsyncSession = dialog_manager.middleware_data.get('session')
    channel = await session.get(SubscribeChannel, channel_id)

    return {'channel_name': channel.name,
            'channel_link': channel.link}


async def get_film_by_code(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    bot = dialog_manager.middleware_data['bot']

    session: AsyncSession = dialog_manager.middleware_data.get('session')
    result = await session.execute(
        select(SubscribeChannel)
    )
    channels = result.scalars().all()

    channels_data = []

    for item in channels:
        user_channel_status = await bot.get_chat_member(chat_id=item.link, user_id=event_from_user.id)
        status = user_channel_status.status.__dict__
        if status['_value_'] not in ['creator', 'member']:
            channels_data.append({"id": int(item.id), "name": item.name, "url": f'https://t.me/{item.link[1:]}'})

    if len(channels_data) > 0:
        return {'not_subscribe': True, 'channels': channels_data}

    ctx = dialog_manager.current_context()
    film_id = int(ctx.dialog_data['film_code'])

    session: AsyncSession = dialog_manager.middleware_data.get('session')
    film = await session.get(Film, film_id)

    if not film:
        await dialog_manager.switch_to(GetFilmByCodeSG.start)
        return {'code_not_found': True}

    return {'subscribe': True,
            'film_name': film.name,
            'film_descr': film.description or '',
            'film_photo': MediaAttachment(ContentType.PHOTO,
                                          file_id=MediaId(film.image))}
