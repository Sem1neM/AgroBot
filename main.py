import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile

API_TOKEN = 'token_here'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Команда start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! 🚜 Я бот, который поможет вам найти подходящие меры государственной поддержки для сельскохозяйственных производителей и кооперативов.\n\n"
        "Выберите категорию вашей деятельности:\n"
        "1️⃣ Самозанятый\n"
        "2️⃣ Личное подсобное хозяйство\n"
        "3️⃣ Индивидуальный предприниматель\n"
        "4️⃣ ИП или Глава КФХ\n"
        "5️⃣ Юридическое лицо или кооператив\n\n"
        "Чтобы узнать, что я умею, отправьте команду /help."
    )

# Команда help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Отправьте цифру, соответствующую вашей категории деятельности, чтобы получить информацию о доступных видах поддержки.")

# Обработка сообщений с цифрами (категории деятельности)
@dp.message_handler(lambda message: message.text.isdigit())
async def send_category_info(message: types.Message):
    category = int(message.text)
    response = "Информация по выбранной категории:"
    if category == 1:
        response += " Самозанятый..."
    elif category == 2:
        response += " Личное подсобное хозяйство..."
    elif category == 3:
        response += " Индивидуальный предприниматель..."
    elif category == 4:
        response += " ИП или Глава КФХ..."
    elif category == 5:
        response += " Юридическое лицо или кооператив..."
    else:
        response = "Пожалуйста, выберите категорию от 1 до 5."
    await message.reply(response)

# Команда navigation_map
@dp.message_handler(commands=['navigation_map'])
async def send_navigation_map(message: types.Message):
    navigation_map = InputFile('path_to__navigation_map.png')
    await message.answer_photo(navigation_map, caption="Вот дорожная карта входа в чат-бота. Она поможет вам ориентироваться!")

# Команда info
@dp.message_handler(commands=['info'])
async def send_info(message: types.Message):
    await message.reply("Информация о государственной поддержке: [описание видов поддержки, условий получения, необходимых документов и т.д.]")

# Команда contact
@dp.message_handler(commands=['contact'])
async def send_contact_info(message: types.Message):
    await message.reply("Если у вас есть вопросы, вы можете связаться с нами:\n\n"
                        "📞 Телефон: +7 123 456 7890\n"
                        "✉️ E-mail: support@example.com\n"
                        "🕘 Часы работы: Пн-Пт с 9:00 до 18:00")

# Команда feedback
@dp.message_handler(commands=['feedback'])
async def request_feedback(message: types.Message):
    await message.reply("Мы ценим ваше мнение! Пожалуйста, напишите ваш отзыв или вопросы касательно получения грантов и мы обязательно на них ответим.")

# Функция для запуска бота
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
