# import sqlite3
import psycopg2


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()


    def getLog(self):
        sql = '''SELECT * FROM log
                 ORDER BY
                         log.id;'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            # Преобразование каждой строки в список значений
            log_list = [dict(row) for row in res]
            if log_list: return log_list
        except psycopg2.Error as e:
            print("Ошибка чтения из БД:", e)
        return []

    def addCustomer(self, date_order, name_customer, brand_car, year_car, number_car, text_order, id_act):
        try:
            # Если id_act пустая строка, заменяем его на None
            if id_act == '':
                id_act = None

            self.__cur.execute("""
                INSERT INTO log (date_order, name_customer, brand_car, year_car, number_car, text_order, id_act)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (date_order, name_customer, brand_car, year_car, number_car, text_order, id_act))

            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка добавления записи в БД:", e)
            return False
        return True

    # Метод для проверки существования акта к данному заказу(если да - удаление запрещено)
    def check_delete_entry(self, entry_id):
        sql = '''SELECT id_act FROM log WHERE id = %s'''
        try:
            self.__cur.execute(sql, (entry_id,))
            result = self.__cur.fetchone()
            return result
        except psycopg2.Error as e:
            print("Ошибка проверки записи:", e)
            return None

    # Метод для удаления записи (если не составлен акт)
    def delete_entry(self, entry_id):
        sql = '''DELETE FROM log WHERE id = %s'''
        try:
            self.__cur.execute(sql, (entry_id,))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка проверки записи:", e)
            self.__db.rollback()

    # Метод для перехода из "Журнала" по данной записи (по entry_id)
    def get_entry(self, entry_id):
        sql = '''SELECT * FROM log WHERE id = %s'''
        try:
            self.__cur.execute(sql, (entry_id,))
            res = self.__cur.fetchone()
            if res:
                return dict(res)
        except psycopg2.Error as e:
            print("Ошибка при получении записи из БД:", e)
        return None

    # Метод для обновления данных в Журнале
    def update_entry(self, entry_id, date_order, name_customer, brand_car, year_car, number_car, text_order, id_act):
        try:
            # Проверяем, является ли id_act None и заменяем на SQL NULL
            if id_act == "" or id_act is None:
                id_act = None
            else:
                # Если id_act не None, убедимся, что это целое число
                id_act = int(id_act)

            sql = '''UPDATE log 
                     SET date_order = %s, name_customer = %s, brand_car = %s, year_car = %s, number_car = %s, text_order = %s, id_act = %s 
                     WHERE id = %s'''
            self.__cur.execute(sql, (date_order, name_customer, brand_car, year_car, number_car, text_order, id_act, entry_id))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка проверки записи:", e)
            self.__db.rollback()

    # Метод для добавления данных в act
    def save_new_act(self, id_act, date_act, name_work, price_work):
        sql = '''
            INSERT INTO act (id_act, date_act, name_work, price_work)
            VALUES (%s, %s, %s, %s)
        '''
        try:
            self.__cur.execute(sql, (id_act, date_act, name_work, price_work))
            self.__db.commit()

            return id_act
        except psycopg2.Error as e:
            print("Ошибка при сохранении новых данных в БД act:", e)
            return None

    # Метод для добавления данных в stock_minus
    def save_new_stock_minus(self, name, price_unit, quantity, id_act):
        sql = '''
            INSERT INTO stock_minus (name, price_unit, quantity, id_act)
            VALUES (%s, %s, %s, %s)
        '''
        try:
            self.__cur.execute(sql, (name, price_unit, quantity, id_act))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка при сохранении новых данных в БД stock_minus:", e)

    # Метод для добавления данных в log по entry_id
    def save_id_act_to_log(self, id_act, entry_id):

        sql = '''
            UPDATE log
            SET id_act = %s
            WHERE id = %s
        '''
        try:
            self.__cur.execute(sql, (id_act, entry_id))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка при обновлении записи в таблице log:", e)

    # Метод для отображения Реестра актов
    def getList_act(self):
        sql = '''SELECT 
                log.id_act,
                act.date_act,
                log.name_customer,
                log.brand_car,
                log.year_car,
                log.number_car,
                SUM(act.price_work) AS total_work,
                (
                    SELECT 
                        SUM(stock_minus.price_unit * stock_minus.quantity)
                    FROM 
                        stock_minus
                    WHERE 
                        stock_minus.id_act = log.id_act
                ) AS total_materials,
                (
                    SUM(act.price_work) +
                    (
                        SELECT 
                            SUM(stock_minus.price_unit * stock_minus.quantity)
                        FROM 
                            stock_minus
                        WHERE 
                            stock_minus.id_act = log.id_act
                    )
                ) AS total_price
            FROM 
                log
            JOIN 
                act ON log.id_act = act.id_act
            GROUP BY 
                log.id_act,
                act.date_act,
                log.name_customer,
                log.brand_car,
                log.year_car,
                log.number_car
            ORDER BY
                log.id_act;'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            # Преобразование каждой строки в список словарей с использованием ключей
            list_act_list = [
                {
                    'id_act': row[0],
                    'date_act': row[1],
                    'name_customer': row[2],
                    'brand_car': row[3],
                    'year_car': row[4],
                    'number_car': row[5],
                    'total_work': row[6],
                    'total_materials': row[7],
                    'total_price': row[8]
                } for row in res
            ]

            if list_act_list:
                return list_act_list
        except psycopg2.Error as e:
            print("Ошибка чтения из БД:", e)
        return []

        # Метод для перехода из "Реестра актов" по данной записи (по entry_id)
    def get_final_act(self, entry_id):
        sql_main = '''
        SELECT 
            log.id_act,
            act.date_act,
            log.name_customer,
            log.brand_car,
            log.year_car,
            log.number_car,
            SUM(act.price_work) AS total_work,
            (
                SELECT 
                    SUM(stock_minus.price_unit * stock_minus.quantity)
                FROM 
                    stock_minus
                WHERE 
                    stock_minus.id_act = log.id_act
            ) AS total_materials,
            (
                SUM(act.price_work) +
                (
                    SELECT 
                        SUM(stock_minus.price_unit * stock_minus.quantity)
                    FROM 
                        stock_minus
                    WHERE 
                        stock_minus.id_act = log.id_act
                )
            ) AS total_price
        FROM 
            log
        JOIN 
            act ON log.id_act = act.id_act
        WHERE 
            log.id_act = %s
        GROUP BY 
            log.id_act,
            act.date_act,
            log.name_customer,
            log.brand_car,
            log.year_car,
            log.number_car
        '''

        sql_works = '''
        SELECT 
            act.name_work,
            act.price_work
        FROM 
            act
        WHERE 
            act.id_act = %s
        '''

        sql_materials = '''
        SELECT 
            stock_minus.name,
            stock_minus.price_unit,
            stock_minus.quantity
        FROM 
            stock_minus
        WHERE 
            stock_minus.id_act = %s
        '''

        try:
            self.__cur.execute(sql_main, (entry_id,))
            main_data = self.__cur.fetchone()

            self.__cur.execute(sql_works, (entry_id,))
            works_data = self.__cur.fetchall()

            self.__cur.execute(sql_materials, (entry_id,))
            materials_data = self.__cur.fetchall()

            if main_data:
                return {
                    'main': dict(main_data),
                    'works': [dict(row) for row in works_data],
                    'materials': [dict(row) for row in materials_data]
                }
        except psycopg2.Error as e:
            print("Ошибка при получении записи из БД:", e)
        return None

        # Метод для обновления (добавления/удаления) данных в final act
    def delete_act_rows(self, entry_id):
        sql = '''DELETE FROM act WHERE id_act = %s'''
        self.__cur.execute(sql, (entry_id,))

    def delete_stock_minus_rows(self, entry_id):
        sql = '''DELETE FROM stock_minus WHERE id_act = %s'''
        self.__cur.execute(sql, (entry_id,))

    def insert_act_row(self, entry_id, date_act, name_work, price_work):
        sql = '''
            INSERT INTO act (id_act, date_act, name_work, price_work)
            VALUES (%s, %s, %s, %s)
        '''
        self.__cur.execute(sql, (entry_id, date_act, name_work, price_work))

    def insert_stock_minus_row(self, entry_id, name, price_unit, quantity):
        sql = '''
            INSERT INTO stock_minus (id_act, name, price_unit, quantity)
            VALUES (%s, %s, %s, %s)
        '''
        self.__cur.execute(sql, (entry_id, name, price_unit, quantity))

    def update_act_and_stock_minus(self, entry_id, date_act, new_act_values, new_stock_minus_values):
        try:
            self.__db.autocommit = False  # Начало транзакции

            # Удаление строк
            self.delete_act_rows(entry_id)
            self.delete_stock_minus_rows(entry_id)

            # Вставка новых значений в act
            for name_work, price_work in new_act_values:
                self.insert_act_row(entry_id, date_act, name_work, price_work)

            # Вставка новых значений в stock_minus
            for name, price_unit, quantity in new_stock_minus_values:
                self.insert_stock_minus_row(entry_id, name, price_unit, quantity)

            self.__db.commit()
        except psycopg2.Error as e:
            self.__db.rollback()
            print(f"Произошла ошибка при вставке в stock_minus: {e}")
        finally:
            self.__db.autocommit = True


    # Отображение Склада
    def getStock(self):
        sql = '''SELECT 
                 sp.name AS name_total,
                 COALESCE (sp.quantity, 0) - COALESCE (sm.quantity, 0) AS quantity_total,
                 sp.price_unit AS price_unit_total
                 FROM (SELECT SUM (quantity) AS quantity, name, price_unit
                    FROM stock_plus
                    GROUP BY 
                    name, price_unit) sp
                 
                 LEFT JOIN 
                    (SELECT SUM (quantity) AS quantity, name, price_unit
                    FROM stock_minus
                    GROUP BY 
                    name, price_unit) sm
                 ON sp.name = sm.name AND sp.price_unit = sm.price_unit
                 ORDER BY sp.name;'''

        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            # Преобразование каждой строки в список значений
            stock_list = [dict(row) for row in res]
            return stock_list
        except psycopg2.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
        return []

    # Метод для добавления в stock_plus
    def addStock(self, name, quantity, price_unit):
        try:
            self.__cur.execute('''
                INSERT INTO stock_plus (name, quantity, price_unit) 
                VALUES (%s, %s, %s);
                ''', (name, quantity, price_unit))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    # Список сотрудников
    def getEmployees(self):
        sql = '''SELECT * FROM employees'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            # Преобразование каждой строки в список значений
            employees_list = [dict(row) for row in res]
            if employees_list: return employees_list
        except psycopg2.Error as e:
            print("Ошибка чтения из БД")
        return []

    # Добавление сотрудника
    def addEmployees(self, name, profession):
        try:
            self.__cur.execute('''INSERT INTO employees VALUES(DEFAULT, %s, %s)''', (name, profession))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    # Удаление из списка сотрудников
    def delete_entry_employees(self, entry_id):
        sql = '''DELETE FROM employees WHERE id = %s'''
        try:
            self.__cur.execute(sql, (entry_id,))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка удаления из БД:", str(e))
            self.__db.rollback()

   # Редактирование списка сотрудников
    def get_entry_employees(self, entry_id):
        sql = '''SELECT * FROM employees WHERE id = %s'''
        try:
            self.__cur.execute(sql, (entry_id,))
            res = self.__cur.fetchone()
            if res:
                return dict(res)
        except psycopg2.Error as e:
            print("Ошибка при получении записи из БД:", str(e))
        return None

    # Метод для обновления данных о сотрудниках
    def update_entry_employees(self, entry_id, name, profession):
        try:
            sql = '''UPDATE employees
                     SET name = %s, profession = %s 
                     WHERE id = %s'''
            self.__cur.execute(sql, (name, profession, entry_id))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка при обновлении записи в БД:", str(e))
            self.__db.rollback()









