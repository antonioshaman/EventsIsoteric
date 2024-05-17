import random
from starter.load_jsons import adminid
from starter.loader import dp, bot
from buttons import markups as nav
from starter.other import Other, base, cur, is_number
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram import F
from aiogram.filters import StateFilter
import datetime
import imgbbpy
import requests

@dp.message(F.text.lower() == 'добавить мероприятие в афишу')
async def addmp(message: types.Message):
    if int(message.from_user.id) != int(adminid()):
        mp = cur.execute(f'SELECT * FROM mps WHERE userid == ?', [message.from_user.id]).fetchone()
        if mp:
            mp = cur.execute(f'SELECT * FROM mps WHERE userid == ?', [message.from_user.id]).fetchall()[-1]
            data_check = datetime.datetime.now()
            elapsed_time = data_check - datetime.datetime.strptime(mp[12], "%Y-%m-%d %H:%M:%S.%f")
            if elapsed_time.total_seconds() >= 72 * 60 * 60:
                ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [message.from_user.id]).fetchone()
                if ank:
                    cur.execute(f'DELETE FROM pre_mps WHERE userid == ?', [message.from_user.id])
                    base.commit()
                cur.execute('INSERT INTO pre_mps VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [message.from_user.id, "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"])
                base.commit()
                await bot.send_message(message.from_user.id, 'Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                                             'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons("-", "-", "-", "-", "-", "-", "-", "-", "-"))
                mess = await bot.send_message(message.from_user.id, "1", reply_markup=nav.crl())
                await bot.delete_message(message.from_user.id, mess.message_id)  # удаление клавиатуры
            else:
                await bot.send_message(message.from_user.id, "Вы можете отправить одно мероприятие раз в 3 дня")
        else:
            ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [message.from_user.id]).fetchone()
            if ank:
                cur.execute(f'DELETE FROM pre_mps WHERE userid == ?', [message.from_user.id])
                base.commit()
            cur.execute('INSERT INTO pre_mps VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [message.from_user.id, "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"])
            base.commit()
            await bot.send_message(message.from_user.id, 'Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                                         'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons("-", "-", "-", "-", "-", "-", "-", "-", "-"))
            mess = await bot.send_message(message.from_user.id, "1", reply_markup=nav.crl())
            await bot.delete_message(message.from_user.id, mess.message_id)  # удаление клавиатуры
    else:
        ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [message.from_user.id]).fetchone()
        if ank:
            cur.execute(f'DELETE FROM pre_mps WHERE userid == ?', [message.from_user.id])
            base.commit()
        cur.execute('INSERT INTO pre_mps VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [message.from_user.id, "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"])
        base.commit()
        await bot.send_message(message.from_user.id, 'Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                                     'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons("-", "-", "-", "-", "-", "-", "-", "-", "-"))
        mess = await bot.send_message(message.from_user.id, "1", reply_markup=nav.crl())
        await bot.delete_message(message.from_user.id, mess.message_id)  # удаление клавиатуры

@dp.callback_query(F.data == 'name')
async def name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Название * (обязательно к заполнению).\n"
                                     'Введите название вашего мероприятия, оно должно быть кратким. Нажмите "⏪ Назад", чтобы вернуться к другим пунктам описания.', reply_markup=nav.back())
    await state.set_state(Other.name)

@dp.message(Other.name, F.text)
async def name(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.name)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    await state.clear()
    cur.execute(f'UPDATE pre_mps SET name == ? WHERE userid == ?', [message.text, message.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [message.from_user.id]).fetchone()
    await bot.send_message(message.from_user.id, 'Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                                 'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))

@dp.callback_query(F.data == 'name_ad')
async def name_ad(callback: types.CallbackQuery, state: FSMContext):
    ank = cur.execute(f'SELECT name FROM pre_mps WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Название * (обязательно к заполнению).\n"
                                     f'Введите название вашего мероприятия, оно должно быть кратким. Нажмите "⏪ Назад", чтобы вернуться к другим пунктам описания.\n\nТекущее значение поля: {ank[0]}', reply_markup=nav.back())
    await state.set_state(Other.name)

@dp.callback_query(F.data == 'date')
async def date(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Дата/время * (обязательно к заполнению).\n"
                                     f'Введите дату начала вашего мероприятия и нажмите отправить. Нажмите "⏪ Назад", чтобы вернуться к другим пунктам описания.\n\n'
                                     f'Формат указания времени: день.месяц.год чч:мм\n\n'
                                     f'Пример заполнения: 26.03.2024 15:30', reply_markup=nav.back())
    await state.set_state(Other.date)

@dp.message(Other.date, F.text)
async def date(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.date)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    try:
        datetime.datetime.strptime(message.text, '%d.%m.%Y %H:%M')
    except:
        await state.set_state(Other.date)
        return await bot.send_message(message.from_user.id, 'Вы указали не верный формат времени, заполните заново или нажмите кнопку "⏪ Назад"')
    await state.update_data(date_start = message.text)
    await bot.send_message(message.from_user.id, "Укажите дату окончания мероприятия, если хотите пропустить то нажмите на кнопку ниже", reply_markup=nav.pass_time())
    await state.set_state(Other.end_date)

@dp.callback_query(StateFilter("*"), F.data == 'pass_time')
async def pass_time(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cur.execute(f'UPDATE pre_mps SET date_start == ? WHERE userid == ?', [data["date_start"], callback.from_user.id])
    base.commit()
    await state.clear()
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text('Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                                 'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))

@dp.message(Other.end_date, F.text)
async def end_date(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.end_date)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    try:
        datetime.datetime.strptime(message.text, '%d.%m.%Y %H:%M')
    except:
        await state.set_state(Other.end_date)
        return await bot.send_message(message.from_user.id, 'Вы указали не верный формат времени, заполните заново или нажмите кнопку "⏪ Назад"')
    data = await state.get_data()
    cur.execute(f'UPDATE pre_mps SET date_start == ? WHERE userid == ?', [data["date_start"], message.from_user.id])
    cur.execute(f'UPDATE pre_mps SET date_end == ? WHERE userid == ?', [message.text, message.from_user.id])
    base.commit()
    await state.clear()
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [message.from_user.id]).fetchone()
    await bot.send_message(message.from_user.id, 'Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                                 'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))

@dp.callback_query(F.data == 'date_ad')
async def date_ad(callback: types.CallbackQuery, state: FSMContext):
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [callback.from_user.id]).fetchone()
    if ank[3] == "-":
        dt = "Не указано"
    else:
        dt = ank[3]
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Дата/время * (обязательно к заполнению).\n"
                                     f'Введите дату начала вашего мероприятия и нажмите отправить. Нажмите "⏪ Назад", чтобы вернуться к другим пунктам описания.\n\n'
                                     f'Формат указания времени: день.месяц.год чч:мм\n\n'
                                     f'Пример заполнения: 26.03.2024 15:30\n\n'
                                     f'Текущее значение поля: {ank[2]}(начало) | {dt}(конец)', reply_markup=nav.back())
    await state.set_state(Other.date)

