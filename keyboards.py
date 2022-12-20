from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


order = "Замовити"
back = "Назад"
main_menu = "Головне меню"

# admin menu
mailing = "Розсилка 📨"
who_came = "Хто заходив 🕺"
user_menu = "Меню покупця 👤"

# user menu
catalog = "Каталог товарів  🗂"
contacts = "Контакти  📍"
message = "Зв'язатись з нами"
recipes = "Рецепти  📚"

# user_cabinet
user_cart = "Корзина"
user_history = "Історія замовлень"


kb_main_back = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu = KeyboardButton(main_menu)
back = KeyboardButton(back)
kb_main_back.add(main_menu).add(back)

# main admin menu
kb_admin_main = ReplyKeyboardMarkup(resize_keyboard=True)
mailing = KeyboardButton(mailing)
who_came = KeyboardButton(who_came)
user_menu = KeyboardButton(user_menu)
kb_admin_main.add(who_came, mailing).add(user_menu)

# main user menu
kb_user_main = ReplyKeyboardMarkup(resize_keyboard=True)
bum1 = KeyboardButton(catalog)
bum2 = KeyboardButton(contacts)
bum3 = KeyboardButton(recipes)
kb_user_main.add(bum1).add(bum2, bum3)

# user_cabinet
kb_user_cabinet = ReplyKeyboardMarkup(resize_keyboard=True)
buc1 = KeyboardButton(user_cart)
buc2 = KeyboardButton(user_history)
kb_user_cabinet.add(buc1).add(buc2, back)

# user_cart
kb_user_cart = ReplyKeyboardMarkup(resize_keyboard=True)
bcc1 = KeyboardButton(user_cart)
bcc2 = KeyboardButton(user_history)
kb_user_cart.add(bcc1).add(bcc2, back)

# user_history
kb_user_history = ReplyKeyboardMarkup(resize_keyboard=True)
buh1 = KeyboardButton(user_cart)
buh2 = KeyboardButton(user_history)
kb_user_history.add(buh1).add(buh2, back)

# recipes
pizza = 'Піца  🍕'
paste = 'Паста  🍝'
salads = 'Салати  🥗'
desserts = 'Десерти  🍰'
meat_dishes = "М'ясні страви  🍖"

# recipes
kb_user_recipes = InlineKeyboardMarkup(resize_keyboard=True)
ibr1 = InlineKeyboardButton(pizza, url='https://bonta.com.ua/ua/cp97840-pitstsa.html')
ibr2 = InlineKeyboardButton(paste, url='https://bonta.com.ua/ua/cp97857-pasta.html')
ibr3 = InlineKeyboardButton(salads, url='https://bonta.com.ua/ua/cp97870-salaty.html')
ibr4 = InlineKeyboardButton(desserts, url='https://bonta.com.ua/ua/cp97871-deserty.html')
ibr5 = InlineKeyboardButton(meat_dishes, url='https://bonta.com.ua/ua/cp97929-myasnye-blyuda-.html')
kb_user_recipes.add(ibr1).add(ibr2).add(ibr3).add(ibr4).add(ibr5)

# user_catalog
sauces = "Соуси"
pasta_and_risotto = "Паста та Різотто"
groceries_and_condiments = "Бакалія та приправи"
flour = "Борошно"
olives = "Оливки"
olive_oil = "Оливкова олія"
canned_food = "Консерви"
sweet = "Солодощі"
novelty = "Новинки"
ready_sets = "Готові набори"
gift_sets = "Подарункові набори 🎁"

# user_catalog
ikb_user_catalog = InlineKeyboardMarkup(resize_keyboard=True)
ibc1 = InlineKeyboardButton(sauces, callback_data='sauces')
ibc2 = InlineKeyboardButton(pasta_and_risotto, callback_data='pasta_and_risotto')
ibc3 = InlineKeyboardButton(groceries_and_condiments, callback_data='groceries_and_condiments')
ibc4 = InlineKeyboardButton(flour, callback_data='flour')
ibc5 = InlineKeyboardButton(olives, callback_data='olives')
ibc6 = InlineKeyboardButton(olive_oil, callback_data='olive_oil')
ibc7 = InlineKeyboardButton(canned_food, callback_data='canned_food')
ibc8 = InlineKeyboardButton(sweet, callback_data='sweet')
ibc9 = InlineKeyboardButton(novelty, callback_data='novelty')
ibc10 = InlineKeyboardButton(ready_sets, callback_data='ready_sets')
ibc11 = InlineKeyboardButton(gift_sets, callback_data='gift_sets')
ikb_user_catalog.add(ibc1).add(ibc2).add(ibc3).add(ibc4).add(ibc5).add(ibc6) \
                .add(ibc7).add(ibc8).add(ibc9).add(ibc10).add(ibc11)

recipes_info = """<b>Італійська кухня</b> – одна з найулюбленіших у світі. І не дарма. 
Її відрізняє не лише вишуканість та смак страв, а й душевність. 
Для будь-якого італійця кожен прийом їжі - це не необхідність, це справжнє задоволення. 
Обід, вечеря чи сніданок – не важливо. 
Кожну трапезу італійці розтягують, прагнуть провести її в хорошій компанії або прикрашають келихом смачного вина. 
Вони нікуди не поспішають. Вони дозволяють відчути собі кожен шматочок їжі, відчути кожен відтінок смаку. 
Адже їжа – це мистецтво. І в італійців дійсно потрібно повчитися любити кожен її прояв. 
Ми зібрали для вас найкращі перевірені рецепти страв італійської кухні, які припадуть до смаку ..."""