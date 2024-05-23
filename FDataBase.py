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


    def delete_entry(self, entry_id):
        sql = '''DELETE FROM log WHERE id = ?'''
        try:
            self.__cur.execute(sql, (entry_id,))
            self.__db.commit()
        except Exception as e:
            print("Ошибка удаления из БД:", str(e))
            self.__db.rollback()


    # Метод для получения entry_id для перехода из "Журнала" по данной записи
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

    # Метод для добавления данных в act вып работ
    def save_new_act(self, date_act, name_work, price_work):
        sql = """
            INSERT INTO act (date_act, name_work, price_work)
            VALUES (?, ?, ?)
        """
        try:
            self.__cur.execute(sql, (date_act, name_work, price_work))
            self.__db.commit()
            return self.__cur.lastrowid  # Возвращаем ID нового акта
        except Exception as e:
            print("Ошибка при сохранении новых данных в БД:", str(e))
            return None

    # Метод для добавления данных в stock_minus через акт вып работ
    def save_new_stock_minus(self, name, price_unit, quantity, id_act):
        sql = """
            INSERT INTO stock_minus (name, price_unit, quantity, id_act)
            VALUES (?, ?, ?, ?)
        """
        try:
            self.__cur.execute(sql, (name, price_unit, quantity, id_act))
            self.__db.commit()
        except Exception as e:
            print("Ошибка при сохранении новых данных в БД:", str(e))

    # Метод для добавления номера акта в Журнал
    def save_id_act_to_log(self, entry_id, id_act):
        # Получаем текущую запись по entry_id
        entry = self.get_entry(entry_id)

        if entry:
            # Дополняем текущую запись id_act и обновляем её
            id_act_old = entry.get('id_act')
            if id_act_old is not None:
                id_act_new = f"{id_act_old} {id_act}"
            else:
                id_act_new = str(id_act)

            sql_update = """
                UPDATE log
                SET id_act = ?
                WHERE id = ?
            """
            try:
                self.__cur.execute(sql_update, (id_act_new, entry_id))
                self.__db.commit()
                print(f"ID акта {id_act} успешно добавлен к записи в таблице log с id {entry_id}")
            except Exception as e:
                print("Ошибка при обновлении записи в таблице log:", str(e))
        else:
            print(f"Запись с id {entry_id} не найдена в таблице log")


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

    '''
# Добавление данных в акт вып работ

    def addAct_foreign_key_db(self, data_order, data_act, number_car, form):
        #print(f"data_order: {data_order}, data_act: {data_act}, number_car: {number_car}, form: {form}")
        try:
            # Добавление данных в таблицу act_foreign_key
            self.__cur.execute("INSERT INTO act_foreign_key (data_order, data_act, number_car) VALUES (?, ?, ?)",
                               (data_order, data_act, number_car))

            # Получение автоматически сгенерированного act_id
            act_id = self.__cur.lastrowid

            for row_data in form:
                materials = row_data['materials'][0]
                price_materials = row_data['price_materials'][0]
                quantity = row_data['quantity'][0]
                work_completed = row_data['work_completed'][0]
                name_work = row_data['name_work'][0]
                price_work = row_data['price_work'][0]

                sql_act_materials = "INSERT INTO act_materials (act_id, materials, price_materials, quantity) VALUES (?, ?, ?, ?)"
                self.__cur.execute(sql_act_materials, (act_id, materials, price_materials, quantity))

                sql_stock_minus = "INSERT INTO stock_minus (name, price_unit, quantity) VALUES (?, ?, ?)"
                #print('ACT sql_stock_minus, (materials, price_materials, quantity)', materials, price_materials, quantity)
                #print('STOCK stock_minus (name, price_unit, quantity)', materials, price_materials, quantity)
                self.__cur.execute(sql_stock_minus, (materials, price_materials, quantity))

                sql_act_work = "INSERT INTO act_work (act_id, work_completed, name_work, price_work) VALUES (?, ?, ?, ?)"
                self.__cur.execute(sql_act_work, (act_id, work_completed, name_work, price_work))

            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка добавления данных в БД: {str(e)}")
            self.__db.rollback()
            raise Exception(f"Ошибка добавления данных в БД: {str(e)}")
    
'''