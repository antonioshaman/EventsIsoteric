from aiogram.types import KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from starter.other import cur

class MyCallback(CallbackData, prefix="my"):
    name: str
    value: str

def crl():
    pu = ReplyKeyboardBuilder()
    addmp = KeyboardButton(text='Добавить мероприятие в афишу')
    editmp = KeyboardButton(text='Редактировать мероприятие')
    delmp = KeyboardButton(text='Удалить мероприятие')
    supp = KeyboardButton(text='Помощь и обратная связь')
    pu.row(addmp)
    pu.row(editmp, delmp)
    pu.row(supp)
    return pu.as_markup(resize_keyboard=True)

def addbuttons(nm, dt, ad, wh, desc, cnt, pr, ph, cn):
    stt = InlineKeyboardBuilder()
    name = InlineKeyboardButton(text='Название *', callback_data='name')
    name_ad = InlineKeyboardButton(text='✅ Название *', callback_data='name_ad')
    date = InlineKeyboardButton(text='Дата/время *', callback_data='date')
    date_ad = InlineKeyboardButton(text='✅ Дата/время *', callback_data='date_ad')
    adres = InlineKeyboardButton(text='Адрес *', callback_data='adres')
    adres_ad = InlineKeyboardButton(text='✅ Адрес *', callback_data='adres_ad')
    who = InlineKeyboardButton(text='Кто проводит', callback_data='who')
    who_ad = InlineKeyboardButton(text='✅ Кто проводит', callback_data='who_ad')
    descrip = InlineKeyboardButton(text='Описание *', callback_data='descrip')
    descrip_ad = InlineKeyboardButton(text='✅ Описание *', callback_data='descrip_ad')
    count = InlineKeyboardButton(text='Цена', callback_data='count')
    count_ad = InlineKeyboardButton(text='✅ Цена', callback_data='count_ad')
    prim = InlineKeyboardButton(text='Примечание', callback_data='prim')
    prim_ad = InlineKeyboardButton(text='✅ Примечание', callback_data='prim_ad')
    photo = InlineKeyboardButton(text='Фото', callback_data='photo')
    photo_ad = InlineKeyboardButton(text='✅ Фото', callback_data='photo_ad')
    contact = InlineKeyboardButton(text='Контакты *', callback_data='contact')
    contact_ad = InlineKeyboardButton(text='✅ Контакты *', callback_data='contact_ad')
    show = InlineKeyboardButton(text='Посмотреть', callback_data='show')
    cancel = InlineKeyboardButton(text='Отменить', callback_data='cancel')
    send = InlineKeyboardButton(text='Отправить', callback_data='send')
    if nm == "-":
        name = name
    else:
        name = name_ad
    if dt == "-":
        date = date
    else:
        date = date_ad
    if ad == "-":
        adres = adres
    else:
        adres = adres_ad
    if wh == "-":
        who = who
    else:
        who = who_ad
    if desc == "-":
        descrip = descrip
    else:
        descrip = descrip_ad
    if cnt == "-":
        count = count
    else:
        count = count_ad
    if pr == "-":
        prim = prim
    else:
        prim = prim_ad
    if ph == "-":
        photo = photo
    else:
        photo = photo_ad
    if cn == "-":
        contact = contact
    else:
        contact = contact_ad
    stt.row(name, date, adres)
    stt.row(who, descrip, count)
    stt.row(prim, photo, contact)
    if nm == "-" or dt == "-" or ad == "-" or desc == "-" or cn == "-":
        stt.row(cancel)
    else:
        stt.row(show, cancel, send)
    return stt.as_markup()

def editbuttons(nm, dt, ad, wh, desc, cnt, pr, cn):
    stt = InlineKeyboardBuilder()
    name_ad = InlineKeyboardButton(text='✅ Название *', callback_data='name_edit')
    date_ad = InlineKeyboardButton(text='✅ Дата/время *', callback_data='date_edit')
    adres_ad = InlineKeyboardButton(text='✅ Адрес *', callback_data='adres_edit')
    who = InlineKeyboardButton(text='Кто проводит', callback_data='who_edit')
    who_ad = InlineKeyboardButton(text='✅ Кто проводит', callback_data='who_edit_ad')
    descrip_ad = InlineKeyboardButton(text='✅ Описание *', callback_data='descrip_edit')
    count = InlineKeyboardButton(text='Цена', callback_data='count_edit')
    count_ad = InlineKeyboardButton(text='✅ Цена', callback_data='count_edit_ad')
    prim = InlineKeyboardButton(text='Примечание', callback_data='prim_edit')
    prim_ad = InlineKeyboardButton(text='✅ Примечание', callback_data='prim_edit_ad')
    contact_ad = InlineKeyboardButton(text='✅ Контакты *', callback_data='contact_edit')
    show = InlineKeyboardButton(text='Посмотреть', callback_data='show_edit')
    cancel = InlineKeyboardButton(text='Отменить', callback_data='cancel_edit')
    send = InlineKeyboardButton(text='Отправить', callback_data='send_edit')
    if wh == "-":
        who = who
    else:
        who = who_ad
    if cnt == "-":
        count = count
    else:
        count = count_ad
    if pr == "-":
        prim = prim
    else:
        prim = prim_ad
    stt.row(name_ad, date_ad, adres_ad)
    stt.row(who, descrip_ad, count)
    stt.row(prim, contact_ad)
    if nm == "-" or dt == "-" or ad == "-" or desc == "-" or cn == "-":
        stt.row(cancel)
    else:
        stt.row(show, cancel, send)
    return stt.as_markup()

def back():
    control = InlineKeyboardBuilder()
    back = InlineKeyboardButton(text='⏪ Назад', callback_data="back_ank")
    control.row(back)
    return control.as_markup()

def back_edit():
    control = InlineKeyboardBuilder()
    back = InlineKeyboardButton(text='⏪ Назад', callback_data="back_ank_edit")
    control.row(back)
    return control.as_markup()

def back_show():
    control = InlineKeyboardBuilder()
    back = InlineKeyboardButton(text='⏪ Назад', callback_data="back_show")
    control.row(back)
    return control.as_markup()

def back_show_edit():
    control = InlineKeyboardBuilder()
    back = InlineKeyboardButton(text='⏪ Назад', callback_data="back_show_edit")
    control.row(back)
    return control.as_markup()

def ps():
    control = InlineKeyboardBuilder()
    add = InlineKeyboardButton(text='Добавить', callback_data="add")
    no = InlineKeyboardButton(text='Не добалять', callback_data="noadd")
    control.row(add)
    control.row(no)
    return control.as_markup()

def ps_edit():
    control = InlineKeyboardBuilder()
    add = InlineKeyboardButton(text='Добавить', callback_data="add_edit")
    no = InlineKeyboardButton(text='Не добалять', callback_data="noadd_edit")
    control.row(add)
    control.row(no)
    return control.as_markup()

def pass_time():
    control = InlineKeyboardBuilder()
    back = InlineKeyboardButton(text='Пропустить', callback_data="pass_time")
    control.row(back)
    return control.as_markup()

def pass_time_edt():
    control = InlineKeyboardBuilder()
    back = InlineKeyboardButton(text='Пропустить', callback_data="pass_time_edt")
    control.row(back)
    return control.as_markup()