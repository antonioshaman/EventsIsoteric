import handlers.other
import commands.com
from starter.load_jsons import adminid, token
from starter.other import base, cur
from starter.loader import dp, bot
import asyncio
from aiogram import types


# все, что касается логирования - начало
import logging
from logging.handlers import RotatingFileHandler

reconstruction_mode = True


# Настоятельно рекомендуется использовать конфигурацию логгера с помощью RotatingFileHandler
# только внутри функции setup_logging для изоляции логирования
def setup_logging():
    logging.basicConfig(filename='bot.log', level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler('bot.log', maxBytes=5000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

# добавим обработчик ошибок с именем error_handler
def error_handler(update, context):
    logger.error(f"Ошибка в обработчике {update}:{context.error}")

# все, что касается логирования - конец


async def handle_reconstruction(update, context):
    if reconstruction_mode:
        await context.bot.send_message(update.effective_chat.id, 'Бот находится на реконструкции, приносим извинения за доставленные неудобства')


# перенесем запуск бота внутрь блока main
async def main():
    setup_logging()  # вызовем функцию настройки логгера
    base.execute("CREATE TABLE IF NOT EXISTS mps(id INT, userid INT, name TEXT, date_start TEXT, date_end TEXT, adress TEXT, who TEXT, descrip TEXT, count TEXT, prim TEXT, photo TEXT, contact TEXT, date_add TEXT, messageid INT)")
    base.execute("CREATE TABLE IF NOT EXISTS mps_edit(id INT, userid INT, name TEXT, date_start TEXT, date_end TEXT, adress TEXT, who TEXT, descrip TEXT, count TEXT, prim TEXT, photo TEXT, contact TEXT, messageid INT)")
    base.execute("CREATE TABLE IF NOT EXISTS pre_mps(userid INT, name TEXT, date_start TEXT, date_end TEXT, adress TEXT, who TEXT, descrip TEXT, count TEXT, prim TEXT, photo TEXT, contact TEXT)")
    base.commit()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.send_message(adminid(), 'Бот запущен!')
    print('Bot started...')
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