@dp.callback_query(F.data == 'adres')
async def adres(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Адрес * (обязательно к заполнению).\n"
                                     'Напишите адрес проведения мероприятия и нажмите кнопку отправить, или нажмите "⏪ Назад", чтобы вернуться к другим пунктам описания.\n\n'
                                     'Формат указания адреса: (населенный пункт/курорт), (улица), (номер дома), (квартира), (примечание)\n\n'
                                     'Пример заполнения: Красная Поляна, ул. Пчеловодов, 23 (Парк шале)', reply_markup=nav.back())
    await state.set_state(Other.adres)

@dp.message(Other.adres, F.text)
async def adres(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.adres)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    await state.clear()
    cur.execute(f'UPDATE pre_mps SET adress == ? WHERE userid == ?', [message.text, message.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [message.from_user.id]).fetchone()
    await bot.send_message(message.from_user.id, 'Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                                 'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))

@dp.callback_query(F.data == 'adres_ad')
async def adres(callback: types.CallbackQuery, state: FSMContext):
    ank = cur.execute(f'SELECT adress FROM pre_mps WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Адрес * (обязательно к заполнению).\n"
                                     'Напишите адрес проведения мероприятия и нажмите кнопку отправить, или нажмите "⏪ Назад", чтобы вернуться к другим пунктам описания.\n\n'
                                     'Формат указания адреса: (населенный пункт/курорт), (улица), (номер дома), (квартира), (примечание)\n\n'
                                     f'Пример заполнения: Красная Поляна, ул. Пчеловодов, 23 (Парк шале)\n\n'
                                     f'Текущее значение поля: {ank[0]}', reply_markup=nav.back())
    await state.set_state(Other.adres)

@dp.callback_query(F.data == 'who')
async def who(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Кто проводит.\n"
                                     'Напишите Фамилию и Имя человека который проводит мероприятие - лектор, инструктор или др. Можно указать несколько. При желании, после имени можно коротко указать профиль работы.\n\n'
                                     'Этот пункт может отличаться от пункта “Контакты” в котором мы указываем контакты организатора мероприятия и человека у которого можно уточнить все подробности. Однако “Кто проводит” и  контакты организатора могут совпадать. Подробнее см. в пункте “Контакты”.\n\n'
                                     '❗️Ссылки в этом пункте запрещены, их можно будет указать в описании мероприятия.\n\n'
                                     'Пример заполнения:\n'
                                     'Иванова Галина, художник и декоратор с опытом работа 15 лет.\n'
                                     'Сурков Михаил, дизайнер интерьеров\n\n'
                                     'После заполнения данных нажмите на кнопку отправить, или нажмите "⏪ Назад", чтобы вернуться к другим пунктам описания', reply_markup=nav.back())
    await state.set_state(Other.who)

@dp.message(Other.who, F.text)
async def who(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.who)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    await state.clear()
    cur.execute(f'UPDATE pre_mps SET who == ? WHERE userid == ?', [message.text, message.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [message.from_user.id]).fetchone()
    await bot.send_message(message.from_user.id, 'Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                                 'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))

@dp.callback_query(F.data == 'who_ad')
async def who(callback: types.CallbackQuery, state: FSMContext):
    ank = cur.execute(f'SELECT who FROM pre_mps WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Кто проводит.\n"
                                     'Напишите Фамилию и Имя человека который проводит мероприятие - лектор, инструктор или др. Можно указать несколько. При желании, после имени можно коротко указать профиль работы.\n\n'
                                     'Этот пункт может отличаться от пункта “Контакты” в котором мы указываем контакты организатора мероприятия и человека у которого можно уточнить все подробности. Однако “Кто проводит” и  контакты организатора могут совпадать. Подробнее см. в пункте “Контакты”.\n\n'
                                     '❗️Ссылки в этом пункте запрещены, их можно будет указать в описании мероприятия.\n\n'
                                     'Пример заполнения:\n'
                                     'Иванова Галина, художник и декоратор с опытом работа 15 лет.\n'
                                     'Сурков Михаил, дизайнер интерьеров\n\n'
                                     'После заполнения данных нажмите на кнопку отправить, или нажмите "⏪ Назад", чтобы вернуться к другим пунктам описания\n\n'
                                     f'Текущее значение поля: {ank[0]}', reply_markup=nav.back())
    await state.set_state(Other.who)

@dp.callback_query(F.data == 'descrip')
async def descrip(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Описание * (обязательно к заполнению).\n"
                                     'Опишите мероприятие и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам.\n\n'
                                     'Постарайтесь быть краткими, но содержательными. Напишите главное, остальное участники смогут уточнить связавшись с вами лично.\n\n'
                                     '⚠️Внимание! Ограничение на объёму текста 1200 символов (включая пробелы).', reply_markup=nav.back())
    await state.set_state(Other.descrip)

@dp.message(Other.descrip, F.text)
async def descrip(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.descrip)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    await state.clear()
    if len(message.text) <= 1200:
        cur.execute(f'UPDATE pre_mps SET descrip == ? WHERE userid == ?', [message.text, message.from_user.id])
        base.commit()
        ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [message.from_user.id]).fetchone()
        await bot.send_message(message.from_user.id, 'Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                                     'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))
    else:
        await bot.send_message(message.from_user.id, "Ваше описание привышает возможную длину 1200 символов(включая пробелы)", reply_markup=nav.back())

@dp.callback_query(F.data == 'descrip_ad')
async def descrip_ad(callback: types.CallbackQuery, state: FSMContext):
    ank = cur.execute(f'SELECT descrip FROM pre_mps WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Описание * (обязательно к заполнению).\n"
                                     'Опишите мероприятие и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам.\n\n'
                                     'Постарайтесь быть краткими, но содержательными. Напишите главное, остальное участники смогут уточнить связавшись с вами лично.\n\n'
                                     '⚠️Внимание! Ограничение на объёму текста 1200 символов (включая пробелы).\n\n'
                                     f'Текущее значение поля: {ank[0]}', reply_markup=nav.back())
    await state.set_state(Other.descrip)

@dp.callback_query(F.data == 'count')
async def count(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Цена.\n"
                                     'Напишите стоимость участия и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания.', reply_markup=nav.back())
    await state.set_state(Other.count)

@dp.message(Other.count, F.text)
async def count(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.count)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    await state.clear()
    cur.execute(f'UPDATE pre_mps SET count == ? WHERE userid == ?', [message.text, message.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [message.from_user.id]).fetchone()
    await bot.send_message(message.from_user.id, 'Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                                 'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))

