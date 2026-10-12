import asyncio
import html
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ----------------- НАСТРОЙКИ -----------------
TOKEN = "8888751440:AAECngYJydYR77jLmtBFueSskqTeGOWTQMk"
ADMIN_ID = 5812615195
# ---------------------------------------------

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Машина состояний для формы заказа
class OrderForm(StatesGroup):
    server = State()
    rank = State()
    task = State()
    deadline = State()

# Главное меню
def main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton(text="📋 Прайс-лист", callback_data="price")],
        [InlineKeyboardButton(text="📝 Оформить заказ", callback_data="start_order")],
        [InlineKeyboardButton(text="🛡 Гарантии и безопасность", callback_data="guarantees")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Меню категорий прайса
def price_keyboard():
    buttons = [
        [InlineKeyboardButton(text="🗺 Карта и квесты", callback_data="price_map")],
        [InlineKeyboardButton(text="⚔️ Бездна и Театр", callback_data="price_abyss")],
        [InlineKeyboardButton(text="⏳ Дейлики и смола", callback_data="price_daily")],
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Обработчик /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    text = (
        "Привет, путешественник! ✨\n"
        "Добро пожаловать в <b>Лавку Наганохары</b>.\n\n"
        "Здесь ты можешь заказать ручную прокачку и закрытие контента в Genshin Impact:\n"
        "• Закрытие карты, сбор сундуков и окулусов\n"
        "• Витая Бездна и Театр Воображариума\n"
        "• Ежедневный уход за аккаунтом и слив смолы\n\n"
        "Работаем строго без модов и стороннего софта. 🎯\n"
        "Выбери нужный раздел ниже:"
    )
    await message.answer(text, reply_markup=main_menu_keyboard(), parse_mode="HTML")

# Кнопка возврата в меню
@dp.callback_query(F.data == "back_main")
async def back_to_main(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Главное меню Лавки Наганохары:",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()

# Раздел "Прайс-лист"
@dp.callback_query(F.data == "price")
@dp.message(Command("price"))
async def show_price(event: types.Message | types.CallbackQuery):
    text = "📋 Выбери категорию услуг:"
    markup = price_keyboard()
    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(text, reply_markup=markup)
        await event.answer()
    else:
        await event.answer(text, reply_markup=markup)

@dp.callback_query(F.data == "price_map")
async def price_map(callback: types.CallbackQuery):
    text = (
        "🗺 <b>Карта и исследование:</b>\n\n"
        "• Сбор всех окулусов региона: от 400 ₽\n"
        "• Зачистка зоны на 100% (все сундуки/загадки): от 500 ₽\n"
        "• Длинные цепочки квестов (Араньяка и т.д.): от 600 ₽\n"
        "• Фарм диковинок персонажа (168 шт.): 250 ₽"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Заказать зачистку", callback_data="start_order")],
        [InlineKeyboardButton(text="⬅️ Назад к прайсу", callback_data="price")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "price_abyss")
async def price_abyss(callback: types.CallbackQuery):
    text = (
        "⚔️ <b>Боевой контент:</b>\n\n"
        "• Витая Бездна (9-12 этажи, 36★): от 350 ₽\n"
        "• Только 12 этаж (9★): 250 ₽\n"
        "• Театр Воображариума (макс. уровень): от 300 ₽"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Заказать Бездну", callback_data="start_order")],
        [InlineKeyboardButton(text="⬅️ Назад к прайсу", callback_data="price")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "price_daily")
async def price_daily(callback: types.CallbackQuery):
    text = (
        "⏳ <b>Ежедневное обслуживание:</b>\n\n"
        "• Неделя: Дейлики + слив всей смолы: 350 ₽\n"
        "• Месяц: Полный фарм смолы + дейлики: 1200 ₽\n"
        "• Главный ивент патча целиком: 300–500 ₽"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Оформить саппорт", callback_data="start_order")],
        [InlineKeyboardButton(text="⬅️ Назад к прайсу", callback_data="price")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()

# Раздел "Гарантии"
@dp.callback_query(F.data == "guarantees")
@dp.message(Command("guarantees"))
async def show_guarantees(event: types.Message | types.CallbackQuery):
    text = (
        "🛡 <b>Гарантии и безопасность:</b>\n\n"
        "1. <b>Без читов и стороннего ПО:</b> Заходим строго через официальный клиент игры.\n"
        "2. <b>2FA защита:</b> Доступ к почте отдавать не нужно! Вход только по коду подтверждения.\n"
        "3. <b>Ресурсы в сохранности:</b> Примогемы, крутки и артефакты не трогаются без вашего ведома.\n"
        "4. <b>Отчеты:</b> Фиксируем скриншотами состояние аккаунта до и после работы."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="back_main")]
    ])
    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        await event.answer()
    else:
        await event.answer(text, reply_markup=keyboard, parse_mode="HTML")

# ----------------- СЦЕНАРИЙ ЗАКАЗА (FSM) -----------------

@dp.callback_query(F.data == "start_order")
@dp.message(Command("order"))
async def order_start(event: types.Message | types.CallbackQuery, state: FSMContext):
    await state.set_state(OrderForm.server)
    prompt = "Шаг 1/4: На каком сервере ты играешь? (Европа, Азия, Америка)"
    if isinstance(event, types.CallbackQuery):
        await event.message.answer(prompt)
        await event.answer()
    else:
        await event.answer(prompt)

@dp.message(OrderForm.server)
async def process_server(message: types.Message, state: FSMContext):
    await state.update_data(server=message.text)
    await state.set_state(OrderForm.rank)
    await message.answer("Шаг 2/4: Какой ранг приключений (AR) на твоем аккаунте?")

@dp.message(OrderForm.rank)
async def process_rank(message: types.Message, state: FSMContext):
    await state.update_data(rank=message.text)
    await state.set_state(OrderForm.task)
    await message.answer("Шаг 3/4: Опиши задачу подробно (например: закрыть Натлан на 100%):")

@dp.message(OrderForm.task)
async def process_task(message: types.Message, state: FSMContext):
    await state.update_data(task=message.text)
    await state.set_state(OrderForm.deadline)
    await message.answer("Шаг 4/4: До какого числа или времени нужно успеть выполнить?")

@dp.message(OrderForm.deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    await state.update_data(deadline=message.text)
    data = await state.get_data()
    await state.clear()

    # Сообщение клиенту
    await message.answer(
        "🎆 <b>Заявка принята!</b>\nМастер скоро свяжется с тобой в Telegram.",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )

    # Формируем и отправляем уведомление админу
    if ADMIN_ID != 0:
        if message.from_user.username:
            user_info = f"@{message.from_user.username} (ID: {message.from_user.id})"
        else:
            full_name = html.escape(message.from_user.full_name or "Без имени")
            user_info = f"ID: {message.from_user.id} ({full_name})"

        admin_alert = (
            "🔔 <b>НОВЫЙ ЗАКАЗ В ЛАВКЕ!</b>\n\n"
            f"👤 <b>Клиент:</b> {user_info}\n"
            f"🌐 <b>Сервер:</b> {html.escape(str(data.get('server')))}\n"
            f"🎖 <b>Ранг:</b> {html.escape(str(data.get('rank')))}\n"
            f"📌 <b>Задача:</b> {html.escape(str(data.get('task')))}\n"
            f"⏰ <b>Дедлайн:</b> {html.escape(str(data.get('deadline')))}"
        )
        try:
            await bot.send_message(chat_id=ADMIN_ID, text=admin_alert, parse_mode="HTML")
            print(f">>> Заказ успешно отправлен админу {ADMIN_ID} <<<")
        except Exception as e:
            print(f"!!! ОШИБКА ОТПРАВКИ АДМИНУ: {e} !!!")

# ----------------- ТОЧКА ВХОДА -----------------
async def main():
    print(">>> Инициализация бота... <<<")
    # Сбрасываем старые апдейты, чтобы убрать конфликты
    await bot.delete_webhook(drop_pending_updates=True)
    print(">>> БОТ УСПЕШНО ЗАПУЩЕН И ГОТОВ К РАБОТЕ <<<")
    
    # Отправляем тестовое сообщение админу прямо при старте!
    if ADMIN_ID != 0:
        try:
            await bot.send_message(chat_id=ADMIN_ID, text="🚀 <b>Бот успешно запущен на хостинге!</b>", parse_mode="HTML")
            print(f">>> Тестовое сообщение отправлено админу {ADMIN_ID} <<<")
        except Exception as e:
            print(f"!!! ОШИБКА СТАРТОВОГО СООБЩЕНИЯ АДМИНУ: {e} !!!")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print(">>> Бот остановлен <<<")

if __name__ == "__main__":
    asyncio.run(main())
