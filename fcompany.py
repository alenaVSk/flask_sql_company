import sqlite3
import os
from flask import Flask, render_template, url_for, request, g, flash, abort, redirect
from FDataBase import FDataBase
#from row_data import process_row_data

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
    return render_template("zhurnal.html", title="Журнал", log=dbase.getLog())


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
        dbase.delete_entry(entry_id)
        flash('Запись успешно удалена', 'success')
    except:
        flash('Ошибка удаления записи', 'danger')
    return redirect(url_for('showZhurnal'))


# Маршрут для страницы редактирования записи записи в "Журнал"
@app.route('/edit_entry/<int:entry_id>', methods=['GET'])
def edit_entry(entry_id):
    entry_data = dbase.get_entry(entry_id)
    # print(entry_data)  # Проверка, получены ли данные
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
    #print(entry_id, entry_data)  # Проверка, получены ли данные

    return render_template('act.html', title="Составить акт выполненных работ", entry_data=entry_data)


# Маршрут для добавления данных в акт
@app.route('/edit_entry_act/<int:entry_id>', methods=['POST'])
def save_new_act(entry_id):
    # Получить данные из формы
    id_acts = request.form.getlist('id_act[]')
    date_acts = request.form.getlist('date_act[]')
    name_works = request.form.getlist('name_work[]')
    price_works = request.form.getlist('price_work[]')
    names = request.form.getlist('name[]')
    price_units = request.form.getlist('price_unit[]')
    quantities = request.form.getlist('quantity[]')

    # проверяем, что длина всех списков одинакова
    for i in range(len(id_acts)):
        dbase.save_new_act(id_acts[i], date_acts[i], name_works[i], price_works[i])
        dbase.save_new_stock_minus(names[i], price_units[i], quantities[i], id_acts[i])
        dbase.save_id_act_to_log(id_acts[i], entry_id)

    return redirect(url_for('edit_entry_act', entry_id=entry_id))


@app.route("/stock")
def showStock():
    return render_template("stock.html", title="Склад материалов", stock=dbase.getStock())


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


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)
