import psycopg2

conn = psycopg2.connect(
    dbname="phone_numbers",
    user="postgres",
    password="adeliya",
    host="localhost",
    port="5432"
)

cur = conn.cursor()


cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        last_name VARCHAR(100),
        name VARCHAR(100),
        phone VARCHAR(20),
        email VARCHAR(100),
        notes TEXT
    )
""")

run = True

while run:
    print("Что хотите сделать?")
    print('''1. Добавить контакт
2. Изменить контакт
3. Посмотреть все контакты
4. Удалить контакт
5. Показать контакт
6. Добавление нового пользователя по имени и фамилии
7. Добавить несколько контактов
8. Показать контакты постранично
9. Выйти
''')

    a = input("Выберите вариант: ")

    if a == "1":
        last_name = input("Фамилия: ")
        name = input("Имя: ")
        phone = input("Телефон: ")
        email = input("Почта: ")
        notes = input("Заметка: ")

        cur.execute("""
            INSERT INTO contacts (last_name, name, phone, email, notes)
            VALUES (%s, %s, %s, %s, %s)
        """, (last_name, name, phone, email, notes))
        conn.commit()
        print("✅ Контакт добавлен.")

    elif a == "2":
        contact_id = input("ID контакта, которого хотите изменить: ")
        last_name = input("Новая фамилия: ")
        name = input("Новое имя: ")
        phone = input("Новый телефон: ")
        email = input("Новая почта: ")
        notes = input("Новая заметка: ")

        cur.execute("""
            UPDATE contacts
            SET last_name=%s, name=%s, phone=%s, email=%s, notes=%s
            WHERE id=%s
        """, (last_name, name, phone, email, notes, contact_id))
        conn.commit()
        print("Контакт обновлён.")

    elif a == "3":
        cur.execute("SELECT * FROM contacts")
        rows = cur.fetchall()

        print("\nСписок контактов:")
        for row in rows:
            print(f"ID: {row[0]}, Фамилия: {row[1]}, Имя: {row[2]}, Телефон: {row[3]}, Почта: {row[4]}, Заметка: {row[5]}")
        if not rows:
            print("Контактов нет.")

    elif a == "4":
        choice = input("Удалить по:\n1 — Имени\n2 — ID\n3 — Номеру телефона\nВыберите (1/2/3): ")

        if choice == "1":
            name = input("Введите имя: ")
            cur.execute("SELECT * FROM contacts WHERE name = %s", (name,))
            rows = cur.fetchall()
            if not rows:
                print("Контакты не найдены.")
            else:
                for row in rows:
                    print(f"ID: {row[0]}, {row[2]} {row[1]}, Телефон: {row[3]}")
                confirm = input("Удалить все эти контакты? (да/нет): ").lower()
                if confirm == "да":
                    cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
                    conn.commit()
                    print("Контакты удалены.")
                else:
                    print("Удаление отменено.")

        elif choice == "2":
            contact_id = input("Введите ID контакта: ")
            cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
            conn.commit()
            print("Контакт удалён.")

        elif choice == "3":
            phone = input("Введите номер телефона: ")
            cur.execute("SELECT * FROM contacts WHERE phone = %s", (phone,))
            rows = cur.fetchall()
            if not rows:
                print("Контакты не найдены.")
            else:
                for row in rows:
                    print(f"ID: {row[0]}, {row[2]} {row[1]}, Телефон: {row[3]}")
                confirm = input("Удалить контакт с этим номером? (да/нет): ").lower()
                if confirm == "да":
                    cur.execute("DELETE FROM contacts WHERE phone = %s", (phone,))
                    conn.commit()
                    print("Контакт удалён.")
                else:
                    print("Удаление отменено.")
        
        else:
            print("Неверный выбор.")


    elif a == "5":
        
        contact_id = input("Введите ID контакта для просмотра: ")
        cur.execute('''SELECT * FROM contacts
                    WHERE id=%s''', (contact_id, ))
        rows = cur.fetchall()
        print("Что хотите посмотреть?")
        print('''1. Фамилию и имя
2. Имя и телефон
3. Имя и почту
4. Имя и запись
              ''')
        contact_e = input(": ")
        for row in rows:
            user_id = row[0]
            last_name = row[1]
            name = row[2]
            phone = row[3]
            email = row[4]
            zapis = row[5]
        if contact_e == "1":
            print(f"{last_name} — {name}")
        elif contact_e == "2":
            print(f"{name} — {phone}")
        elif contact_e == "3":
            print(f"{name} — {email}")
        elif contact_e == "4":
            print(f"{name} — {zapis}")
        else:
            print("Такого запроса не существует.")
    elif a == "6":
        contact_name = int(input("Какого пользователя вы хотите добавить?(имя):"))
        cur.execute('''SELECT * FROM contacts WHERE name=%s''', (contact_name, ))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(f"ID: {row[0]}, Фамилия: {row[1]}, Имя: {row[2]}, Телефон: {row[3]}, Почта: {row[4]}, Заметка: {row[5]}")
            
            print("Что хотите сделать?")
            print('''1. Изменить контакт
        2. Выйти''')

            choice = input("Выберите: ")

            if choice == "1":
                contact_id = input("Введите ID контакта для изменения: ")
                new_phone = input("Новый телефон: ")
                cur.execute("UPDATE contacts SET phone = %s WHERE id = %s", (new_phone, contact_id))
                conn.commit()
                print("Телефон обновлён.")
            elif choice == "2":
                print("Возврат в меню.")
            else:
                print("Неверный выбор.")
        else:
            print("Контакты не найдены.")
    elif a == "7":
        coount = input("Сколько контактов хотите добавить?: ")
        for i in range(coount):
            print(f"\nКонтакт {i+1}:")

            last_name = input("Фамилия: ")
            name = input("Имя: ")
            phone = input("Телефон: ")
            email = input("Почта: ")
            notes = input("Заметка: ")

            cur.execute("""
                INSERT INTO contacts (last_name, name, phone, email, notes)
                VALUES (%s, %s, %s, %s, %s)
            """, (last_name, name, phone, email, notes))
            conn.commit()
            print("✅ Контакт добавлен.")
    elif a == "8":
        page_size = 5
        page = 0

        while True:
            offset = page * page_size
            cur.execute("""
                SELECT * FROM contacts
                ORDER BY id
                LIMIT %s OFFSET %s
            """, (page_size, offset))
            rows = cur.fetchall()

            if not rows:
                print("Нет данных для отображения.")
                break

            print(f"\nСтраница {page + 1}")
            for row in rows:
                print(f"ID: {row[0]}, Фамилия: {row[1]}, Имя: {row[2]}, Телефон: {row[3]}, Почта: {row[4]}, Заметка: {row[5]}")

            print("\nКоманды: [n]ext — следующая, [p]revious — предыдущая, [q]uit — выход")
            cmd = input("Выберите: ").lower()

            if cmd == "n":
                page += 1
            elif cmd == "p" and page > 0:
                page -= 1
            elif cmd == "q":
                break
            else:
                print("Неверная команда.")

    elif a == "9":
        run = False
        print("Выход")

    else:
        print("Неверный выбор. Попробуйте снова.")
    
# cur.execute('''
#     INSERT INTO contacts (last_name, name, phone, email, notes)
#     Values(%s, %s, %s, %s, %s)
            
        
# ''', ("Azamatkyzy", "Ayazhan", "+77086695049", "ayazhan@mail.ru", "My bestie"))

conn.commit()
cur.close()
conn.close()
