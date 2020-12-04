# -*- coding: utf8 -*-
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
# import dbworker
# import config
import datetime
import logging
import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user
from flask_login import UserMixin
from flask_login import LoginManager

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

UPLOAD_FOLDER = 'static/'

app.secret_key = 'some secret salt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

manager = LoginManager(app)


# Таблица для текстовых обновлений админки
class AdminUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)


# Таблица для кнопок в боте
class TelButton(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<TelButton %r>' % self.id


# Таблица для подкатегорий
class PodCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(300))
    main_category = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<PodCategory %r>' % self.id


# Таблица для покупок прямо сейчас
class Realsale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    item_name = db.Column(db.Text, nullable=False)
    count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Realsale %r>' % self.id


# Таблица для аккаунтов ( текстовых файлов для отображения пользователя )
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    account_text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Account %r>' % self.id


# Таблица для рефералов
class Referal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    wallet = db.Column(db.Text, nullable=False)
    curator = db.Column(db.String, nullable=False)
    ref_invited = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Referal %r>' % self.id


# Таблица базы данных для продаж
class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, nullable=False)
    name_tovara = db.Column(db.Text, nullable=False)
    kolvo_tovara = db.Column(db.Integer, nullable=False)
    data_of_sale = db.Column(db.String, nullable=False)
    time_of_sale = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Sales %r>' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.Text)
    date = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


class AdminUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Wallet %r>' % self.id


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(300))
    link = db.Column(db.String(100))

    def __repr__(self):
        return '<Category %r>' % self.id


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    kolvo = db.Column(db.Integer, nullable=False, default=0)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    limit_on_time_purchase = db.Column(db.Integer, nullable=False) #

    def __repr__(self):
        return '<Product %r>' % self.id


# База данных купонов
class Coupone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_coupone = db.Column(db.String(100), nullable=False)
    procent = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Coupone %r>' % self.id


# Base of send - messages from bot
class SendMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text_message = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<SendMessage %r>' % self.id


@manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(user_id)


# Обработка ошибок доступа к логину
@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page'))

    return response


@app.route("/admin/send-message")
@login_required
def adminSendMessages():
    send_messages = SendMessage.query.all()
    return render_template("sendmessages.html", send_messages=send_messages)


@app.route('/admin/create-sendmessage', methods=['POST', 'GET'])
@login_required
def adminCreateSendMessage():
    if request.method == "POST":
        title = request.form['title']
        text_message = request.form['text_message']

        sendmessage = SendMessage(title=title, text_message=text_message)

        try:
            db.session.add(sendmessage)
            db.session.commit()
            return redirect('/admin/send-message')
        except:
            return "При добавлении рассылки произошла ошибка"
    else:
        return render_template("create_sendmessage.html")


@app.route('/admin/create-account', methods=['POST', 'GET'])
@login_required
def adminCreateAccount():
    if request.method == "POST":
        product_name = request.form['product_name']
        account_text = request.form['account_text']

        account = Account(product_name=product_name, account_text=account_text)

        product = Product.query.filter_by(title=product_name).first()
        product.kolvo = int(product.kolvo + 1)

        try:
            db.session.add(account)
            db.session.commit()
            return redirect('/admin/accounts')
        except:
            return "При добавлении аккаунта произошла ошибка"
    else:
        products = Product.query.all()
        return render_template("create_account.html", products=products)


@app.route('/admin/accounts')
@login_required
def adminAccounts():
    accounts = Account.query.all()
    return render_template("account.html", accounts=accounts)


@app.route('/admin/coupone')
@login_required
def adminCoupones():
    coupones = Coupone.query.all()
    return render_template("coupone.html", coupones=coupones)


