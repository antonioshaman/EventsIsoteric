from starter.loader import dp, bot
from aiogram.filters import CommandStart, StateFilter
from starter.load_jsons import mpchannel
from buttons import markups as nav
from aiogram import types

@dp.message(StateFilter(None), CommandStart())
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f'Добро пожаловать в бот Афиши мероприятий\n\n'
                                                 f'Следуя простой инструкции, вы можете самостоятельно опубликовать мероприятие в выбранной группе или канале.\n\n'
                                                 f'Размещение в афише бесплатное. Периодичность размещения 1️⃣ мероприятие в 3️⃣ дня. Размещение - моментальное. Мы рекомендуем размещать мероприятия минимум за 3-5 дней до его проведения.\n\n'
                                                 f'✅ На любом этапе заполнения информации о вашем мероприятии вы можете воспользоваться предпросмотром - для этого нажмите кнопку "Посмотреть".📝 Если вы совершили ошибку или после публикации необходимо внести правки - воспользуйтесь функцией "Редактировать мероприятие".\n\n'
                                                 f'❌ Если в процессе диалога будут проблемы отправьте команду /start чтоб перезапустить бота и начать с момента последнего редактирования.', reply_markup=nav.crl())