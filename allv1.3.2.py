from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.router import Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import F
import logging
import asyncio
import random
from datetime import datetime, timedelta

# Ваш токен от BotFather
BOT_TOKEN = "7901721463:AAGMGelSlGnD6aPDFN4puKAySG7t2G2lwRs"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Карты и их названия + ссылки на изображения
CARDS = {
    "https://picloud.cc/images/536815a3eec9133c0748e67f8ddacc67.png": "Тройка Пентаклей — мастерство, сотрудничество",
    "https://picloud.cc/images/d7ba9b5c9a02865cd371cd10bc8c0ae5.png": "Двойка Пентаклей — баланс, гибкость",
    "https://picloud.cc/images/7705dcbd33a596d76cddb39c633ce9b6.png": "Королева Кубков — интуиция, забота",
    "https://picloud.cc/images/0383829dbe5718029afdeffa9605f30b.png": "Страница Кубков — исследование, любопытство",
    "https://picloud.cc/images/168cabdf3aab9751a234f9b1339798be.png": "Рыцарь Кубков — романтика, идеализм",
    "https://picloud.cc/images/4cddf42a4adb1e6e456900452fa36f5d.png": "Король Кубков — эмоции, зрелость",
    "https://picloud.cc/images/396d5c1478d0ec91cfd5ac65649b22f6.png": "Туз Кубков — новые возможности, чувства",
    "https://picloud.cc/images/f06505b40f26f1043c4f56ef4691e347.png": "Десятка Кубков — семейное счастье",
    "https://picloud.cc/images/0ac1e2e2dfce45fb633048c2c36168bc.png": "Девятка Кубков — исполнение желаемого",
    "https://picloud.cc/images/470ca0ae868e5dfa9cfcd8823d73ec6b.png": "Восьмёрка Кубков — уход, поиски",
    "https://picloud.cc/images/74c1669ea037e70ee799ca4365caf7ac.png": "Семёрка Кубков — иллюзии, мечты",
    "https://picloud.cc/images/2cd5530f363ef379daec4a7f81f2c1bf.png": "Шестёрка Кубков — ностальгия, радость",
    "https://picloud.cc/images/29a4d64df844295138211e7a52e998d0.png": "Пятёрка Кубков — сожаление, потеря",
    "https://picloud.cc/images/e9ea7b08e934cd2fba634e3c630b1ee9.png": "Четвёрка Кубков — скука, разочарование",
    "https://picloud.cc/images/cde536f2e43471030d6120824a2009b9.png": "Тройка Кубков — радость, общение",
    "https://picloud.cc/images/f2ef2b9730049101ac198478398d4169.png": "Двойка Кубков — союз, гармония",
    "https://picloud.cc/images/436f164ea0166cc860b81fdfeac37605.png": "Мир — завершение, полнота",
    "https://picloud.cc/images/defb8b41fb41aadd5016d611713ef578.png": "Башня — разрушение, кардинальные перемены",
    "https://picloud.cc/images/67c91d2274bb59cedd6cadf18262ecbe.png": "Умеренность — баланс, терпение",
    "https://picloud.cc/images/5a28cda2c2be0da173b4b5b336992bc8.png": "Солнце — радость, успех",
    "https://picloud.cc/images/bef4d1a57151f1932fc6da988abc017d.png": "Сила — внутреннее преодоление",
    "https://picloud.cc/images/04725a9504039aad2475b62ee0c5130e.png": "Звезда — надежда, вдохновение",
    "https://picloud.cc/images/45904c843a5c143e2ce1359d653e5e73.png": "Жрица — интуиция, тайна",
    "https://picloud.cc/images/ce8991cd16354e30e8bfbbe25e009aa7.png": "Луна — иллюзии, интуиция",
    "https://picloud.cc/images/55bcc51094e012985f79067839788305.png": "Маг — сила воли, мастерство",
    "https://picloud.cc/images/bd63d273dd8040e120b4d156d7c05466.png": "Влюблённые — выбор, любовь",
    "https://picloud.cc/images/506b943c771df7a584902c534a4abb18.png": "Правосудие — справедливость, карма",
    "https://picloud.cc/images/d678f0f26a79a487c603346012f76ccb.png": "Суд — возрождение, искупление",
    "https://picloud.cc/images/e69e913669efa2eb3392744a262578ef.png": "Иерофант — традиции, обучение",
    "https://picloud.cc/images/7407a2fa56975bc85e45379cdd7b8a0e.png": "Отшельник — поиск, одиночество",
    "https://picloud.cc/images/4009a81efc6ad2278f3a02b72253721a.png": "Повешенный — жертвенность, новый взгляд",
    "https://picloud.cc/images/3f032af5aac3676bff3479f2695f742c.png": "Колесо Фортуны — цикличность, удача",
    "https://picloud.cc/images/df2b181ea039109078da13bc820d28b5.png": "Дурак — начало, спонтанность",
    "https://picloud.cc/images/c0a6dd82b3007ac867627f2b121296c0.png": "Императрица — плодородие, изобилие",
    "https://picloud.cc/images/462a5409eced955139cc8ea900bb032f.png": "Император — власть, структура",
    "https://picloud.cc/images/a574fad548cf0a6f5df7b3af087cd349.png": "Дьявол — искушение, привязанности",
    "https://picloud.cc/images/59da81076975fa5bded9437d33aacd4b.png": "Колесница — контроль, движение",
    "https://picloud.cc/images/c95f57711710c2602cf49b4fd9662c2c.png": "Пятёрка Мечей — конфликт, поражение",
    "https://picloud.cc/images/470b3353312d902faa33b318b4a3d9b5.png": "Смерть — завершение, трансформация",
    "https://picloud.cc/images/509cdcc41dacf9738126785b56d3ff8b.png": "Королева Жезлов — страсть, независимость",
    "https://picloud.cc/images/6a45cbeeb787122f400c70ab2f868309.png": "Страница Жезлов — исследование, новаторство",
    "https://picloud.cc/images/2b96883e7e53395c95e84a8b6e837edb.png": "Рыцарь Жезлов — энергия, решимость",
    "https://picloud.cc/images/72300a452507523e8cc8d0fe9963a95b.png": "Король Жезлов — авторитет, лидерство",
    "https://picloud.cc/images/9015aad28c7dc357111ebf8518285343.png": "Туз Жезлов — начало, вдохновение",
    "https://picloud.cc/images/3e279100d2f9516f9b23246a3648ff5e.png": "Десятка Жезлов — перегрузка, ответственность",
    "https://picloud.cc/images/3f56a7b64a3b2206415d6c7b44686572.png": "Девятка Жезлов — устойчивость, защита",
    "https://picloud.cc/images/81b6dd9820174a9c6253766c0de27039.png": "Восьмёрка Жезлов — скорость, движение",
    "https://picloud.cc/images/f9bf9f719f56f0e36cc8a212875d765e.png": "Семёрка Жезлов — сопротивление, борьба",
    "https://picloud.cc/images/bfae4133a6222eaf51f03991f7bb712b.png": "Шестёрка Жезлов — успех, признание",
    "https://picloud.cc/images/de69eec460b53077f45cc2c47cfefac9.png": "Пятёрка Жезлов — конкуренция, борьба",
    "https://picloud.cc/images/ab0a187617bce0af2e72c3159f70fadd.png": "Четвёрка Жезлов — празднование, стабильность",
    "https://picloud.cc/images/caecc11a60f412e96a07c87f12881efd.png": "Тройка Жезлов — расширение, прогресс",
    "https://picloud.cc/images/19445d6cf9571379a564bb9425b7560f.png": "Двойка Жезлов — выбор, стратегия",
    "https://picloud.cc/images/4c9abfa0be1e162513a46e2c23df07ad.png": "Королева Мечей — ясность, независимость",
    "https://picloud.cc/images/21d21074148ca4e080e3cbed256a8591.png": "Страница Мечей — любопытство, наблюдение",
    "https://picloud.cc/images/f4c148ae27ff55d6a70328795986f8d2.png": "Рыцарь Мечей — решительность, агрессия",
    "https://picloud.cc/images/5e53741173885d5b62e71c219bc7440f.png": "Король Мечей — разум, власть",
    "https://picloud.cc/images/7900132e560d27c54b90ccc110296ab6.png": "Туз Мечей — ясность, истина",
    "https://picloud.cc/images/649174aa3a155322b15bf83a348dc18c.png": "Десятка Мечей — завершение, трагедия",
    "https://picloud.cc/images/40761bacdd9a457f0dbaeee85fd5e997.png": "Девятка Мечей — страх, беспокойство",
    "https://picloud.cc/images/331b8623f22b36446c531754ad372456.png": "Восьмёрка Мечей — ограничение, блокировка",
    "https://picloud.cc/images/5bc58684d6f529c50445c5ef7684fa40.png": "Семёрка Мечей — обман, скрытность",
    "https://picloud.cc/images/7f88e27b4448070db2c352b529d261af.png": "Шестёрка Мечей — путешествия, переход",
    "https://picloud.cc/images/587875ddefc6f10f48b15593bc947caa.png": "Пятёрка Мечей — конфликт, поражение",
    "https://picloud.cc/images/34ba4c6e38b238105a8715c3bc97163c.png": "Тройка Мечей — боль, утрата",
    "https://picloud.cc/images/33e30dd9b663135723f10f8f205da986.png": "Двойка Мечей — выбор, блокировка",
    "https://picloud.cc/images/cc8adbee8d68697faf862f4b775018da.png": "Королева Пентаклей — забота, материальность",
    "https://picloud.cc/images/95323cbb97d7b3b590ca60d552861fa9.png": "Страница Пентаклей — учёба, начало",
    "https://picloud.cc/images/c8bc8f06c7a7aad9f8b6497962505cb5.png": "Рыцарь Пентаклей — стабильность, усердие",
    "https://picloud.cc/images/b2cfdca2eb73fb428a900e233279c607.png": "Король Пентаклей — успех, богатство",
    "https://picloud.cc/images/8d177ab935012420f9811efa15b1f32c.png": "Туз Пентаклей — начало, благополучие",
    "https://picloud.cc/images/6a4c5eb34db09bfec82283bbc2daddca.png": "Десятка Пентаклей — стабильность, наследие",
    "https://picloud.cc/images/ff6e3defdaf45f9f1d59a0847a26089f.png": "Девятка Пентаклей — успех, независимость",
    "https://picloud.cc/images/4528d901163ea607713f67a61afef15c.png": "Восьмёрка Пентаклей — усердие, мастерство",
    "https://picloud.cc/images/f863ef828c83ea8fc49d164793d3d69b.png": "Семёрка Пентаклей — терпение, анализ",
    "https://picloud.cc/images/cb76e83434f41c8a9c1e902ad844713a.png": "Шестёрка Пентаклей — баланс, щедрость",
    "https://picloud.cc/images/384fde7293a2c35a04cba1ba296320db.png": "Пятёрка Пентаклей — нужда, бедность",
    "https://picloud.cc/images/8155176e355b9093e86377e48fe52e06.png": "Четвёрка Пентаклей — удержание, накопление"
}