@app.route('/admin/create-category', methods=['POST', 'GET'])
@login_required
def adminCreateCategory():
    if request.method == "POST":
        title = request.form['title']
        file = request.files['inputFile']
        # link = request.form['link']

        # Пропишем проверку, если нету фотографии категории
        if not file:
            category = Category(title=title, link='link' + str(title), image='Null')
        else:
            category = Category(title=title, link='link' + str(title), image=file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        try:
            db.session.add(category)
            db.session.commit()
            return redirect('/admin/categories')
        except:
            return "При добавлении категории произошла ошибка"
    else:
        return render_template("create_category.html")


# Обработка декоратара создания подкатегории
@app.route('/admin/create-podcategory', methods=['POST', 'GET'])
@login_required
def adminCreatePodCategory():
    if request.method == "POST":
        title = request.form['title']
        file = request.files['inputFile']
        main_category = request.form['mainCategory']

        # Пропишем проверку, если нету фотографии категории
        if not file:
            podcategory = PodCategory(title=title, image='Null', main_category=main_category)
        else:
            podcategory = PodCategory(title=title, image=file.filename, main_category=main_category)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        try:
            db.session.add(podcategory)
            db.session.commit()
            return redirect('/admin/podcategories')
        except:
            return "При добавлении категории произошла ошибка"
    else:
        category = Category.query.all()
        return render_template("create_podcategory.html", categories=category)


# Обработка декоратора октрывания подкатегорий
@app.route("/admin/podcategories")
@login_required
def adminPodCategories():
    podcategories = PodCategory.query.all()
    return render_template("podcategory.html", podcategories=podcategories)


@app.route("/admin/create-coupone", methods=['POST', 'GET'])
@login_required
def adminCreateCoupone():
    if request.method == "POST":
        name_coupone = request.form['name_coupone']
        procent = request.form['procent']

        coupone = Coupone(name_coupone=name_coupone, procent=procent)

        try:
            db.session.add(coupone)
            db.session.commit()
            return redirect('/admin/coupone')
        except:
            return "При добавлении купона произошла ошибка"
    else:
        return render_template("create_coupone.html")


@app.route('/admin/create-product', methods=['POST', 'GET'])
@login_required
def createArticle():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        category = request.form['category']
        description = request.form['description']
        limit_on_time_purchase = request.form['limit_on_time_purchase'] #

        product = Product(title=title, price=price, kolvo=0, category=category, description=description,
                          limit_on_time_purchase=limit_on_time_purchase) #

        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/admin/products')
        except:
            return "При добавлении продукта произошла ошибка"
    else:
        podcategories = PodCategory.query.all()
        return render_template("create_product.html", podcategories=podcategories)


@app.route("/admin/products")
@login_required
def adminProducts():
    products = Product.query.all()
    print(products)
    # categories = Category.query.filter_by(title=products[2]).all()
    return render_template("product.html", products=products)


@app.route("/admin/categories")
@login_required
def adminCategories():
    categories = Category.query.all()
    return render_template("category.html", categories=categories)


@app.route("/admin/users")
@login_required
def adminUsers():
    users = User.query.all()
    # Выводим общее число пользователей
    users_count = User.query.count()
    # Обозначаем реферальную ссылку и передаем её в темплейт
    ref_link_user = "https://t.me/Gold_Games_bot?start="
    # Обозначаем юзер инфо для создания моделей
    modals = User.query.all()
    return render_template("users.html", users=users, users_count=users_count, ref_link_user=ref_link_user,
                           modals=modals)


# Отработка декоратора вывода аккаунтов администратора и добавления нового
@app.route("/admin/register", methods=['POST', 'GET'])
@login_required
def adminRegisterUsers():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if not (login or password or password2):
            print('Пожалуйста, заполните все поля')
        elif password != password2:
            print('Поля пароля неодинаковые!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = AdminUser(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('adminRegisterUsers'))
    else:
        adminusers = AdminUser.query.all()
        return render_template("register.html", adminusers=adminusers)


# Отработка декоратара логин страницы
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = AdminUser.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            print('Логин или пароль неверны')
    else:
        print('Пожалуйста введите все поля!')

    return render_template('login.html')


# Редактирование продукта
@app.route('/admin/posts/<int:id>/update', methods=['POST', 'GET'])
@login_required
def post_update(id):
    product = Product.query.get(id)
    if request.method == "POST":
        product.title = request.form['title']
        product.price = request.form['price']
        product.category = request.form['category']
        product.description = request.form['description']
        product.limit_on_time_purchase = request.form['limit_on_time_purchase'] #

        try:
            db.session.commit()
            return redirect('/admin/products')
        except:
            return "При редактировании товара произошла ошибка"
    else:
        podcategories = PodCategory.query.all()
        return render_template("product_update.html", product=product, podcategories=podcategories)


# Удаление продукта
@app.route('/admin/posts/<int:id>/del')
@login_required
def post_delete(id):
    product = Product.query.get_or_404(id)

    try:
        db.session.delete(product)
        db.session.commit()
        return redirect('/admin/products')
    except:
        return "При удалении товара произошла ошибки"

    return render_template("product_update.html", product=product)


# Удаление аккаунта
@app.route('/admin/accounts/<int:id>/del')
@login_required
def accountDelete(id):
    account = Account.query.get_or_404(id)

    try:
        db.session.delete(account)
        db.session.commit()
        return redirect('/admin/accounts')
    except:
        return "При удалении аккаунта произошла ошибки"

    return render_template("product_update.html", product=product)


# Удаление подкатегории
@app.route('/admin/podacategories/<int:id>/del')
@login_required
def podcategoryDelete(id):
    podcategory = PodCategory.query.get_or_404(id)

    try:
        db.session.delete(podcategory)
        db.session.commit()
        return redirect('/admin/podcategories')
    except:
        return "При удалении подкатегории произошла ошибки"

    return render_template("product_update.html")


# Удаление администратора
@app.route('/admin/register/<int:id>/del')
@login_required
def adminUserDelete(id):
    useradmin = AdminUser.query.get_or_404(id)

    try:
        db.session.delete(useradmin)
        db.session.commit()
        return redirect('/admin/register')
    except:
        return "При удалении администратора произошла ошибки"

    return render_template("register.html", adminusers=adminusers)


# Редактирование категории
@app.route('/admin/category/<int:id>/update', methods=['POST', 'GET'])
@login_required
def categoryUpdate(id):
    category = Category.query.get(id)
    if request.method == "POST":
        category.title = request.form['title']
        file = request.files['inputFile']
        category.link = request.form['link']

        if not file:
            pass
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            category.image = file.filename

        try:
            db.session.commit()
            return redirect('/admin/categories')
        except:
            return "При редактировании категории произошла ошибка"
    else:
        return render_template("category_update.html", category=category)


# Редактирование подкатегории
@app.route('/admin/podcategory/<int:id>/update', methods=['POST', 'GET'])
@login_required
def podcategoryUpdate(id):
    podcategory = PodCategory.query.get(id)
    if request.method == "POST":
        podcategory.title = request.form['title']
        file = request.files['inputFile']
        podcategory.main_category = request.form['main_category']

        if not file:
            pass
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            category.image = file.filename

        try:
            db.session.commit()
            return redirect('/admin/podcategories')
        except:
            return "При редактировании подкатегории произошла ошибка"
    else:
        categories = Category.query.all()
        return render_template("podcategory_update.html", podcategory=podcategory, categories=categories)


# Удаление категории
@app.route('/admin/categories/<int:id>/del')
@login_required
def categoryDelete(id):
    category = Category.query.get_or_404(id)

    try:
        db.session.delete(category)
        db.session.commit()
        return redirect('/admin/categories')
    except:
        return "При удалении категории произошла ошибки"

    return render_template("category_update.html", category=category)


# Редактирование купона
@app.route('/admin/coupone/<int:id>/update', methods=['POST', 'GET'])
@login_required
def couponeUpdate(id):
    coupone = Coupone.query.get(id)
    if request.method == "POST":
        coupone.name_coupone = request.form['name_coupone']
        coupone.procent = request.form['procent']

        try:
            db.session.commit()
            return redirect('/admin/coupone')
        except:
            return "При редактировании купона произошла ошибка"
    else:
        return render_template("coupone_update.html", coupone=coupone)


# Удаление купона
@app.route('/admin/coupone/<int:id>/del')
@login_required
def couponeDelete(id):
    coupone = Coupone.query.get_or_404(id)

    try:
        db.session.delete(coupone)
        db.session.commit()
        return redirect('/admin/coupone')
    except:
        return "При удалении купона произошла ошибки"

    return render_template("coupone_update.html", coupone=coupone)


# Редактирование рассылки
@app.route('/admin/send-message/<int:id>/update', methods=['POST', 'GET'])
@login_required
def sendmessageUpdate(id):
    sendmessage = SendMessage.query.get(id)
    if request.method == "POST":
        sendmessage.title = request.form['title']
        sendmessage.text_message = request.form['text_message']

        try:
            db.session.commit()
            return redirect('/admin/send-message')
        except:
            return "При редактировании рассылки произошла ошибка"
    else:
        return render_template("sendmessage_update.html", sendmessage=sendmessage)


# Редактирование аккаунта ( текстового файла )
@app.route('/admin/accounts/<int:id>/update', methods=['POST', 'GET'])
@login_required
def accountUpdate(id):
    account = Account.query.get(id)
    if request.method == "POST":
        account.product_name = request.form['product_name']
        account.account_text = request.form['account_text']

        try:
            db.session.commit()
            return redirect('/admin/accounts')
        except:
            return "При редактировании аккаунта произошла ошибка"
    else:
        products = Product.query.all()
        return render_template("account_update.html", account=account, products=products)


# Удаление рассылки
@app.route('/admin/send-message/<int:id>/del')
@login_required
def sendmessageDelete(id):
    sendmessage = SendMessage.query.get_or_404(id)

    try:
        db.session.delete(sendmessage)
        db.session.commit()
        return redirect('/admin/send-message')
    except:
        return "При удалении рассылки произошла ошибки"

    return render_template("sendmessage_update.html", sendmessage=sendmessage)


# Раздел конструктора кнопок в телеграме
@app.route("/admin/buttons", methods=['POST', 'GET'])
@login_required
def adminButtons():
    telegrambuttons = TelButton.query.all()
    if request.method == "POST":
        telegrambuttons[0].name = request.form['name1']
        telegrambuttons[0].text = request.form['text1']
        telegrambuttons[1].name = request.form['name2']
        telegrambuttons[1].text = request.form['text2']
        telegrambuttons[2].name = request.form['name3']
        telegrambuttons[2].text = request.form['text3']
        telegrambuttons[3].name = request.form['name4']
        telegrambuttons[3].text = request.form['text4']
        telegrambuttons[4].name = request.form['name5']
        telegrambuttons[4].text = request.form['text5']
        telegrambuttons[5].name = request.form['name6']
        telegrambuttons[5].text = request.form['text6']
        telegrambuttons[6].name = request.form['name7']
        telegrambuttons[6].text = request.form['text7']
        telegrambuttons[7].name = request.form['name8']
        telegrambuttons[7].text = request.form['text8']
        telegrambuttons[8].name = request.form['name9']
        telegrambuttons[8].text = request.form['text9']

        try:
            db.session.commit()
            return redirect('/admin/buttons')
        except:
            return "При обновлении кнопок произошла ошибка"

    else:
        telegrambuttons = TelButton.query.all()
        return render_template("buttons.html", telegrambuttons=telegrambuttons)


# Раздел покупок в боте
@app.route("/admin/sales")
@login_required
def adminSales():
    sales = Sales.query.all()
    sales.reverse()
    return render_template("sales.html", sales=sales)


# Раздел покупок прямо сейчас в боте
@app.route("/admin/realsales")
@login_required
def adminRealSales():
    realsales = Realsale.query.all()
    realsales.reverse()
    return render_template("realsales.html", realsales=realsales)


# Раздел админ обновлений в боте
@app.route("/admin/updates")
@login_required
def adminUpdates():
    updates = AdminUpdate.query.all()
    updates.reverse()
    return render_template("updates.html", updates=updates)

# Тестовая страница
@app.route("/admin/test-page")
@login_required
def testPage():
    return render_template("test-new-design.html")


@app.route('/')
@login_required
def index():
    # Выводим количество товаров в магазине
    accounts = Account.query.count()
    # Выводим общую сумму заработка в магазине ( надо плюсовать каждую покупку )

    # Выводим общее количество юзеров в боте
    users = User.query.count()

    # Выводим общее количество категорий в боте
    categories = Category.query.count()

    # Выводим общее количество покупок в боте за всё время
    sales = Sales.query.count()

    return render_template("admin.html", accounts=accounts, users=users, categories=categories, sales=sales)


# Обработка логаута
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
