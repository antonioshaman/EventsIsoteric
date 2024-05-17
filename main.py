import handlers.other
import commands.com
from starter.load_jsons import adminid, token
from starter.other import base, cur
from starter.loader import dp, bot
#from telegram.ext import Updater, CommandHandler
import asyncio


# все что касается логирования - начало
import logging
#from logging.handlers import RotatingFileHandler

logging.basicConfig(filename='bot.log', level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)  # установим уровень логирования

# настроим rfl
#handler = RotatingFileHandler('bot.log', maxBytes=5000000, backupCount=5)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#handler.setFormatter(formatter)

# добавляем обработчик к логеру
#logger.addHandler(handler)
# все что касается логирования - конец

#добавим для ловли обработчиком
def error_handler(update, context):
    logger.error(f"Ошибка в обработчике{update}: {context.error}")

async def main():
    base.execute("CREATE TABLE IF NOT EXISTS mps(id INT, userid INT, name TEXT, date_start TEXT, date_end TEXT, adress TEXT, who TEXT, descrip TEXT, count TEXT, prim TEXT, photo TEXT, contact TEXT, date_add TEXT, messageid INT)")
    base.execute("CREATE TABLE IF NOT EXISTS mps_edit(id INT, userid INT, name TEXT, date_start TEXT, date_end TEXT, adress TEXT, who TEXT, descrip TEXT, count TEXT, prim TEXT, photo TEXT, contact TEXT, messageid INT)")
    base.execute("CREATE TABLE IF NOT EXISTS pre_mps(userid INT, name TEXT, date_start TEXT, date_end TEXT, adress TEXT, who TEXT, descrip TEXT, count TEXT, prim TEXT, photo TEXT, contact TEXT)")
    base.commit()
#добавим для обработчика
	updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()
#конец вставки
    await bot.send_message(adminid(), 'Бот запущен!')
    print('Bot started...')
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())