# Кнопки стартового меню
def create_start_menu(user_id):
    menu = [
        [KeyboardButton(text="✨ Сделать расклад")],
        [KeyboardButton(text="💰 Баланс раскладов")],
        [KeyboardButton(text="📖 Узнать про колоду")],

    ]
    
    if user_data.get(user_id, {}).get("free_today", False) == False:
        menu.insert(0, [KeyboardButton(text="🎁 Бесплатный расклад")])
    
    return ReplyKeyboardMarkup(
        keyboard=menu,
        resize_keyboard=True
    )

# Кнопки выбора расклада
spread_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💫 Три карты")],
        [KeyboardButton(text="🔮 Кельтский крест")],
        [KeyboardButton(text="💖 Отношения")],
        [KeyboardButton(text="💰 Баланс раскладов")]
    ],
    resize_keyboard=True
)


# Обработчик кнопки "📖 Узнать про колоду"
@router.message(F.text == "📖 Узнать про колоду")
async def about_deck(message: types.Message):
    await message.answer("🃏 Колода Райдера — Уэйта содержит 78 карт: Старшие и Младшие Арканы 🌹 \nОни помогают в самопознании и анализе жизненных ситуаций ⭐️")
# Кнопка для нового расклада
new_spread_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔄 Новый расклад")],
        [KeyboardButton(text="💰 Баланс раскладов")],
        [KeyboardButton(text="🏠 Главное меню")]
    ],
    resize_keyboard=True
)

