# -*- coding: utf8 -*-
# GIT UPDATE
import logging
#import dbworker
#import config
import os.path
from sqlite_db_worker import *
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)


now = datetime.datetime.now()


storage = MemoryStorage()

bot = Bot(token="967548998:AAG_L68xhcsQtWbXRroeKpcKUHJQA__1_IE")
dp = Dispatcher(bot, storage=storage)



username_of_admin_channel = '@dev_test_channell_vova'





# Смайлы для текст дизайн бота
smile_with_2_love = u'\U0001F60D'
love = u'\U00012764'
podmiga = u'\U0001F609'

# Добавление меню с информацией о товаре
product_menu = types.InlineKeyboardMarkup()
buy_button = types.InlineKeyboardButton(text="(смайл) КУПИТЬ", callback_data='buy_button')
product_menu.add(buy_button)



#Добавление меню с покупкой товара ( выбор количества штук и использование купонов )
product_buy_meny = types.InlineKeyboardMarkup()
product_buy_now_button = types.InlineKeyboardButton(text="Купить товар ( Выбор количества здесь ) ", callback_data='product_buy_now_button')
#one_button = types.InlineKeyboardButton(text="1 шт", callback_data='one_button')
#five_button = types.InlineKeyboardButton(text="5 шт", callback_data='five_button')
#ten_button = types.InlineKeyboardButton(text="10 шт", callback_data='ten_button')
#tvelwe_button = types.InlineKeyboardButton(text="20 шт", callback_data='tvelwe_button')
#fifty_button = types.InlineKeyboardButton(text="50 шт", callback_data='fifty_button')
#one_hundred_button = types.InlineKeyboardButton(text="100 шт", callback_data='one_hundred_button')
use_coupone_button = types.InlineKeyboardButton(text="Использовать купон", callback_data='use_coupone_button')
#product_buy_meny.row(one_button,five_button,ten_button)
#product_buy_meny.row(tvelwe_button, fifty_button, one_hundred_button)
product_buy_meny.add(product_buy_now_button)
product_buy_meny.add(use_coupone_button)


# Добавление меню выбора оплаты
how_to_buy_menu = types.InlineKeyboardMarkup()
qiwi_buy_button = types.InlineKeyboardButton(text="Qiwi (Visa/MasterCard)", callback_data='qiwi_buy_button')
btc_buy_button = types.InlineKeyboardButton(text="BTC оплата", callback_data='btc_buy_button')
oplata_cheta_button = types.InlineKeyboardButton(text="Оплата личным балансом", callback_data='oplata_cheta_button')
how_to_buy_menu.add(qiwi_buy_button)
how_to_buy_menu.add(btc_buy_button)
how_to_buy_menu.add(oplata_cheta_button)





# Добавление меню пополнение баланса
moi_kabinet_menu = types.InlineKeyboardMarkup()
moi_pokupki = types.InlineKeyboardButton(text="Мои покупки ( смайл )", callback_data="moi_pokupki")
popolnit_balance = types.InlineKeyboardButton(text="Пополнить баланс ( смайл ) ", callback_data="popolnit_balance")
moi_kabinet_menu.add(moi_pokupki)
moi_kabinet_menu.add(popolnit_balance)



# Добавление главного меню бота
main_menu_buttons_update = get_names_of_buttons_main_menu()
main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
catalog_tovarov = types.KeyboardButton(text=str(main_menu_buttons_update[4]), callback_data="catalog_tovarov")
moi_kabinet = types.KeyboardButton(text=str(main_menu_buttons_update[5]), callback_data="moi_kabinet")
moi_pokupki = types.KeyboardButton(text=str(main_menu_buttons_update[6]), callback_data="moi_pokupki")
main_menu.row(catalog_tovarov,moi_kabinet,moi_pokupki)
main_menu_buttons = get_names_of_buttons_main_menu()
button1 = types.KeyboardButton(text=str(main_menu_buttons[0]), callback_data=str(main_menu_buttons[0]))
button2 = types.KeyboardButton(text=str(main_menu_buttons[1]), callback_data=str(main_menu_buttons[1]))
button3 = types.KeyboardButton(text=str(main_menu_buttons[2]), callback_data=str(main_menu_buttons[2]))
button4 = types.KeyboardButton(text=str(main_menu_buttons[3]), callback_data=str(main_menu_buttons[3]))
main_menu.row(button1, button2, button3)
main_menu.add(button4)

