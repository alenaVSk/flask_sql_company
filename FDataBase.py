import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getLog(self):
        sql = '''SELECT * FROM log'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            # Преобразование каждой строки в список значений
            log_list = [dict(row) for row in res]
            if log_list: return log_list
        except:
            print("Ошибка чтения из БД")
        return []


    def addCustomer(self, date_order, name_customer, brand_car, year_car, number_car, text_order, id_act):
        try:
            self.__cur.execute("INSERT INTO log VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)",
                               (date_order, name_customer, brand_car, year_car, number_car, text_order, id_act))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    # Метод для проверки существования акта к данному заказу(если да - удаление запрещено)
    def check_delete_entry(self, entry_id):
        sql = '''SELECT id_act FROM log WHERE id = ?'''
        try:
            self.__cur.execute(sql, (entry_id,))
            result = self.__cur.fetchone()
            return result
        except Exception as e:
            print("Ошибка проверки записи:", str(e))
            return None

    # Метод для удаления записи (если не составлен акт)
    def delete_entry(self, entry_id):
        sql = '''DELETE FROM log WHERE id = ?'''
        try:
            self.__cur.execute(sql, (entry_id,))
            self.__db.commit()
        except Exception as e:
            print("Ошибка удаления из БД:", str(e))
            self.__db.rollback()


    # Метод для перехода из "Журнала" по данной записи (по entry_id)
    def get_entry(self, entry_id):
        sql = '''SELECT * FROM log WHERE id = ?'''
        try:
            self.__cur.execute(sql, (entry_id,))
            res = self.__cur.fetchone()
            if res:
                return dict(res)
        except Exception as e:
            print("Ошибка при получении записи из БД:", str(e))
        return None


    # Метод для обновления данных в Журнале
    def update_entry(self, entry_id, date_order, name_customer, brand_car, year_car, number_car, text_order, id_act):
        try:
            sql = '''UPDATE log 
                     SET date_order = ?, name_customer = ?, brand_car = ?, year_car = ?, number_car = ?, text_order = ?, id_act = ? 
                     WHERE id = ?'''
            self.__cur.execute(sql, (date_order, name_customer, brand_car, year_car, number_car, text_order, id_act, entry_id))
            self.__db.commit()
        except Exception as e:
            print("Ошибка при обновлении записи в БД:", str(e))
            self.__db.rollback()

    # Метод для добавления данных в act
    def save_new_act(self, id_act, date_act, name_work, price_work):
        sql = """
            INSERT INTO act (id_act, date_act, name_work, price_work)
            VALUES (?, ?, ?, ?)
        """
        try:
            print(
                f"Сохранение в act: id_act={id_act}, date_act={date_act}, name_work={name_work}, price_work={price_work}")
            self.__cur.execute(sql, (id_act, date_act, name_work, price_work))
            self.__db.commit()
            print(f"Данные успешно сохранены в act")
            return id_act
        except Exception as e:
            print(f"Ошибка при сохранении новых данных в БД act: {str(e)}")
            return None

    # Метод для добавления данных в stock_minus
    def save_new_stock_minus(self, name, price_unit, quantity, id_act):
        sql = """
            INSERT INTO stock_minus (name, price_unit, quantity, id_act)
            VALUES (?, ?, ?, ?)
        """
        try:
            print(
                f"Сохранение в stock_minus: name={name}, price_unit={price_unit}, quantity={quantity}, id_act={id_act}")
            self.__cur.execute(sql, (name, price_unit, quantity, id_act))
            self.__db.commit()
            print("Данные успешно сохранены в stock_minus")
        except Exception as e:
            print("Ошибка при сохранении новых данных в БД stock_minus:", str(e))

    # Метод для добавления данных в log по entry_id
    def save_id_act_to_log(self, id_act, entry_id):

        sql = """
            UPDATE log
            SET id_act = ?
            WHERE id = ?
        """
        try:
            self.__cur.execute(sql, (id_act, entry_id))
            self.__db.commit()
        except Exception as e:
            print("Ошибка при обновлении записи в таблице log:", str(e))

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
                log.number_car;'''
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
        except Exception as e:
            print(f"Ошибка чтения из БД: {e}")
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
            log.id_act = ?
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
            act.id_act = ?
        '''

        sql_materials = '''
        SELECT 
            stock_minus.name,
            stock_minus.price_unit,
            stock_minus.quantity
        FROM 
            stock_minus
        WHERE 
            stock_minus.id_act = ?
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
        except Exception as e:
            print("Ошибка при получении записи из БД:", str(e))
        return None



        # Метод для обновления данных в final act  ??????????????????

    def update_final_act(self, entry_id, date_act, name_works, price_works, names, price_units, quantities):
        try:
            self.__cur.execute("""
                UPDATE act SET name_work = ?, price_work = ?, date_act = ? WHERE id_act = ?;
            """, (name_works, price_works, date_act, entry_id))
            self.__db.commit()

            # Удаление старых записей из таблицы stock_minus для данного акта
            self.__cur.execute("""
                DELETE FROM stock_minus WHERE id_act = ?;
            """, (entry_id,))

            # Вставка новых записей в таблицу stock_minus
            for name, price_unit, quantity in zip(names, price_units, quantities):
                self.__cur.execute('''
                    INSERT INTO stock_minus (id_act, name, price_unit, quantity) VALUES (?, ?, ?, ?);
                ''', (entry_id, name, price_unit, quantity))
            self.__db.commit()

        except Exception as e:
            print("Ошибка обновления данных в БД:", str(e))
            self.__db.rollback()




        # Отображение Склада
    def getStock(self):
        sql = '''SELECT 
                 sp.name AS name_total,
                 IFNULL (sp.quantity, 0) - IFNULL (sm.quantity, 0) AS quantity_total,
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
                 ON sp.name = sm.name AND sp.price_unit = sm.price_unit;'''

        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            # Преобразование каждой строки в список значений
            stock_list = [dict(row) for row in res]
            return stock_list
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
        return []

    # Метод для добавления в stock_plus
    def addStock(self, name, quantity, price_unit):
        try:
            self.__cur.execute("""
                INSERT INTO stock_plus (name, quantity, price_unit) 
                VALUES (?, ?, ?);
                """, (name, quantity, price_unit))
            self.__db.commit()
        except sqlite3.Error as e:
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
        except:
            print("Ошибка чтения из БД")
        return []

    # Добавление сотрудника
    def addEmployees(self, name, profession):
        try:
            self.__cur.execute("INSERT INTO employees VALUES(NULL, ?, ?)", (name, profession))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    # Удаление из списка сотрудников
    def delete_entry_employees(self, entry_id):
        sql = '''DELETE FROM employees WHERE id = ?'''
        try:
            self.__cur.execute(sql, (entry_id,))
            self.__db.commit()
        except Exception as e:
            print("Ошибка удаления из БД:", str(e))
            self.__db.rollback()

   # Редактирование списка сотрудников
    def get_entry_employees(self, entry_id):
        sql = '''SELECT * FROM employees WHERE id = ?'''
        try:
            self.__cur.execute(sql, (entry_id,))
            res = self.__cur.fetchone()
            if res:
                return dict(res)
        except Exception as e:
            print("Ошибка при получении записи из БД:", str(e))
        return None

    # Метод для обновления данных о сотрудниках
    def update_entry_employees(self, entry_id, name, profession):
        try:
            sql = '''UPDATE employees
                     SET name = ?, profession = ? 
                     WHERE id = ?'''
            self.__cur.execute(sql, (name, profession, entry_id))
            self.__db.commit()
        except Exception as e:
            print("Ошибка при обновлении записи в БД:", str(e))
            self.__db.rollback()