# Кнопка оплаты
pay_button = ReplyKeyboardMarkup(
    keyboard=[
     [KeyboardButton(text="💳 Получить 10 раскладов за 99 рублей")],
     [KeyboardButton(text="🏠 Главное меню")]

     ],
    resize_keyboard=True
)

# Для хранения данных пользователей
user_data = {}

# Обработчик команды /start
@router.message(F.text == "/start")
async def start(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'free_today': False, 'paid_spreads': 0, 'last_free_spread': None}
    await message.answer("Добро пожаловать в Таро-Бот v1.3! Выберите действие:", reply_markup=create_start_menu(user_id))

# Обработчик кнопки "💰 Баланс раскладов"
@router.message(F.text == "💰 Баланс раскладов")
async def check_balance(message: types.Message):
    user_id = message.from_user.id
    balance = user_data.get(user_id, {}).get('paid_spreads', 0)
    if not user_data[user_id]['free_today']:
        balance += 1  # Добавляем бесплатный расклад, если он не был использован
    await message.answer(f"💡 У вас осталось {balance} раскладов.", reply_markup=create_start_menu(user_id))

# Обработчик кнопки "🎁 Бесплатный расклад"
@router.message(F.text == "🎁 Бесплатный расклад")
async def free_spread(message: types.Message):
    user_id = message.from_user.id
    
    # Проверка времени последнего бесплатного расклада
    if user_data[user_id]['last_free_spread'] and datetime.now() - user_data[user_id]['last_free_spread'] < timedelta(days=1):
        await message.answer("Вы уже использовали бесплатный расклад сегодня. Попробуйте позже.", reply_markup=create_start_menu(user_id))
        return

    user_data[user_id]['free_today'] = True
    user_data[user_id]['last_free_spread'] = datetime.now()
    await message.answer("Выберите тип расклада:", reply_markup=spread_menu)