# Добавление меню с принудительным сообщением
prinud_menu = types.InlineKeyboardMarkup()
ok_button = types.InlineKeyboardButton(text="Принять условия", callback_data="ok_info")
prinud_menu.add(ok_button)

#Вытягиваем главное сообщение приветствия
hi_text = get_text_of_button_id(id=8)


# Создание уникальной реферальной ссылки пользователя
ref_link_user = "https://t.me/Gold_Games_bot?start="

# Создаём уникальный код, для человека в реферальной ссылке
def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None


# /test command
#@dp.message_handler(commands=["test"])
#async def testCommand(message: types.Message):



# /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
	if get_have_user_in_a_base(user_id=message.chat.id) == 1:
		test_text = str(get_text_of_button_id(id=8))
		if test_text.split().count('first_name'):
			print (test_text.split().count('first_name'))
			print (test_text.find('first_name'))
			l = len(test_text)
			index_of_first_name = int(test_text.find('first_name')) - 1
			test_text_part1 = test_text[0:index_of_first_name]
			print(test_text_part1)
			test_text_part2 = test_text[index_of_first_name+12:l]
			print(test_text_part2)
			await bot.send_message(message.chat.id, test_text_part1 + message.from_user.first_name + test_text_part2, reply_markup=main_menu)
		else:
			await bot.send_message(message.chat.id, str(get_text_of_button_id(id=8)), reply_markup=main_menu)
	else:
		await bot.send_message(message.chat.id, str(get_text_of_button_id(id=9)), reply_markup=prinud_menu)



# Обработка кнопок главного меню бота
@dp.message_handler(content_types=["text"])
async def main_menu_buttons(message: types.Message):

	# Обработка всех динамических кнопок
	buttons_menu_callback = get_names_of_buttons_main_menu()
	if buttons_menu_callback[4] == message.text:
		store_categories = get_full_list_categories_of_store()
		menu_categories = types.InlineKeyboardMarkup()
		for number in range(len(store_categories)):
			button = types.InlineKeyboardButton(text=str(store_categories[number]), callback_data=str(store_categories[number]))
			menu_categories.add(button)

		await bot.send_message(message.from_user.id, "Выберите категорию:", reply_markup=menu_categories)
	
	elif buttons_menu_callback[5] == message.text:
		await bot.send_message(message.from_user.id, "Баланс пользователя: " + str(get_balance_of_user(user_id=message.from_user.id)) + " рублей \n\nЗаработано по реферальной программе: 0 рублей \n\nЯ получаю 5% с продаж \n\nВсего рефералов: " + str(find_ref_curator_of_member(user_id=message.from_user.id)))
		global ref_link_user
		ref_link_user = ref_link_user + str(message.from_user.id)
		#Вывод реферальной ссылки
		await bot.send_message(message.from_user.id, "Ваша реферальная ссылка: \n " + ref_link_user, reply_markup=moi_kabinet_menu)
	else:
		for number in range(len(buttons_menu_callback)):
			if buttons_menu_callback[number] == message.text:
				await bot.send_message(message.from_user.id, get_text_of_button_id(id=int(number+1)))




# Функция вывода информации о товаре
async def info_product_out(user_choice_product_id):
	product_caption =	'Информация о товаре \n\nЦена: ' + str(get_name_tovara_price(name_tovara=str(user_choice_product_id))) + ' RUB' + '\n\nДоступное количество: ' + str(get_name_tovara_kolvo(name_tovara=str(user_choice_product_id))) + '\n\nДоставка: Моментальная\n\n' + str(get_name_tovara_description(name_tovara=str(user_choice_product_id)))
	return product_caption						