@dp.callback_query(F.data == 'count_ad')
async def count_ad(callback: types.CallbackQuery, state: FSMContext):
    ank = cur.execute(f'SELECT count FROM pre_mps WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Цена.\n"
                                     'Напишите стоимость участия и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания.\n\n'
                                     f'Текущее значение поля: {ank[0]}', reply_markup=nav.back())
    await state.set_state(Other.count)

@dp.callback_query(F.data == 'prim')
async def prim(callback: types.CallbackQuery):
    await callback.message.edit_text("Содержание поля по умолчанию:\n"
                                     'Участие строго по записи. Всю дополнительную информацию вы можете получить у организатора!\n\n'
                                     'Если для вашего мероприятия это актуально, то нажмите кнопку “Добавить”.\n'
                                     'Нажмите кнопку “Не добавлять”, чтобы пропустить это поле.', reply_markup=nav.ps())

@dp.callback_query(F.data == 'add')
async def add(callback: types.CallbackQuery):
    cur.execute(f'UPDATE pre_mps SET prim == ? WHERE userid == ?', ["Участие строго по записи. Всю дополнительную информацию вы можете получить у организатора!", callback.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text('Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                                 'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))

@dp.callback_query(F.data == 'noadd')
async def add(callback: types.CallbackQuery):
    cur.execute(f'UPDATE pre_mps SET prim == ? WHERE userid == ?', ["-", callback.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text('Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                                 'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))

@dp.callback_query(F.data == 'prim_ad')
async def prim(callback: types.CallbackQuery):
    await callback.message.edit_text("Содержание поля по умолчанию:\n"
                                     'Участие строго по записи. Всю дополнительную информацию вы можете получить у организатора!\n\n'
                                     'Если для вашего мероприятия это актуально, то нажмите кнопку “Добавить”.\n'
                                     'Нажмите кнопку “Не добавлять”, чтобы пропустить это поле.', reply_markup=nav.ps())

@dp.callback_query(F.data == 'photo')
async def photo_mess(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('🔄 Вы сейчас редактируете поле Фото\n\n'
                                     'Нажмите на скрепку чтобы отправить фото или видео афиши мероприятия. Ограничение по количеству 1️⃣ фото или 1️⃣ видео. Ограничение по  размеру файла 5 мб.\n'
                                     '‼️Обязательно отметьте галочку "Сжать изображение", иначе фото не прикрепится.', reply_markup=nav.back())
    await state.set_state(Other.photo)

@dp.message(Other.photo, F.photo)
async def photo_mess(message: types.Message, state: FSMContext):
    await state.clear()
    await message.bot.download(message.photo[-1].file_id, f'media/{message.from_user.id}_photo.png')
    client = imgbbpy.AsyncClient('7e2b2dfe79bb308bba62728933231682')
    image = await client.upload(file=f'media/{message.from_user.id}_photo.png')
    cur.execute(f'UPDATE pre_mps SET photo == ? WHERE userid == ?', [image.url, message.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [message.from_user.id]).fetchone()
    await bot.send_message(message.from_user.id, 'Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                                 'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))

@dp.message(Other.photo, F.video)
async def video_mess(message: types.Message, state: FSMContext):
    await state.clear()
    await bot.send_message(message.from_user.id, "Ожидайте, загружаю видео...")
    await message.bot.download(message.video.file_id, f'media/{message.from_user.id}_video.mp4')
    with open(f'media/{message.from_user.id}_video.mp4', 'rb') as photo:
        path = requests.post(
            "https://te.legra.ph/upload", files={"file": (f'file', photo, None)}
        ).json()
        try:
            link = "https://te.legra.ph" + path[0]["src"]
        except:
            link = path["error"]
            await state.set_state(Other.photo)
            return await bot.send_message(message.from_user.id, f'{link}\n\nОтправьте другое видео или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    cur.execute(f'UPDATE pre_mps SET photo == ? WHERE userid == ?', [link, message.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [message.from_user.id]).fetchone()
    await bot.send_message(message.from_user.id, 'Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                                 'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))

@dp.message(Other.photo, F.document)
async def get_file(message: types.Message):
    await bot.send_message(message.from_user.id, "Вы не отправили сжатое изображение\n"
                                                 "Файл не получен\n"
                                                 'Попробуйте еще раз, не забудьте сжать изображение перед отправкой или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())

@dp.callback_query(F.data == 'photo_ad')
async def photo_mess(callback: types.CallbackQuery, state: FSMContext):
    ank = cur.execute(f'SELECT photo FROM pre_mps WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text('🔄 Вы сейчас редактируете поле Фото\n\n'
                                     'Нажмите на скрепку чтобы отправить фото или видео афиши мероприятия. Ограничение по количеству 1️⃣ фото или 1️⃣ видео. Ограничение по  размеру файла 5 мб.\n'
                                     '‼️Обязательно отметьте галочку "Сжать изображение", иначе фото не прикрепится.\n\n'
                                     f'Текущее значение поля: <a href="{ank[0]}">ㅤ</a>', reply_markup=nav.back())
    await state.set_state(Other.photo)

@dp.callback_query(F.data == 'contact')
async def contact(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('🔄 Вы сейчас редактируете поле Контакты * (обязательно к заполнению).\n\n'
                                     'Укажите свои контакты и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания.\n\n'
                                     'В этом пункте желательно указать свой ник в телеграм, чтобы участники смогли записаться или задать вам интересующие вопросы по мероприятию. По желанию можно указать свой номер телефона для связи.\n\n'
                                     'Формат размещения контактов: (ник в телеграм) (телефон) (имя)\n\n'
                                     'Пример заполнения: @shaman8888 +7(918)123-45-67 Антон', reply_markup=nav.back())
    await state.set_state(Other.contact)

@dp.message(Other.contact, F.text)
async def contact(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.contact)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    if "@" not in message.text:
        await state.set_state(Other.contact)
        return await bot.send_message(message.from_user.id, 'Вы не указали телеграмм для связи, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    await state.clear()
    cur.execute(f'UPDATE pre_mps SET contact == ? WHERE userid == ?', [message.text, message.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [message.from_user.id]).fetchone()
    await bot.send_message(message.from_user.id, 'Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                                 'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))

@dp.callback_query(F.data == 'contact_ad')
async def contact_ad(callback: types.CallbackQuery, state: FSMContext):
    ank = cur.execute(f'SELECT contact FROM pre_mps WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text('🔄 Вы сейчас редактируете поле Контакты * (обязательно к заполнению).\n\n'
                                     'Укажите свои контакты и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания.\n\n'
                                     'В этом пункте желательно указать свой ник в телеграм, чтобы участники смогли записаться или задать вам интересующие вопросы по мероприятию. По желанию можно указать свой номер телефона для связи.\n\n'
                                     'Формат размещения контактов: (ник в телеграм) (телефон) (имя)\n\n'
                                     'Пример заполнения: @shaman8888 +7(918)123-45-67 Антон\n\n'
                                     f'Текущее значение поля: {ank[0]}', reply_markup=nav.back())
    await state.set_state(Other.contact)

@dp.callback_query(F.data == 'show')
async def show(callback: types.CallbackQuery):
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [callback.from_user.id]).fetchone()
    if ank[9] == "-":
        if ank[3] == "-":
            dt = ank[2]
        else:
            dt = f"{ank[2]} - {ank[3]}"
        mess = f"✅ <b>{ank[1]}</b>\n⏰ {dt}\n📍 {ank[4]}\n"
        if ank[5] != "-":
            mess += f"👤 {ank[5]}\n\n{ank[6]}\n\n"
        else:
            mess += f"\n{ank[6]}\n\n"
        if ank[7] != "-":
            mess += f"💸 Цена: {ank[7]}\n\n"
        mess += f"☎️ Контакты: {ank[10]}\n\n"
        if ank[8] != "-":
            mess += f"P.S. {ank[8]}\n\n"
        if callback.from_user.username != None:
            mess += f"Опубликовал: @{callback.from_user.username}"
        await callback.message.edit_text(mess, parse_mode='HTML', reply_markup=nav.back_show())
    else:
        if ank[3] == "-":
            dt = ank[2]
        else:
            dt = f"{ank[2]} - {ank[3]}"
        mess = f"✅ <b>{ank[1]}</b>\n⏰ {dt}\n📍 {ank[4]}\n"
        if ank[5] != "-":
            mess += f"👤 {ank[5]}\n\n{ank[6]}\n\n"
        else:
            mess += f"\n{ank[6]}\n\n"
        if ank[7] != "-":
            mess += f"💸 Цена: {ank[7]}\n\n"
        mess += f"☎️ Контакты: {ank[10]}\n\n"
        if ank[8] != "-":
            mess += f"P.S. {ank[8]}\n"
        if callback.from_user.username != None:
            mess += f"Опубликовал: @{callback.from_user.username}\n"
            mess += f'<a href="{ank[9]}">ㅤ</a>'
        else:
            mess += f'\n<a href="{ank[9]}">ㅤ</a>'
        await callback.message.edit_text(mess, parse_mode='HTML', reply_markup=nav.back_show())

@dp.callback_query(StateFilter("*"), F.data == 'back_ank')
async def back_ank(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [callback.from_user.id]).fetchone()
    try:
        await callback.message.edit_text('Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                         'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))
    except:
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await bot.send_message(callback.from_user.id, 'Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                         'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))

@dp.callback_query(F.data == 'back_show')
async def back_show(callback: types.CallbackQuery):
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [callback.from_user.id]).fetchone()
    try:
        await callback.message.edit_text('Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                         'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))
    except:
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await bot.send_message(callback.from_user.id, 'Для добавления мероприятия необходимо заполнить поля, отмеченные звездочкой (*). Остальные пункты не обязательны к заполнению, но желательны.\n\n'
                                         'Если вы не хотели добавлять мероприятие нажмите на кнопку "Отменить"', reply_markup=nav.addbuttons(ank[1], ank[2], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10]))

