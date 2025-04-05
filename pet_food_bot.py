import telebot
from telebot import types
import sqlite3

BOT_TOKEN = '7759602453:AAFeBxtc0VRTBzTjplpcbg7Dm-oAvkZuqws'
bot = telebot.TeleBot(BOT_TOKEN)

# Словник для зберігання кошиків: {telegram_id: [список product_id]}
cart = {}

# Словник для зв'язку product_id з назвами товарів
PRODUCT_NAMES = {
    'add_rc_cat1': 'Royal Canin Sterilised (Кот)',
    'add_rc_cat2': 'Royal Canin Gastro Intestinal (Кот)',
    'add_rc_cat3': 'Royal Canin British Shorthair Adult (Кот)',
    'add_pp_cat1': 'Purina Pro Plan Sterilised (Кот)',
    'add_pp_cat2': 'Purina Pro Plan Adult 1+ Derma Care (Кот)',
    'add_pp_cat3': 'Purina Pro Plan Delicate Lamb (Кот)',
    'add_o_cat1': 'Optimeal - індичка та овес (Кот)',
    'add_o_cat2': 'Optimeal Adult Cat Sterilised (Кот)',
    'add_o_cat3': 'Optimeal - яловичина та сорго (Кот)',
    'add_rc_dog1': 'Royal Canin Gastro Intestinal (Собака)',
    'add_rc_dog2': 'Royal Canin Maxi Adult (Собака)',
    'add_rc_dog3': 'Royal Canin Medium Adult (Собака)',
    'add_pp_dog1': 'Purina Pro Plan Puppy Small & Mini (Собака)',
    'add_pp_dog2': 'Purina Pro Plan Adult Medium (Собака)',
    'add_pp_dog3': 'Purina Pro Plan Medium Sensitive Skin (Собака)',
    'add_o_dog1': 'Optimeal для дорослих собак великих порід (Собака)',
    'add_o_dog2': 'Optimeal для цуценят всіх порід (Собака)',
    'add_o_dog3': 'Optimeal гіпоалергенний (Собака)',
    
}

def create_connection():
    conn = sqlite3.connect('pet_food_bot.db', check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor

def close_connection(conn, cursor):
    cursor.close()
    conn.close()

# Функція для додавання користувача в базу даних та отримання його ID
def add_user(telegram_id):
    conn, cursor = create_connection()
    user_id = None
    try:
        cursor.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (telegram_id,))
        conn.commit()
        cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
        result = cursor.fetchone()
        if result:
            user_id = result[0]
    finally:
        close_connection(conn, cursor)
    return user_id

# /start
@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.from_user.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_cats = types.KeyboardButton('Корм для котів 🐈')
    btn_dogs = types.KeyboardButton('Корм для собак 🐕')
    btn_cart = types.KeyboardButton('Переглянути кошик')
    btn_order = types.KeyboardButton('Оформити замовлення')
    markup.add(btn_cats, btn_dogs)
    markup.add(btn_cart, btn_order)
    bot.send_message(message.chat.id, f"Вітаю, {message.from_user.first_name}! 👋\nЯ бот для замовлення корму для ваших улюбленців.\nОберіть, для якої тваринки шукаєте корм:", reply_markup=markup)