# Здесь прописано начало логики после выбора категории до отправки самого аккаунта
# Важно: Логика работает за счёт конечных автоматов и ничто это логику не должно прерывать
# Всю остальную логику не продаж прописать выше!
@dp.callback_query_handler(lambda call: True)
async def orderStepTwo(call):
	# Старт работы с ботом
	if str(call.data) == "ok_info":
		unique_code = extract_unique_code(call.data)
		print(unique_code)

		if extract_unique_code(call.data):

			splited = call.data.split()[1]
			print(splited)
			if user_id_in_base(user_id=int(splited)) == True:
				print('Я нашёл вашего реферала')
				if user_id_in_base(user_id=call.chat.id) == False:
					add_message_to_ref_user_base(user_id=call.chat.id, wallet=str(call.chat.id) + 'wallet',
																						curator=str(splited))
					add_curator_ref_member(find_user_id=splited)
					print('Я добавил вас как реферала')
				else:
					pass
			else:
				await bot.send_message(call.chat.id, "Вы пришли не по реферальной программе..")
			if user_id_in_base(user_id=call.chat.id) == False:
				add_message_to_ref_user_base(user_id=call.chat.id, wallet=str(call.chat.id) + 'wallet',
																							curator='Null')





	# Проверка зарегистрировался человек уже в боте или нет
		if get_have_user_in_a_base(user_id=call.from_user.id) == 0:
			add_new_wallet_to_base(user_id=call.from_user.id)
			add_new_user_to_base(user_id = call.from_user.id, username = call.from_user.username, date=str(now.day) + "." + str(now.month) + "." + str(now.year))
			test_text = str(get_text_of_button_id(id=8))
			if test_text.split().count('first_name'):
				print (test_text.split().count('first_name'))
				print (test_text.find('first_name'))
				l = len(test_text)
				index_of_first_name = int(test_text.find('first_name')) - 1
				test_text_part1 = test_text[0:index_of_first_name]
				print(test_text_part1)
				test_text_part2 = test_text[index_of_first_name+11:l]
				print(test_text_part2)
				await bot.send_message(call.from_user.id, test_text_part1 + call.from_user.first_name + test_text_part2, reply_markup=main_menu)
			else:
				await bot.send_message(call.from_user.id, str(get_text_of_button_id(id=8)), reply_markup=main_menu)
		else:
			print('User allready in a base')
			test_text = str(get_text_of_button_id(id=8))
			if test_text.split().count('first_name'):
				print (test_text.split().count('first_name'))
				print (test_text.find('first_name'))
				l = len(test_text)
				index_of_first_name = int(test_text.find('first_name')) - 1
				test_text_part1 = test_text[0:index_of_first_name]
				print(test_text_part1)
				test_text_part2 = test_text[index_of_first_name+11:l]
				print(test_text_part2)
				await bot.send_message(call.from_user.id, test_text_part1 + call.from_user.first_name + test_text_part2, reply_markup=main_menu)
			else:
				await bot.send_message(call.from_user.id, str(get_text_of_button_id(id=8)), reply_markup=main_menu)

	# обработкан нажатия по категории
	store_categories = get_full_list_categories_of_store()
	for number in range(len(store_categories)):
		if str(store_categories[number]) == str(call.data):
			# Отправка фотографии категории
			filename_path = get_filename_of_category_image(title=str(store_categories[number]))
			print(filename_path)
			#print(filename_path)
			check_file = os.path.exists('static/'+str(filename_path))
			print(check_file)
			# Проверка есть ли что - то, если нету - не отправлять
			if check_file == True:
				with open('static/'+filename_path, 'rb') as photo:
					await bot.send_photo(call.from_user.id, photo)
			# Удаление всех риалсейлов по клиенту и подготовка занесение нового
			delete_realsales_user_id(user_id=call.from_user.id)
			# Вывод всех продуктов по заданной категории ( готово )
			all_products = get_name_podcategory_po_category(name_category=str(call.data))
			menu_products = types.InlineKeyboardMarkup()
			for number in range(len(all_products)):
				button = types.InlineKeyboardButton(text=str(all_products[number]), callback_data=str(all_products[number]))
				menu_products.add(button)

			await bot.send_message(call.from_user.id, "Выберите подкатегорию:", reply_markup=menu_products)			
		else:  
			pass




	# Обработка нажатии по подкатегории		
	store_podcategories = get_full_list_podcategories_of_store()
	for number in range(len(store_podcategories)):
		if str(store_podcategories[number]) == str(call.data):
			# Отправка фотографии категории
			filename_path = get_filename_of_podcategory_image(title=str(store_podcategories[number]))
			check_file = os.path.exists('static/'+str(filename_path))
			if check_file == True:
				with open('static/'+filename_path, 'rb') as photo:
					await bot.send_photo(call.from_user.id, photo)
			# Вывод всех продуктов по заданной подкатегории ( готово )
			all_podproducts = get_name_tovara_po_podcategory(name_category=str(call.data))
			menu_podproducts = types.InlineKeyboardMarkup()
			for number in range(len(all_podproducts)):
				button = types.InlineKeyboardButton(text=str(all_podproducts[number]), callback_data=str(all_podproducts[number]))
				menu_podproducts.add(button)

			await bot.send_message(call.from_user.id, "Выберите товар:", reply_markup=menu_podproducts)			
		else:  
			pass

	# Обработка при нажатии на выведенный товар
	store_products = get_full_name_products_of_store()
	for number in range(len(store_products)):
		if str(store_products[number]) == str(call.data):
			print("1.Try to send product:" + str(store_products[number]))

			# Вывод информации о товаре
			await bot.send_message(call.from_user.id, await info_product_out(user_choice_product_id=str(call.data)), reply_markup=product_menu)
			# Вносим риал - тайм покупку в базу ( запоминаем все нужные данные )
			delete_realsales_user_id(user_id=call.from_user.id)
			in_text_real_sale(user_id=call.from_user.id, item_name=str(call.data), count=1)
		else:
			pass


	# Обработка при нажатии кнопки "Купить"
	if str(call.data) == "buy_button":
		await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id , reply_markup=product_buy_meny)
		print("2.Try to send product:" + str(get_item_name_from_real_sale(user_id = call.message.chat.id)))
	else:
		pass


	# Обработка при нажатии кнопки "Купить ( выбор количества ) "
	if str(call.data) == "product_buy_now_button":
		await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id , reply_markup=how_to_buy_menu)
		print("3.Try to send product:" + str(get_item_name_from_real_sale(user_id = call.message.chat.id)))
	else:
		pass


	# Обработка оплаты личным счётом в боте
	if str(call.data) == "oplata_cheta_button":
		# Проверка есть ли на счету нужная сумма
		update_price = get_name_tovara_price(name_tovara=str(store_products[number]))
		if int(get_name_tovara_price(name_tovara=str(get_item_name_from_real_sale(user_id = call.message.chat.id)))) > get_balance_of_user(user_id=call.from_user.id):
			print("Update price = " + str(update_price))
			await bot.send_message(call.from_user.id, "У вас не хватает денег на счету для оплаты данных товаров.")
		else:
			# Проверка есть ли нужное количество товара
			#if get_name_tovara_kolvo()
			# Списание счета
			print("Update price = " + str(update_price))
			new_balance = get_balance_of_user(user_id=call.from_user.id) - int(get_name_tovara_price(name_tovara=str(get_item_name_from_real_sale(user_id = call.message.chat.id))))
			update_balance_of_user(balance=new_balance, user_id=call.from_user.id)
			# Списание количества товара 
			time_kolvo_tovara = int(get_name_tovara_price(name_tovara=str(store_products[number]))) / int(get_name_tovara_price(name_tovara=str(store_products[number])))
			time_kolvo_tovara = 1
			print("Update price = " + str(update_price))
			print("Get name tovara price = " + str(get_name_tovara_price(name_tovara=str(store_products[number]))))
			update_kolvo_of_product(kolvo_tovara = int(get_name_tovara_kolvo(name_tovara=str(get_item_name_from_real_sale(user_id = call.message.chat.id)))) - time_kolvo_tovara, name_tovara=str(get_item_name_from_real_sale(user_id = call.message.chat.id)))
			# Отправка айди админу оповещение о покупке товара
			await bot.send_message(username_of_admin_channel, "( смайл ) Новый заказ в магазине! \n\nСумма заказа: " + str(get_name_tovara_price(name_tovara=str(get_item_name_from_real_sale(user_id = call.message.chat.id)))))

			# Оплата прошла успешно
			await bot.send_message(call.from_user.id, "Спасибо за покупку в нашем магазине. \nОплата прошла успешно")
			# Занесение покупки в базу данных в корзине
			add_sale_to_sells_base(user_id=call.from_user.id, name_tovara=str(get_item_name_from_real_sale(user_id = call.message.chat.id)), kolvo_tovara = time_kolvo_tovara, data_of_sale=str(now.day) + "." + str(now.month) + "." + str(now.year), time_of_sale=str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
			# Отправка аккаунтов
			print("4. Try to send product:" + str(get_item_name_from_real_sale(user_id = call.message.chat.id)))
			await bot.send_message(call.from_user.id, "Ваш товар: \n" + str(get_text_from_account_base(product_name=str(get_item_name_from_real_sale(user_id = call.message.chat.id)))))
			delete_realsales_user_id(user_id=call.from_user.id)	
	else:
		pass







#Запуск самого бота    
if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)