@dp.callback_query(F.data == 'cancel')
async def cancel(callback: types.CallbackQuery):
    cur.execute(f'DELETE FROM pre_mps WHERE userid == ?', [callback.from_user.id])
    base.commit()
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, "Вы вышли в главное меню", reply_markup=nav.crl())

@dp.callback_query(F.data == 'send')
async def send(callback: types.CallbackQuery):
    ank = cur.execute(f'SELECT * FROM pre_mps WHERE userid == ?', [callback.from_user.id]).fetchone()
    id = random.randint(1111111111, 9999999999)
    data_check = datetime.datetime.now()
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, "Ваше мероприятие успешно отправлено в чат", reply_markup=nav.crl())
    if ank[9] == "-":
        if ank[3] == "-":
            dt = ank[2]
        else:
            dt = f"{ank[2]} - {ank[3]}"
        mess = f"⚙️ ID: {id}\n\n✅ <b>{ank[1]}</b>\n⏰ {dt}\n📍 {ank[4]}\n"
        if ank[5] != "-":
            mess += f"👤 {ank[5]}\n\n{ank[6]}\n\n"
        else:
            mess += f"\n{ank[6]}\n\n"
        if ank[7] != "-":
            mess += f"💸 Цена: {ank[7]}\n\n"
        mess += f"☎️ Контакты: {ank[10]}\n\n"
        if ank[8] != "-":
            mess += f"P.S. {ank[8]}\n\n"
        if callback.from_user.username != None:
            mess += f"Опубликовал: @{callback.from_user.username}"
        msg = await bot.send_message(-1002001083190, mess, parse_mode='HTML')
        cur.execute('INSERT INTO mps VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [id, callback.from_user.id, ank[1], ank[2], ank[3], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10], data_check, msg.message_id])
        base.commit()
        cur.execute(f'DELETE FROM pre_mps WHERE userid == ?', [callback.from_user.id])
        base.commit()
    else:
        if ank[3] == "-":
            dt = ank[2]
        else:
            dt = f"{ank[2]} - {ank[3]}"
        mess = f"⚙️ ID: {id}\n\n✅ <b>{ank[1]}</b>\n⏰ {dt}\n📍 {ank[4]}\n"
        if ank[5] != "-":
            mess += f"👤 {ank[5]}\n\n{ank[6]}\n\n"
        else:
            mess += f"\n{ank[6]}\n\n"
        if ank[7] != "-":
            mess += f"💸 Цена: {ank[7]}\n\n"
        mess += f"☎️ Контакты: {ank[10]}\n\n"
        if ank[8] != "-":
            mess += f"P.S. {ank[8]}\n"
        if callback.from_user.username != None:
            mess += f"\nОпубликовал: @{callback.from_user.username}\n"
            mess += f'<a href="{ank[10]}">ㅤ</a>'
        else:
            mess += f'\n<a href="{ank[10]}">ㅤ</a>'
        msg = await bot.send_message(-1002001083190, mess, parse_mode='HTML')
        cur.execute('INSERT INTO mps VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [id, callback.from_user.id, ank[1], ank[2], ank[3], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10], data_check, msg.message_id])
        base.commit()
        cur.execute(f'DELETE FROM pre_mps WHERE userid == ?', [callback.from_user.id])
        base.commit()

@dp.message(F.text.lower() == 'редактировать мероприятие')
async def editmp(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Укажите id обьявления которое хотите отредактировать")
    await state.set_state(Other.editmpid)

@dp.message(Other.editmpid, F.text)
async def editmpid(message: types.Message, state: FSMContext):
    await state.clear()
    if is_number(message.text):
        ank = cur.execute(f'SELECT * FROM mps WHERE id == ?', [message.text]).fetchone()
        if ank:
            if int(ank[1]) != int(message.from_user.id) and int(message.from_user.id) != int(adminid()):
                await bot.send_message(message.from_user.id, "Вы не можете редактировать чужое обьявление")
            else:
                edt = cur.execute(f'SELECT * FROM mps_edit WHERE userid == ?', [message.from_user.id]).fetchone()
                if edt:
                    cur.execute(f'DELETE FROM mps_edit WHERE userid == ?', [message.from_user.id])
                    base.commit()
                cur.execute('INSERT INTO mps_edit VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [ank[0], message.from_user.id, ank[2], ank[3], ank[4], ank[5], ank[6], ank[7], ank[8], ank[9], ank[10], ank[11], ank[13]])
                base.commit()
                await bot.send_message(message.from_user.id, "Выберите поля для заполнения или редактирования", reply_markup=nav.editbuttons(ank[2], ank[3], ank[5], ank[6], ank[7], ank[8], ank[9], ank[11]))
                mess = await bot.send_message(message.from_user.id, "1", reply_markup=nav.crl())
                await bot.delete_message(message.from_user.id, mess.message_id)  # удавление клавиатуры
        else:
            await bot.send_message(message.from_user.id, "Мероприятия с таким id не существует")
    else:
        await bot.send_message(message.from_user.id, "Вы указали не число")

@dp.callback_query(F.data == 'name_edit')
async def name(callback: types.CallbackQuery, state: FSMContext):
    ank = cur.execute(f'SELECT name FROM mps_edit WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Название * (обязательно к заполнению).\n"
                                     'Введите название вашего мероприятия, оно должно быть кратким. Нажмите "⏪ Назад", чтобы вернуться к другим пунктам описания.\n\n'
                                     f'Текущее значение поля: {ank[0]}', reply_markup=nav.back_edit())
    await state.set_state(Other.name_edit)

@dp.message(Other.name_edit, F.text)
async def name(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.name_edit)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    await state.clear()
    cur.execute(f'UPDATE mps_edit SET name == ? WHERE userid == ?', [message.text, message.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM mps_edit WHERE userid == ?', [message.from_user.id]).fetchone()
    await bot.send_message(message.from_user.id, 'Выберите поля для заполнения или редактирования', reply_markup=nav.editbuttons(ank[2], ank[3], ank[5], ank[6], ank[7], ank[8], ank[9], ank[11]))

@dp.callback_query(F.data == 'date_edit')
async def date(callback: types.CallbackQuery, state: FSMContext):
    ank = cur.execute(f'SELECT * FROM mps_edit WHERE userid == ?', [callback.from_user.id]).fetchone()
    if ank[4] == "-":
        dt = "Не указанно"
    else:
        dt = ank[4]
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Дата/время * (обязательно к заполнению).\n"
                                     f'Введите дату начала вашего мероприятия и нажмите отправить. Нажмите "⏪ Назад", чтобы вернуться к другим пунктам описания.\n\n'
                                     f'Формат указания времени: день.месяц.год чч:мм\n\n'
                                     f'Пример заполнения: 26.03.2024 15:30\n\n'
                                     f'Текущее значение поля: {ank[3]}(начало) | {dt}(конец)', reply_markup=nav.back_edit())
    await state.set_state(Other.date_edit)

@dp.message(Other.date_edit, F.text)
async def date(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.date_edit)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    try:
        datetime.datetime.strptime(message.text, '%d.%m.%Y %H:%M')
    except:
        await state.set_state(Other.date)
        return await bot.send_message(message.from_user.id, 'Вы указали не верный формат времени, заполните заново или нажмите кнопку "⏪ Назад"')
    await state.update_data(date_start = message.text)
    await bot.send_message(message.from_user.id, "Укажите дату окончания мероприятия, если хотите пропустить то нажмите на кнопку ниже", reply_markup=nav.pass_time_edt())
    await state.set_state(Other.end_date_edit)

@dp.callback_query(StateFilter("*"), F.data == 'pass_time_edt')
async def pass_time_edt(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cur.execute(f'UPDATE mps_edit SET date_start == ? WHERE userid == ?', [data["date_start"], callback.from_user.id])
    cur.execute(f'UPDATE mps_edit SET date_end == ? WHERE userid == ?', ["-", callback.from_user.id])
    base.commit()
    await state.clear()
    ank = cur.execute(f'SELECT * FROM mps_edit WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text('Выберите поля для заполнения или редактирования', reply_markup=nav.editbuttons(ank[2], ank[3], ank[5], ank[6], ank[7], ank[8], ank[9], ank[11]))

@dp.message(Other.end_date_edit, F.text)
async def end_date(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.end_date_edit)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    try:
        datetime.datetime.strptime(message.text, '%d.%m.%Y %H:%M')
    except:
        await state.set_state(Other.end_date_edit)
        return await bot.send_message(message.from_user.id, 'Вы указали не верный формат времени, заполните заново или нажмите кнопку "⏪ Назад"')
    data = await state.get_data()
    cur.execute(f'UPDATE mps_edit SET date_start == ? WHERE userid == ?', [data["date_start"], message.from_user.id])
    cur.execute(f'UPDATE mps_edit SET date_end == ? WHERE userid == ?', [message.text, message.from_user.id])
    base.commit()
    await state.clear()
    ank = cur.execute(f'SELECT * FROM mps_edit WHERE userid == ?', [message.from_user.id]).fetchone()
    await bot.send_message(message.from_user.id, 'Выберите поля для заполнения или редактирования', reply_markup=nav.editbuttons(ank[2], ank[3], ank[5], ank[6], ank[7], ank[8], ank[9], ank[11]))

@dp.callback_query(F.data == 'adres_edit')
async def adres(callback: types.CallbackQuery, state: FSMContext):
    ank = cur.execute(f'SELECT adress FROM mps_edit WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Адрес * (обязательно к заполнению).\n"
                                     'Напишите адрес проведения мероприятия и нажмите кнопку отправить, или нажмите "⏪ Назад", чтобы вернуться к другим пунктам описания.\n\n'
                                     'Формат указания адреса: (населенный пункт/курорт), (улица), (номер дома), (квартира), (примечание)\n\n'
                                     'Пример заполнения: Красная Поляна, ул. Пчеловодов, 23 (Парк шале)\n\n'
                                     f'Текущее значение поля: {ank[0]}', reply_markup=nav.back_edit())
    await state.set_state(Other.adres_edit)

@dp.message(Other.adres_edit, F.text)
async def adres(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.adres_edit)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    await state.clear()
    cur.execute(f'UPDATE mps_edit SET adress == ? WHERE userid == ?', [message.text, message.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM mps_edit WHERE userid == ?', [message.from_user.id]).fetchone()
    await bot.send_message(message.from_user.id, 'Выберите поля для заполнения или редактирования', reply_markup=nav.editbuttons(ank[2], ank[3], ank[5], ank[6], ank[7], ank[8], ank[9], ank[11]))

@dp.callback_query(F.data == 'who_edit')
async def who(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Кто проводит.\n"
                                     'Напишите Фамилию и Имя человека который проводит мероприятие - лектор, инструктор или др. Можно указать несколько. При желании, после имени можно коротко указать профиль работы.\n\n'
                                     'Этот пункт может отличаться от пункта “Контакты” в котором мы указываем контакты организатора мероприятия и человека у которого можно уточнить все подробности. Однако “Кто проводит” и  контакты организатора могут совпадать. Подробнее см. в пункте “Контакты”.\n\n'
                                     '❗️Ссылки в этом пункте запрещены, их можно будет указать в описании мероприятия.\n\n'
                                     'Пример заполнения:\n'
                                     'Иванова Галина, художник и декоратор с опытом работа 15 лет.\n'
                                     'Сурков Михаил, дизайнер интерьеров\n\n'
                                     'После заполнения данных нажмите на кнопку отправить, или нажмите "⏪ Назад", чтобы вернуться к другим пунктам описания\n\n', reply_markup=nav.back_edit())
    await state.set_state(Other.who_edit)

@dp.message(Other.who_edit, F.text)
async def who(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.who_edit)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    await state.clear()
    cur.execute(f'UPDATE mps_edit SET who == ? WHERE userid == ?', [message.text, message.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM mps_edit WHERE userid == ?', [message.from_user.id]).fetchone()
    await bot.send_message(message.from_user.id, 'Выберите поля для заполнения или редактирования', reply_markup=nav.editbuttons(ank[2], ank[3], ank[5], ank[6], ank[7], ank[8], ank[9], ank[11]))

@dp.callback_query(F.data == 'who_edit_ad')
async def who(callback: types.CallbackQuery, state: FSMContext):
    ank = cur.execute(f'SELECT who FROM mps_edit WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Кто проводит.\n"
                                     'Напишите Фамилию и Имя человека который проводит мероприятие - лектор, инструктор или др. Можно указать несколько. При желании, после имени можно коротко указать профиль работы.\n\n'
                                     'Этот пункт может отличаться от пункта “Контакты” в котором мы указываем контакты организатора мероприятия и человека у которого можно уточнить все подробности. Однако “Кто проводит” и  контакты организатора могут совпадать. Подробнее см. в пункте “Контакты”.\n\n'
                                     '❗️Ссылки в этом пункте запрещены, их можно будет указать в описании мероприятия.\n\n'
                                     'Пример заполнения:\n'
                                     'Иванова Галина, художник и декоратор с опытом работа 15 лет.\n'
                                     'Сурков Михаил, дизайнер интерьеров\n\n'
                                     'После заполнения данных нажмите на кнопку отправить, или нажмите "⏪ Назад", чтобы вернуться к другим пунктам описания\n\n'
                                     f'Текущее значение поля: {ank[0]}', reply_markup=nav.back_edit())
    await state.set_state(Other.who_edit)

@dp.callback_query(F.data == 'descrip_edit')
async def descrip_ad(callback: types.CallbackQuery, state: FSMContext):
    ank = cur.execute(f'SELECT descrip FROM mps_edit WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Описание * (обязательно к заполнению).\n"
                                     'Опишите мероприятие и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам.\n\n'
                                     'Постарайтесь быть краткими, но содержательными. Напишите главное, остальное участники смогут уточнить связавшись с вами лично.\n\n'
                                     '⚠️Внимание! Ограничение на объёму текста 1200 символов (включая пробелы).\n\n'
                                     f'Текущее значение поля: {ank[0]}', reply_markup=nav.back_edit())
    await state.set_state(Other.descrip_edit)

@dp.message(Other.descrip_edit, F.text)
async def descrip(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.descrip_edit)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    await state.clear()
    if len(message.text) <= 1200:
        cur.execute(f'UPDATE mps_edit SET descrip == ? WHERE userid == ?', [message.text, message.from_user.id])
        base.commit()
        ank = cur.execute(f'SELECT * FROM mps_edit WHERE userid == ?', [message.from_user.id]).fetchone()
        await bot.send_message(message.from_user.id, 'Выберите поля для заполнения или редактирования', reply_markup=nav.editbuttons(ank[2], ank[3], ank[5], ank[6], ank[7], ank[8], ank[9], ank[11]))
    else:
        await bot.send_message(message.from_user.id, "Ваше описание привышает возможную длинну 1200 символов(включая пробелы)", reply_markup=nav.back_edit())

@dp.callback_query(F.data == 'count_edit')
async def count(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Цена.\n"
                                     'Напишите стоимость участия и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания.', reply_markup=nav.back_edit())
    await state.set_state(Other.count_edit)

@dp.message(Other.count_edit, F.text)
async def count(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.count_edit)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    await state.clear()
    cur.execute(f'UPDATE mps_edit SET count == ? WHERE userid == ?', [message.text, message.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM mps_edit WHERE userid == ?', [message.from_user.id]).fetchone()
    await bot.send_message(message.from_user.id, 'Выберите поля для заполнения или редактирования', reply_markup=nav.editbuttons(ank[2], ank[3], ank[5], ank[6], ank[7], ank[8], ank[9], ank[11]))

@dp.callback_query(F.data == 'count_edit_ad')
async def count_ad(callback: types.CallbackQuery, state: FSMContext):
    ank = cur.execute(f'SELECT count FROM mps_edit WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text("🔄 Вы сейчас редактируете поле Цена.\n"
                                     'Напишите стоимость участия и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания.\n\n'
                                     f'Текущее значение поля: {ank[0]}', reply_markup=nav.back_edit())
    await state.set_state(Other.count_edit)

@dp.callback_query(F.data == 'prim_edit')
async def prim(callback: types.CallbackQuery):
    await callback.message.edit_text("Содержание поля по умолчанию:\n"
                                     'Участие строго по записи. Всю дополнительную информацию вы можете получить у организатора!\n\n'
                                     'Если для вашего мероприятия это актуально, то нажмите кнопку “Добавить”.\n'
                                     'Нажмите кнопку “Не добавлять”, чтобы пропустить это поле.', reply_markup=nav.ps_edit())

@dp.callback_query(F.data == 'add_edit')
async def add(callback: types.CallbackQuery):
    cur.execute(f'UPDATE mps_edit SET prim == ? WHERE userid == ?', ["Участие строго по записи. Всю дополнительную информацию вы можете получить у организатора!", callback.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM mps_edit WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text('Выберите поля для заполнения или редактирования', reply_markup=nav.editbuttons(ank[2], ank[3], ank[5], ank[6], ank[7], ank[8], ank[9], ank[11]))

@dp.callback_query(F.data == 'noadd_edit')
async def add(callback: types.CallbackQuery):
    cur.execute(f'UPDATE mps_edit SET prim == ? WHERE userid == ?', ["-", callback.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM mps_edit WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text('Выберите поля для заполнения или редактирования', reply_markup=nav.editbuttons(ank[2], ank[3], ank[5], ank[6], ank[7], ank[8], ank[9], ank[11]))

@dp.callback_query(F.data == 'prim_edit_ad')
async def prim(callback: types.CallbackQuery):
    await callback.message.edit_text("Содержание поля по умолчанию:\n"
                                     'Участие строго по записи. Всю дополнительную информацию вы можете получить у организатора!\n\n'
                                     'Если для вашего мероприятия это актуально, то нажмите кнопку “Добавить”.\n'
                                     'Нажмите кнопку “Не добавлять”, чтобы пропустить это поле.', reply_markup=nav.ps_edit())

@dp.callback_query(F.data == 'contact_edit')
async def contact(callback: types.CallbackQuery, state: FSMContext):
    ank = cur.execute(f'SELECT contact FROM mps_edit WHERE userid == ?', [callback.from_user.id]).fetchone()
    await callback.message.edit_text('🔄 Вы сейчас редактируете поле Контакты * (обязательно к заполнению).\n\n'
                                     'Укажите свои контакты и нажмите кнопку отправить, или нажмите назад, чтобы вернуться к другим пунктам описания.\n\n'
                                     'В этом пункте желательно указать свой ник в телеграм, чтобы участники смогли записаться или задать вам интересующие вопросы по мероприятию. По желанию можно указать свой номер телефона для связи.\n\n'
                                     'Формат размещения контактов: (ник в телеграм) (телефон) (имя)\n\n'
                                     'Пример заполнения: @shaman8888 +7(918)123-45-67 Антон\n\n'
                                     f'Текущее значение поля: {ank[0]}', reply_markup=nav.back_edit())
    await state.set_state(Other.contact_edit)

@dp.message(Other.contact_edit, F.text)
async def contact(message: types.Message, state: FSMContext):
    if "http" in message.text or "https" in message.text:
        await state.set_state(Other.contact_edit)
        return await bot.send_message(message.from_user.id, 'Ссылки запрещены, заполните еще раз или нажмите кнопку "⏪ Назад"', reply_markup=nav.back())
    if "@" not in message.text:
        await state.set_state(Other.contact_edit)
        return await bot.send_message(message.from_user.id, "Вы не указали телеграмм для связи")
    await state.clear()
    cur.execute(f'UPDATE prim_edit SET contact == ? WHERE userid == ?', [message.text, message.from_user.id])
    base.commit()
    ank = cur.execute(f'SELECT * FROM prim_edit WHERE userid == ?', [message.from_user.id]).fetchone()
    await bot.send_message(message.from_user.id, 'Выберите поля для заполнения или редактирования', reply_markup=nav.editbuttons(ank[2], ank[3], ank[5], ank[6], ank[7], ank[8], ank[9], ank[11]))

@dp.callback_query(F.data == 'show_edit')
async def show(callback: types.CallbackQuery):
    ank = cur.execute(f'SELECT * FROM mps_edit WHERE userid == ?', [callback.from_user.id]).fetchone()
    if ank[10] == "-":
        if ank[4] == "-":
            dt = ank[3]
        else:
            dt = f"{ank[3]} - {ank[4]}"
        mess = f"⚙️ ID: {ank[0]}\n\n✅ <b>{ank[2]}</b>\n⏰ {dt}\n📍 {ank[5]}\n"
        if ank[6] != "-":
            mess += f"👤 {ank[6]}\n\n{ank[7]}\n\n"
        else:
            mess += f"\n{ank[7]}\n\n"
        if ank[8] != "-":
            mess += f"💸 Цена: {ank[8]}\n\n"
        mess += f"☎️ Контакты: {ank[11]}\n\n"
        if ank[9] != "-":
            mess += f"P.S. {ank[9]}\n\n"
        if callback.from_user.username != None:
            mess += f"Опубликовал: @{callback.from_user.username}"
        await callback.message.edit_text(mess, parse_mode='HTML', reply_markup=nav.back_show_edit())
    else:
        if ank[4] == "-":
            dt = ank[3]
        else:
            dt = f"{ank[3]} - {ank[4]}"
        mess = f"⚙️ ID: {ank[0]}\n\n✅ <b>{ank[2]}</b>\n⏰ {dt}\n📍 {ank[5]}\n"
        if ank[6] != "-":
            mess += f"👤 {ank[6]}\n\n{ank[7]}\n\n"
        else:
            mess += f"\n{ank[7]}\n\n"
        if ank[8] != "-":
            mess += f"💸 Цена: {ank[8]}\n\n"
        mess += f"☎️ Контакты: {ank[11]}\n\n"
        if ank[9] != "-":
            mess += f"P.S. {ank[9]}\n"
        if callback.from_user.username != None:
            mess += f"Опубликовал: @{callback.from_user.username}\n"
            mess += f'<a href="{ank[10]}">ㅤ</a>'
        else:
            mess += f'\n<a href="{ank[10]}">ㅤ</a>'
        await callback.message.edit_text(mess, parse_mode='HTML', reply_markup=nav.back_show_edit())

@dp.callback_query(StateFilter("*"), F.data == 'back_ank_edit')
async def back_ank(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    ank = cur.execute(f'SELECT * FROM mps_edit WHERE userid == ?', [callback.from_user.id]).fetchone()
    try:
        await callback.message.edit_text('Выберите поля для заполнения или редактирования', reply_markup=nav.editbuttons(ank[2], ank[3], ank[5], ank[6], ank[7], ank[8], ank[9], ank[11]))
    except:
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await bot.send_message(callback.from_user.id, 'Выберите поля для заполнения или редактирования', reply_markup=nav.editbuttons(ank[2], ank[3], ank[5], ank[6], ank[7], ank[8], ank[9], ank[11]))

@dp.callback_query(F.data == 'back_show_edit')
async def back_show(callback: types.CallbackQuery):
    ank = cur.execute(f'SELECT * FROM mps_edit WHERE userid == ?', [callback.from_user.id]).fetchone()
    try:
        await callback.message.edit_text('Выберите поля для заполнения или редактирования', reply_markup=nav.editbuttons(ank[2], ank[3], ank[5], ank[6], ank[7], ank[8], ank[9], ank[11]))
    except:
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await bot.send_message(callback.from_user.id, 'Выберите поля для заполнения или редактирования', reply_markup=nav.editbuttons(ank[2], ank[3], ank[5], ank[6], ank[7], ank[8], ank[9], ank[11]))

@dp.callback_query(F.data == 'cancel_edit')
async def cancel(callback: types.CallbackQuery):
    cur.execute(f'DELETE FROM mps_edit WHERE userid == ?', [callback.from_user.id])
    base.commit()
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, "Вы вышли в главное меню", reply_markup=nav.crl())

@dp.callback_query(F.data == 'send_edit')
async def send_edit(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, "Вы успешно отредактировали мероприятие", reply_markup=nav.crl())
    ank = cur.execute(f'SELECT * FROM mps_edit WHERE userid == ?', [callback.from_user.id]).fetchone()
    if ank[10] == "-":
        if ank[4] == "-":
            dt = ank[3]
        else:
            dt = f"{ank[3]} - {ank[4]}"
        mess = f"⚙️ ID: {ank[0]}\n\n✅ <b>{ank[2]}</b>\n⏰ {dt}\n📍 {ank[5]}\n"
        if ank[6] != "-":
            mess += f"👤 {ank[6]}\n\n{ank[7]}\n\n"
        else:
            mess += f"\n{ank[7]}\n\n"
        if ank[8] != "-":
            mess += f"💸 Цена: {ank[8]}\n\n"
        mess += f"☎️ Контакты: {ank[11]}\n\n"
        if ank[9] != "-":
            mess += f"P.S. {ank[9]}\n\n"
        if callback.from_user.username != None:
            mess += f"Опубликовал: @{callback.from_user.username}"
        await bot.edit_message_text(mess, mpchanelid, ank[12], parse_mode='HTML')
        cur.execute(f'UPDATE mps SET name == ? WHERE id == ?', [ank[2], ank[0]])
        cur.execute(f'UPDATE mps SET date_start == ? WHERE id == ?', [ank[3], ank[0]])
        cur.execute(f'UPDATE mps SET date_end == ? WHERE id == ?', [ank[4], ank[0]])
        cur.execute(f'UPDATE mps SET adress == ? WHERE id == ?', [ank[5], ank[0]])
        cur.execute(f'UPDATE mps SET who == ? WHERE id == ?', [ank[6], ank[0]])
        cur.execute(f'UPDATE mps SET descrip == ? WHERE id == ?', [ank[7], ank[0]])
        cur.execute(f'UPDATE mps SET count == ? WHERE id == ?', [ank[8], ank[0]])
        cur.execute(f'UPDATE mps SET prim == ? WHERE id == ?', [ank[9], ank[0]])
        cur.execute(f'UPDATE mps SET contact == ? WHERE id == ?', [ank[11], ank[0]])
        base.commit()
        cur.execute(f'DELETE FROM mps_edit WHERE userid == ?', [callback.from_user.id])
        base.commit()
    else:
        if ank[4] == "-":
            dt = ank[3]
        else:
            dt = f"{ank[3]} - {ank[4]}"
        mess = f"⚙️ ID: {ank[0]}\n\n✅ <b>{ank[2]}</b>\n⏰ {dt}\n📍 {ank[5]}\n"
        if ank[6] != "-":
            mess += f"👤 {ank[6]}\n\n{ank[7]}\n\n"
        else:
            mess += f"\n{ank[7]}\n\n"
        if ank[8] != "-":
            mess += f"💸 Цена: {ank[8]}\n\n"
        mess += f"☎️ Контакты: {ank[11]}\n\n"
        if ank[9] != "-":
            mess += f"P.S. {ank[9]}\n"
        if callback.from_user.username != None:
            mess += f"\nОпубликовал: @{callback.from_user.username}\n"
            mess += f'<a href="{ank[10]}">ㅤ</a>'
        else:
            mess += f'\n<a href="{ank[10]}">ㅤ</a>'
        await bot.edit_message_text(mess, mpchanelid, ank[12], parse_mode='HTML')
    cur.execute(f'UPDATE mps SET name == ? WHERE id == ?', [ank[2], ank[0]])
    cur.execute(f'UPDATE mps SET date_start == ? WHERE id == ?', [ank[3], ank[0]])
    cur.execute(f'UPDATE mps SET date_end == ? WHERE id == ?', [ank[4], ank[0]])
    cur.execute(f'UPDATE mps SET adress == ? WHERE id == ?', [ank[5], ank[0]])
    cur.execute(f'UPDATE mps SET who == ? WHERE id == ?', [ank[6], ank[0]])
    cur.execute(f'UPDATE mps SET descrip == ? WHERE id == ?', [ank[7], ank[0]])
    cur.execute(f'UPDATE mps SET count == ? WHERE id == ?', [ank[8], ank[0]])
    cur.execute(f'UPDATE mps SET prim == ? WHERE id == ?', [ank[9], ank[0]])
    cur.execute(f'UPDATE mps SET contact == ? WHERE id == ?', [ank[11], ank[0]])
    base.commit()
    cur.execute(f'DELETE FROM mps_edit WHERE userid == ?', [callback.from_user.id])
    base.commit()

@dp.message(F.text.lower() == 'удалить мероприятие')
async def editmp(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Укажите id обьявления которое хотите удалить")
    mess = await bot.send_message(message.from_user.id, "1", reply_markup=nav.crl())
    await bot.delete_message(message.from_user.id, mess.message_id)  # удавление клавиатуры
    await state.set_state(Other.deletempid)

@dp.message(Other.deletempid, F.text)
async def deletempid(message: types.Message, state: FSMContext):
    await state.clear()
    if is_number(message.text):
        ank = cur.execute(f'SELECT * FROM mps WHERE id == ?', [message.text]).fetchone()
        if ank:
            if int(ank[1]) != int(message.from_user.id) and int(message.from_user.id) != int(adminid()):
                await bot.send_message(message.from_user.id, "Вы не можете удалить чужое обьявление")
            else:
                await bot.delete_message(mpchanelid, ank[13])
                cur.execute(f'DELETE FROM mps WHERE id == ?', [message.text])
                base.commit()
                await bot.send_message(message.from_user.id, "Вы успешно удалили мероприятие")

@dp.message(F.text.lower() == 'помощь и обратная связь')
async def supp(message: types.Message):
    await bot.send_message(message.from_user.id, "Если у вас возникли сложности при добавлении мероприятия в афишу,сформулируйте проблему в текстовом формате и отправьте @shaman8888")