# Обработчик кнопки "✨ Сделать расклад"
@router.message(F.text == "✨ Сделать расклад")
async def make_spread(message: types.Message):
    user_id = message.from_user.id
    balance = user_data.get(user_id, {}).get('paid_spreads', 0)

    # Проверка бесплатного расклада
    if not user_data[user_id]['free_today']:
        balance += 1  # Бесплатный расклад учитывается до использования

    if balance > 0:
        if not user_data[user_id]['free_today']:
            user_data[user_id]['free_today'] = True  # Используем бесплатный
        else:
            user_data[user_id]['paid_spreads'] -= 1  # Уменьшаем платный баланс
        await message.answer("Выберите тип расклада:", reply_markup=spread_menu)
    else:
        await message.answer("❗ У вас не осталось доступных раскладов. Пополните баланс.", reply_markup=pay_button)

# Обработчик кнопки оплаты
@router.message(F.text == "💳 Получить 10 раскладов за 99 рублей")
async def pay_spreads(message: types.Message):
    user_id = message.from_user.id
    await message.answer("🔗 Ссылка на оплату: https://example.com/test-payment")
    await message.answer("✅ Оплата прошла успешно! У вас теперь 10 новых раскладов.", reply_markup=create_start_menu(user_id))
    user_data[user_id]['paid_spreads'] += 10

# Обработчик выбора типа расклада
@router.message(F.text.in_({"💫 Три карты", "🔮 Кельтский крест", "💖 Отношения"}))
async def choose_spread(message: types.Message):
    spread_name = message.text
    await message.answer("Сформулируйте ваш вопрос для Таро:", reply_markup=ReplyKeyboardRemove())

    @router.message()
    async def get_question(user_message: types.Message):
        await message.answer(f"Вопрос получен: {user_message.text}\nНачинаем расклад '{spread_name}'.")

        # Генерация карт
        card_count = 3 if spread_name != "🔮 Кельтский крест" else 10
        selected_cards = random.sample(list(CARDS.items()), card_count)
        for card_image, card_name in selected_cards:
            await message.answer_photo(photo=card_image, caption=card_name)

        await message.answer("Ваш расклад завершён. Вы можете сделать новый расклад или вернуться в главное меню.", await message.answer("Выберите тип расклада:", reply_markup=spread_menu))

# Обработчик кнопки "🔄 Новый расклад"
@router.message(F.text == "🔄 Новый расклад")
async def new_spread(message: types.Message):
    user_id = message.from_user.id
    balance = user_data.get(user_id, {}).get('paid_spreads', 0)

    # Проверка бесплатного расклада
    if not user_data[user_id]['free_today']:
        balance += 1  # Бесплатный расклад учитывается до использования

    if balance > 0:
        if not user_data[user_id]['free_today']:
            user_data[user_id]['free_today'] = True  # Используем бесплатный
        else:
            user_data[user_id]['paid_spreads'] -= 1  # Уменьшаем платный баланс
        await message.answer("Выберите тип расклада:", reply_markup=spread_menu)
    else:
        await message.answer("❗ У вас не осталось доступных раскладов. Пополните баланс.", reply_markup=pay_button)


# Обработчик кнопки "🏠 Главное меню"
@router.message(F.text == "🏠 Главное меню")
async def main_menu(message: types.Message):
    user_id = message.from_user.id
    await message.answer("Добро пожаловать в главное меню! Выберите действие:", reply_markup=create_start_menu(user_id))

# Главный метод для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