# категорія Корм для котів
@bot.message_handler(func=lambda message: message.text == 'Корм для котів 🐈')
def show_cat_brands(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_royal_canin_cats = types.KeyboardButton('Royal Canin (Cats)')
    btn_purina_cats = types.KeyboardButton('Purina Pro Plan (Cats)')
    btn_optiMeal_cats = types.KeyboardButton("OptiMeal (Cats)")
    btn_back = types.KeyboardButton('⬅️ Назад')
    markup.add(btn_royal_canin_cats, btn_purina_cats, btn_optiMeal_cats)
    markup.add(btn_back)
    bot.send_message(message.chat.id, "Оберіть бренд:", reply_markup=markup)

# Royal Canin (для котів)
@bot.message_handler(func=lambda message: message.text == 'Royal Canin (Cats)')
def show_royal_canin_cats(message):
    markup_rc_cat1 = types.InlineKeyboardMarkup()
    btn_add_rc_cat1 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_rc_cat1')
    markup_rc_cat1.add(btn_add_rc_cat1)
    bot.send_message(message.chat.id, "<b>Royal Canin (Для котів)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/3/700x700l80mc0/sukhiy-korm-dlya-kotiv-royal-canin-sterilised-37-400-g-82438080816065.webp'> Сухий корм для котів Royal Canin Sterilised </a> 🐾\n",
                                    parse_mode='html', reply_markup=markup_rc_cat1)

    markup_rc_cat2 = types.InlineKeyboardMarkup()
    btn_add_rc_cat2 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_rc_cat2')
    markup_rc_cat2.add(btn_add_rc_cat2)
    bot.send_message(message.chat.id, "<b>Royal Canin (Для котів)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/25/700x700l80mc0/sukhoy-korm-dlya-koshek-pri-zabolevaniyakh-zheludochno-kishechnogo-trakta-royal-canin-gastro-intestinal-2-kg-domashnyaya-ptitsa-51737914164841.webp'>Сухий корм для котів Royal Canin Gastro Intestinal</a> 🐾\n",
                                        parse_mode='html', reply_markup=markup_rc_cat2)

    markup_rc_cat3 = types.InlineKeyboardMarkup()
    btn_add_rc_cat3 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_rc_cat3')
    markup_rc_cat3.add(btn_add_rc_cat3)
    bot.send_message(message.chat.id, "<b>Royal Canin (Для котів)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/46/700x700l80mc0/sukhiy-korm-dlya-kotiv-royal-canin-british-shorthair-adult-400-g-domashnya-ptitsya-12473590661405.webp'>Сухий корм для котів породи британська короткошерста Royal Canin British Shorthair Adult</a> 🐾\n",
                                       parse_mode='html', reply_markup=markup_rc_cat3)

# Purina Pro Plan (для котів)
@bot.message_handler(func=lambda message: message.text == 'Purina Pro Plan (Cats)')
def show_purina_cats(message):
    markup_pp_cat1 = types.InlineKeyboardMarkup()
    btn_add_pp_cat1 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_pp_cat1')
    markup_pp_cat1.add(btn_add_pp_cat1)
    bot.send_message(message.chat.id, "<b>Purina Pro Plan (Для котів)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/16/700x700l80mc0/sukhoy-korm-dlya-pozhilykh-sterilizovannykh-koshek-pro-plan-sterilised-7-15-kg-indeyka-26858866681636.webp'>Сухий корм для котів Pro Plan Sterilised</a> 🐾\n",
                                      parse_mode='html', reply_markup=markup_pp_cat1)

    markup_pp_cat2 = types.InlineKeyboardMarkup()
    btn_add_pp_cat2 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_pp_cat2')
    markup_pp_cat2.add(btn_add_pp_cat2)
    bot.send_message(message.chat.id, "<b>Purina Pro Plan (Для котів)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/17/700x700l80mc0/sukhiy-korm-dlya-kotiv-sherst-yakikh-vimagaie-dodatkovogo-doglyadu-pro-plan-elegant-adult-salmon-400-g-losos-78256025396486.webp'>Сухий корм для котів Pro Plan Adult 1+ Derma Care</a> 🐾\n",
                                      parse_mode='html', reply_markup=markup_pp_cat2)

    markup_pp_cat3 = types.InlineKeyboardMarkup()
    btn_add_pp_cat3 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_pp_cat3')
    markup_pp_cat3.add(btn_add_pp_cat3)
    bot.send_message(message.chat.id, "<b>Purina Pro Plan (Для котів)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/21/700x700l80mc0/sukhoy-korm-dlya-koshek-s-chuvstvitelnym-pishchevareniem-pro-plan-delicate-15-kg-yagnenok-80842266147037.webp'>Сухий корм для котів з чутливим травленням Pro Plan Delicate Lamb</a> 🐾\n",
                                      parse_mode='html', reply_markup=markup_pp_cat3)

# OptiMeal (для котів)
@bot.message_handler(func=lambda message: message.text == "OptiMeal (Cats)")
def show_optimeal_cats(message):
    markup_o_cat1 = types.InlineKeyboardMarkup()
    btn_add_o_cat1 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_o_cat1')
    markup_o_cat1.add(btn_add_o_cat1)
    bot.send_message(message.chat.id, "<b>OptiMeal (Для котів)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/12/700x700l80mc0/suxoy-korm-dlja-sterilizovannyx-koshek-i-kastrirovannyx-kotov-optimeal-4-kg-indeyka-i-oves-99089663354128.webp'>Сухий корм для стерилізованих котів Optimeal - індичка та овес</a> 🐾\n",
                                      parse_mode='html', reply_markup=markup_o_cat1)

    markup_o_cat2 = types.InlineKeyboardMarkup()
    btn_add_o_cat2 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_o_cat2')
    markup_o_cat2.add(btn_add_o_cat2)
    bot.send_message(message.chat.id, "<b>OptiMeal (Для котів)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/29/700x700l80mc0/sukhiy-korm-dlya-kotiv-optimeal-adult-cat-sterilised-10-kg-losos-66662956320268.webp'>Сухий корм для котів Optimeal Adult Cat Sterilised</a> 🐾\n",
                                      parse_mode='html', reply_markup=markup_o_cat2)

    markup_o_cat3 = types.InlineKeyboardMarkup()
    btn_add_o_cat3 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_o_cat3')
    markup_o_cat3.add(btn_add_o_cat3)
    bot.send_message(message.chat.id, "<b>OptiMeal (Для котів)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/28/700x700l80mc0/sukhiy-korm-dlya-sterilizovanikh-kishok-optimeal-4-kg-yalovichina-ta-sorgo-49290621672250.webp'>Сухий корм для стерилізованих кішок Optimeal</a> 🐾\n",
                                      parse_mode='html', reply_markup=markup_o_cat3)

# категорія Корм для собак
@bot.message_handler(func=lambda message: message.text == 'Корм для собак 🐕')
def show_dog_brands(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_royal_canin_dogs = types.KeyboardButton('Royal Canin (Dogs)')
    btn_purina_dogs = types.KeyboardButton('Purina Pro Plan (Dogs)')
    btn_optimeal_dogs = types.KeyboardButton('OptiMeal (Dogs)')
    btn_back = types.KeyboardButton('⬅️ Назад')
    markup.add(btn_royal_canin_dogs, btn_purina_dogs, btn_optimeal_dogs)
    markup.add(btn_back)
    bot.send_message(message.chat.id, "Оберіть бренд:", reply_markup=markup)

# Royal Canin (для собак)
@bot.message_handler(func=lambda message: message.text == 'Royal Canin (Dogs)')
def show_royal_canin_dogs(message):
    markup_rc_dog1 = types.InlineKeyboardMarkup()
    btn_add_rc_dog1 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_rc_dog1')
    markup_rc_dog1.add(btn_add_rc_dog1)
    bot.send_message(message.chat.id, "<b>Royal Canin (Для собак)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/35/700x700l80mc0/sukhoy-korm-dlya-sobak-pri-zabolevaniyakh-zheludochno-kishechnogo-trakta-royal-canin-gastro-intestinal-2-kg-domashnyaya-ptitsa-28809777287282.webp'>Сухий корм для собак Royal Canin Gastro Intestinal</a> 🐾\n",
                                    parse_mode='html', reply_markup=markup_rc_dog1)

    markup_rc_dog2 = types.InlineKeyboardMarkup()
    btn_add_rc_dog2 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_rc_dog2')
    markup_rc_dog2.add(btn_add_rc_dog2)
    bot.send_message(message.chat.id, "<b>Royal Canin (Для собак)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/5/700x700l80mc0/sukhiy-korm-dlya-sobak-royal-canin-maxi-adult-4-kg-domashnya-ptitsya-75694807835381.webp'>Сухий корм для собак Royal Canin Maxi Adult</a> 🐾\n",
                                      parse_mode='html', reply_markup=markup_rc_dog2)

    markup_rc_dog3 = types.InlineKeyboardMarkup()
    btn_add_rc_dog3 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_rc_dog3')
    markup_rc_dog3.add(btn_add_rc_dog3)
    bot.send_message(message.chat.id, "<b>Royal Canin (Для собак)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/6/700x700l80mc0/suxoy-korm-dlja-sobak-royal-canin-medium-adult-4-kg--domashnjaja-ptica-44350272952965.webp'>Сухий корм для собак Royal Canin Medium Adult</a> 🐾\n",
                                      parse_mode='html', reply_markup=markup_rc_dog3)

# Purina Pro Plan (для собак)
@bot.message_handler(func=lambda message: message.text == 'Purina Pro Plan (Dogs)')
def show_purina_dogs(message):
    markup_pp_dog1 = types.InlineKeyboardMarkup()
    btn_add_pp_dog1 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_pp_dog1')
    markup_pp_dog1.add(btn_add_pp_dog1)
    bot.send_message(message.chat.id, "<b>Purina Pro Plan (Для собак)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/20/700x700l80mc0/suxoy-korm-dlja-shenkov-malyx-porod-pro-plan-small-and-mini-puppy-7-kg-kurica-76286800680992.webp'>Сухий корм для цуценят та молодих собак Pro Plan Puppy Small & Mini</a> 🐾\n",
                                      parse_mode='html', reply_markup=markup_pp_dog1)

    markup_pp_dog2 = types.InlineKeyboardMarkup()
    btn_add_pp_dog2 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_pp_dog2')
    markup_pp_dog2.add(btn_add_pp_dog2)
    bot.send_message(message.chat.id, "<b>Purina Pro Plan (Для собак)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/7/700x700l80mc0/suxoy-korm-dlja-vzroslyx-sobak-srednix-porod-pro-plan-adult-medium-3-kg-kurica-41260792839959.webp'>Сухий корм для собак Pro Plan Adult Medium</a> 🐾\n",
                                      parse_mode='html', reply_markup=markup_pp_dog2)

    markup_pp_dog3 = types.InlineKeyboardMarkup()
    btn_add_pp_dog3 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_pp_dog3')
    markup_pp_dog3.add(btn_add_pp_dog3)
    bot.send_message(message.chat.id, "<b>Purina Pro Plan (Для собак)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/44/700x700l80mc0/sukhiy-korm-dlya-doroslikh-sobak-serednikh-porid-proplan-medium-sensitive-skin-14-kg-losos-36895003515746.webp'>Сухий корм для собак ProPlan Medium Sensitive Skin</a> 🐾\n",
                                      parse_mode='html', reply_markup=markup_pp_dog3)

# OptiMeal (для собак)
@bot.message_handler(func=lambda message: message.text == 'OptiMeal (Dogs)')
def show_optimeal_dogs(message):
    markup_o_dog1 = types.InlineKeyboardMarkup()
    btn_add_o_dog1 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_o_dog1')
    markup_o_dog1.add(btn_add_o_dog1)
    bot.send_message(message.chat.id, "<b>OptiMeal (Для собак)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/35/700x700l80mc0/sukhiy-korm-dlya-doroslikh-sobak-velikikh-porid-optimeal-15-kg-indichka-97878546311428.webp'>Сухий корм для дорослих собак великих порід Optimeal</a> 🐾\n",
                                      parse_mode='html', reply_markup=markup_o_dog1)

    markup_o_dog2 = types.InlineKeyboardMarkup()
    btn_add_o_dog2 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_o_dog2')
    markup_o_dog2.add(btn_add_o_dog2)
    bot.send_message(message.chat.id, "<b>OptiMeal (Для собак)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/38/700x700l80mc0/suxoy-polnoracionnyy-korm-dlja-shenkov-vsex-porod-optimeal-15-kg-indeyka-92115270126012.webp'>Сухий повнораціонний корм для цуценят всіх порід Optimeal </a> 🐾\n",
                                      parse_mode='html', reply_markup=markup_o_dog2)

    markup_o_dog3 = types.InlineKeyboardMarkup()
    btn_add_o_dog3 = types.InlineKeyboardButton("Додати до кошика", callback_data='add_o_dog3')
    markup_o_dog3.add(btn_add_o_dog3)
    bot.send_message(message.chat.id, "<b>OptiMeal (Для собак)</b>\n\n"
                                      "<a href='https://masterzoo.ua/content/images/36/700x700l80mc0/sukhiy-gipoalergenniy-korm-optimeal-dlya-doroslikh-sobak-serednikh-ta-velikikh-porid-4-kg-losos-30916144363031.webp'>Сухий гіпоалергенний корм Optimeal для дорослих собак середніх та великих порід</a> 🐾\n",
                                      parse_mode='html', reply_markup=markup_o_dog3)

# Назад
@bot.message_handler(func=lambda message: message.text == '⬅️ Назад')
def back_to_main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_cats = types.KeyboardButton('Корм для котів 🐈')
    btn_dogs = types.KeyboardButton('Корм для собак 🐕')
    btn_cart = types.KeyboardButton('Переглянути кошик')
    btn_order = types.KeyboardButton('Оформити замовлення')
    markup.add(btn_cats, btn_dogs)
    markup.add(btn_cart, btn_order)
    bot.send_message(message.chat.id, "Оберіть дію:", reply_markup=markup)

# Перегляд кошика
@bot.message_handler(func=lambda message: message.text == 'Переглянути кошик')
def show_cart(message):
    user_id = message.from_user.id
    if user_id in cart and cart[user_id]:
        cart_items = cart[user_id]
        cart_text = "<b>Ваш кошик:</b>\n"
        item_counts = {}
        for item_id in cart_items:
            item_counts[item_id] = item_counts.get(item_id, 0) + 1

        for item_id, quantity in item_counts.items():
            product_name = PRODUCT_NAMES.get(item_id, "Невідомий товар")
            cart_text += f"- {product_name} (Кількість: {quantity})\n"

        bot.send_message(message.chat.id, cart_text, parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Ваш кошик порожній.")

# Оформлення замовлення
@bot.message_handler(func=lambda message: message.text == 'Оформити замовлення')
def process_order(message):
    user_id = message.from_user.id
    if user_id in cart and cart[user_id]:
        bot.send_message(message.chat.id, "Будь ласка, введіть ваш номер телефону для зв'язку:")
        bot.register_next_step_handler(message, get_phone_number)
    else:
        bot.send_message(message.chat.id, "Ваш кошик порожній. Неможливо оформити замовлення.")

def get_phone_number(message):
    phone_number = message.text
    user_id = message.from_user.id
    cart_items = cart.get(user_id, [])
    order_details = "\n".join([PRODUCT_NAMES.get(item_id, "Невідомий товар") for item_id in cart_items])

    bot.send_message(message.chat.id,
                     f"Дякуємо! Ваш номер телефону: {phone_number}.\nВаше замовлення:\n{order_details}\n\nЯкщо у вас є якісь побажання до замовлення, введіть їх зараз, або натисніть 'Підтвердити замовлення'.",
                     reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                         types.KeyboardButton('Підтвердити замовлення')))
    bot.register_next_step_handler(message, confirm_order, phone_number, cart_items)

def confirm_order(message, phone_number, cart_items):
    if message.text == 'Підтвердити замовлення':
        cart.clear()
        ordered_items = "\n".join([PRODUCT_NAMES.get(item_id, "Невідомий товар") for item_id in cart_items])
        bot.send_message(message.chat.id,
                         f"Ваше замовлення прийнято. Ми зателефонуємо вам найближчим часом для підтвердження.\nНомер телефону: {phone_number}.\nЗамовлені товари:\n{ordered_items}",
                         reply_markup=types.ReplyKeyboardRemove())
    else:
        cart.clear()
        ordered_items = "\n".join([PRODUCT_NAMES.get(item_id, "Невідомий товар") for item_id in cart_items])
        bot.send_message(message.chat.id,
                         f"Ваше повідомлення до замовлення: {message.text}.\nЗамовлення прийнято. Ми зателефонуємо вам найближчим часом для підтвердження.\nНомер телефону: {phone_number}.\nЗамовлені товари:\n{ordered_items}",
                         reply_markup=types.ReplyKeyboardRemove())

# Додати до кошика
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
def add_to_cart(call):
    user_id = call.from_user.id
    product_id = call.data

    if user_id not in cart:
        cart[user_id] = []

    cart[user_id].append(product_id)

    product_name = PRODUCT_NAMES.get(product_id, "Невідомий товар")
    bot.answer_callback_query(call.id, f"Товар '{product_name}' додано до кошика!")
    bot.send_message(call.message.chat.id, f"Товар '{product_name}' додано до кошика.\nЩоб переглянути кошик, натисніть кнопку 'Переглянути кошик'.")

if __name__ == '__main__':
    # Створення таблиці користувачів при запуску
    conn, cursor = create_connection()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE
                )
            ''')
    # Створення таблиці кошика при запуску
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id TEXT, -- Унікальний ідентифікатор товару (наприклад, 'rc_cat1')
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    close_connection(conn, cursor)

    bot.polling(none_stop=True)