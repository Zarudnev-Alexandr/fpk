from aiogram.fsm.state import StatesGroup, State


class StartSG(StatesGroup):
    start_check_auth = State()


class EnterFilmSG(StatesGroup):
    enter_name = State()
    enter_description = State()
    enter_photo = State()
    enter_finish = State()
    enter_after_finish = State()


class AllFilmsSG(StatesGroup):
    all_films_start = State()
    film_info = State()


class SubscribesSG(StatesGroup):
    start = State()
    add_channel = State()
    submit_add_channel = State()
    final_submit_add_channel = State()
    change_one_channel = State()


class GetFilmByCodeSG(StatesGroup):
    start = State()
    film_info = State()


