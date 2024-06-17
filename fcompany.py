import sqlite3
import os
from flask import Flask, render_template, url_for, request, g, flash, redirect
from FDataBase import FDataBase
from math import ceil


# конфигурация
DATABASE = '/tmp/fcompany.db'  # путь к БД
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
USERNAME = 'admin'
PASSWORD = '123'


app = Flask(__name__)
app.config.from_object(__name__)  # загружаем конфигурацию из приложения (__name__ ссылается на этот текущий модуль)

app.config.update(dict(DATABASE=os.path.join(app.root_path,'fcompany.db'))) # переопределим путь к БД(ссылка на тек каталог


def connect_db():  # общая функция для установления соединения с БД
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row  # записи будут представлены не в виде кортежей, а в виде словаря (для исп в шаблонах)
    return conn

def create_db():
    """Вспомогательная функция для создания таблиц БД (без запуска вебсервера)"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:  # откр файл для чтения
        db.cursor().executescript(f.read())      # выполняем скрипт кот находится в файле
    db.commit()             # применить изменения к текущей БД
    db.close()             # закрыть установленное соединение


def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/zhurnal")
def showZhurnal():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Количество элементов на странице
    log_query = dbase.getLog()  # Получаем все элементы журнала
    total_items = len(log_query)  # Получаем общее количество элементов
    total_pages = ceil(total_items / per_page)  # Вычисляем общее количество страниц
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    log = log_query[start_index:end_index]  # Получаем элементы текущей страницы
    pagination = {
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'total_items': total_items
    }
    return render_template("zhurnal.html", title="Журнал", log=log, pagination=pagination)


@app.route("/add_customer", methods=["POST", "GET"])
def addCustomer():
    if request.method == "POST":

        res = dbase.addCustomer(request.form['date_order'], request.form['name_customer'], request.form['brand_car'],
                                request.form['year_car'], request.form['number_car'], request.form['text_order'], request.form['id_act'])
        if not res:
            flash('Ошибка добавления', category='error')
        else:
            flash('Запись добавлена успешно', category='success')

    return render_template('add_customer.html', title="Добавление записи в журнал")


# Маршрут для удаления записи в "Журнал"
@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    try:
        result = dbase.check_delete_entry(entry_id)
        if result and result[0]:
            message = 'Удаление запрещено, так как составлен акт выполненных работ'
            status = 'error'
        else:
            dbase.delete_entry(entry_id)
            message = 'Запись успешно удалена'
            status = 'success'
    except Exception as e:
        print("Ошибка удаления записи:", str(e))
        message = 'Ошибка удаления записи'
        status = 'error'

    return redirect(url_for('showZhurnal', status=status, message=message))

# Маршрут для страницы редактирования записи записи в "Журнал"
@app.route('/edit_entry/<int:entry_id>', methods=['GET'])
def edit_entry(entry_id):
    entry_data = dbase.get_entry(entry_id)
    print('entry_data', entry_data)  # Проверка, получены ли данные
    return render_template('edit_entry.html', title="Редактировать", entry_data=entry_data)


# Маршрут для сохранения изменений в "Журнал"
@app.route('/save_entry/<int:entry_id>', methods=['POST'])
def save_entry(entry_id):
    date_order = request.form['date_order']
    name_customer = request.form['name_customer']
    brand_car = request.form['brand_car']
    year_car = request.form['year_car']
    number_car = request.form['number_car']
    text_order = request.form['text_order']
    id_act = request.form['id_act']
    dbase.update_entry(entry_id, date_order, name_customer, brand_car, year_car, number_car, text_order, id_act)
    return redirect(url_for('showZhurnal'))


# Маршрут для составления акта (получение данных из "Журнала" по id)
@app.route('/edit_entry_act/<int:entry_id>', methods=['GET'])
def edit_entry_act(entry_id):
    entry_data = dbase.get_entry(entry_id)

    return render_template('act.html', title="Составить акт выполненных работ", entry_data=entry_data)


# Маршрут для добавления данных в акт
@app.route('/save_new_act/<int:entry_id>', methods=['POST'])
def save_new_act(entry_id):
    print("Получение данных из формы...")
    id_acts = request.form.getlist('id_act[]')
    date_acts = request.form.getlist('date_act[]')
    name_works = request.form.getlist('name_work[]')
    price_works = request.form.getlist('price_work[]')
    names = request.form.getlist('name[]')
    price_units = request.form.getlist('price_unit[]')
    quantities = request.form.getlist('quantity[]')

    print(f"Полученные данные: id_acts={id_acts}, date_acts={date_acts}, name_works={name_works}, price_works={price_works}, names={names}, price_units={price_units}, quantities={quantities}")

    for i in range(len(name_works)):
        id_act = id_acts[0]  # Предполагаем, что id_act и date_act одинаковы для всех строк
        date_act = date_acts[0]
        name_work = name_works[i]
        price_work = price_works[i]

        print(f"Сохранение строки {i + 1} в act...")
        saved_id_act = dbase.save_new_act(id_act, date_act, name_work, price_work)
        if saved_id_act is not None:
            # Поскольку materials тоже имеют несколько строк, используем i для их индексации
            if i < len(names):
                name = names[i]
                price_unit = price_units[i]
                quantity = quantities[i]
                print(f"Сохранение строки {i + 1} в stock_minus...")
                dbase.save_new_stock_minus(name, price_unit, quantity, saved_id_act)

    print(f"Сохранение id_act={id_acts[0]} в log...")
    dbase.save_id_act_to_log(id_acts[0], entry_id)

    print("Перенаправление на страницу edit_entry_act...")
    return redirect(url_for('edit_entry_act', entry_id=entry_id))  # перенаправить на финальный акт !!!!!!


# Маршрут для перехода в реестр актов
@app.route("/list_act")
def showList_act():

    page = request.args.get('page', 1, type=int)
    per_page = 10  # Количество элементов на странице
    list_act_query = dbase.getList_act()  # Получаем все элементы реестра
    total_items = len(list_act_query)  # Получаем общее количество элементов
    total_pages = ceil(total_items / per_page)  # Вычисляем общее количество страниц
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    list_act = list_act_query[start_index:end_index]  # Получаем элементы текущей страницы
    pagination = {
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'total_items': total_items
    }
    return render_template("list_act.html", title="Реестр", list_act=list_act, pagination=pagination)


# Маршрут для отображения финального акта (получение данных из "Реестра" по id)
@app.route('/final_act/<int:entry_id>')
def showFinal_act(entry_id):
    print('entry_id: ', entry_id)
    entry_data = dbase.get_final_act(entry_id)

    return render_template('final_act.html', title="Акт выполненных работ", entry_data=entry_data)


# Маршрут для редактирования финального акта
@app.route('/edit_final_act/<int:entry_id>')
def edit_final_act(entry_id):
    entry_data = dbase.get_final_act(entry_id)
    print(f"Entry data: {entry_data}")
    print('edit_final_ac - entry_id: ', entry_id)
    return render_template('edit_final_act.html', title="Редактировать", entry_data=entry_data)


# Маршрут для сохранения изменённых и/или добавленных данных в финальном акте
@app.route('/save_edit_final_act/<int:entry_id>', methods=['POST'])
def save_edit_final_act(entry_id):

    name_works = request.form.getlist('name_work[]')
    price_works = request.form.getlist('price_work[]')
    names = request.form.getlist('name[]')
    price_units = request.form.getlist('price_unit[]')
    quantities = request.form.getlist('quantity[]')
    date_act = request.form.get('date_act')  # Добавляем получение даты акта из формы
    print(
        f"Полученные данные: date_act={date_act}, name_works={name_works}, price_works={price_works}, names={names}, price_units={price_units}, quantities={quantities}")

    new_act_values = [(name_work, price_work) for name_work, price_work in zip(name_works, price_works)]
    new_stock_minus_values = [(name, price_unit, quantity) for name, price_unit, quantity in
                              zip(names, price_units, quantities)]

    print(f"new_act_values: {new_act_values}")
    print(f"new_stock_minus_values: {new_stock_minus_values}")

    dbase.update_act_and_stock_minus(entry_id, date_act, new_act_values, new_stock_minus_values)

    return redirect(url_for('showFinal_act', entry_id=entry_id))


@app.route("/stock")
def showStock():
    page = request.args.get('page', 1, type=int)
    per_page = 3  # Количество элементов на странице
    stock_query = dbase.getStock()  # Получаем все элементы склада
    total_items = len(stock_query)  # Получаем общее количество элементов
    total_pages = ceil(total_items / per_page)  # Вычисляем общее количество страниц
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    stock = stock_query[start_index:end_index]  # Получаем элементы текущей страницы
    pagination = {
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'total_items': total_items
    }
    return render_template("stock.html", title="Склад материалов", stock=stock, pagination=pagination)


@app.route("/add_stock", methods=["POST", "GET"])
def addStock():
    if request.method == "POST":

        res = dbase.addStock(request.form['name'], request.form['quantity'], request.form['price_unit'])
        if not res:
            flash('Ошибка добавления', category='error')
        else:
            flash('Запись добавлена успешно', category='success')

    return render_template('add_stock.html', title="Добавление материалов на склад")


@app.route("/employees")
def showEmployees():
    return render_template("employees.html", title="Сотрудники", employees=dbase.getEmployees())


@app.route("/add_employees", methods=["POST", "GET"])
def addEmployees():
    if request.method == "POST":

        res = dbase.addEmployees(request.form['name'], request.form['profession'])
        if not res:
            flash('Ошибка добавления', category='error')
        else:
            flash('Запись добавлена успешно', category='success')

    return render_template('add_employees.html', title="Добавление сотрудника")


# Маршрут для удаления записи в "Сотрудники"
@app.route('/delete_entry_employees/<int:entry_id>', methods=['POST'])
def delete_entry_employees(entry_id):
    try:
        dbase.delete_entry_employees(entry_id)
        flash('Запись успешно удалена', 'success')
    except:
        flash('Ошибка удаления записи', 'danger')
    return redirect(url_for('showEmployees'))


# Маршрут для страницы редактирования записи записи в "Сотрудники"
@app.route('/edit_entry_employees/<int:entry_id>', methods=['GET'])
def edit_entry_employees(entry_id):
    entry_data = dbase.get_entry_employees(entry_id)
    # print(entry_data)  # Проверка, получены ли данные
    return render_template('edit_entry_employees.html', title="Редактировать", entry_data=entry_data)


# Маршрут для сохранения изменений  в "Сотрудники"
@app.route('/save_entry_employees/<int:entry_id>', methods=['POST'])
def save_entry_employees(entry_id):
    name = request.form['name']
    profession = request.form['profession']
    dbase.update_entry_employees(entry_id, name, profession)
    return redirect(url_for('showEmployees'))


@app.route('/requisites')
def requisites():
    return render_template('requisites.html')


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)
