from aiogram.dispatcher.filters.state import State, StatesGroup


class CheckTrackCodeState(StatesGroup):
    track_code = State()


class GetExpressIdState(StatesGroup):
    name = State()
    phone_number = State()
    passport_seria = State()
    passport_info = State()
    birthdate = State()
    address = State()
    filial = State()
    branch = State()
    passport_front = State()
    passport_back = State()
    check_data = State()


class SendAdState(StatesGroup):
    post = State()
    check_data = State()


class ChineseWarehouseReceive(StatesGroup):
    time = State()
    file = State()
    check_data = State()


class ComplaintState(StatesGroup):
    complaint = State()
    user_name = State()
    phone_number = State()


class AchchotSendState(StatesGroup):
    file = State()


class AchchotSentRefUserState(StatesGroup):
    file = State()


class DeliveryProductState(StatesGroup):
    photo = State()
    name = State()
    phone_number = State()
    address = State()
    mail_type = State()


class CreateRefState(StatesGroup):
    user_id = State()
    name = State()
    link_code = State()
    express_code = State()
    price = State()
    check_data = State()


class CardDataGetState(StatesGroup):
    card_number = State()
    card_name = State()
    check_data = State()


class PaymentScreenshotState(StatesGroup):
    photo = State()
    check_data = State()


class OneAchchotSendState(StatesGroup):
    photo = State()
    id_code = State()
    weight = State()
    price = State()
    type = State()
    check_data = State()


class AutoAchchotSendState(StatesGroup):
    flight_name = State()
    photo = State()
    id_code = State()
    weight = State()
    type = State()
    check_data = State()


class AddExpenseState(StatesGroup):
    amount = State()
    type = State()
    check_data = State()

class AddCardState(StatesGroup):
    card_number = State()
    card_name = State()
    card_branch_code = State()


class SelectionState(StatesGroup):
    choosing_region = State()
    choosing_branch = State()


class TrackCodeExcelState(StatesGroup):
    file = State()
    reys = State()
    check_data = State()
