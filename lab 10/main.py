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
5. Выйти''')

    a = input("Выберите вариант: ")

    if a == "1":
        name = input("Имя: ")
        phone = input("Телефон: ")
        email = input("Почта: ")
        notes = input("Заметка: ")

        cur.execute("""
            INSERT INTO contacts (name, phone, email, notes)
            VALUES (%s, %s, %s, %s)
        """, (name, phone, email, notes))
        conn.commit()
        print("✅ Контакт добавлен.")

    elif a == "2":
        contact_id = input("ID контакта, которого хотите изменить: ")
        name = input("Новое имя: ")
        phone = input("Новый телефон: ")
        email = input("Новая почта: ")
        notes = input("Новая заметка: ")

        cur.execute("""
            UPDATE contacts
            SET name=%s, phone=%s, email=%s, notes=%s
            WHERE id=%s
        """, (name, phone, email, notes, contact_id))
        conn.commit()
        print("Контакт обновлён.")

    elif a == "3":
        cur.execute("SELECT * FROM contacts")
        rows = cur.fetchall()

        print("\nСписок контактов:")
        for row in rows:
            print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}, Почта: {row[3]}, Заметка: {row[4]}")
        if not rows:
            print("Контактов нет.")

    elif a == "4":
        contact_id = input("Введите ID контакта для удаления: ")
        cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
        conn.commit()
        print(" Контакт удалён.")

    elif a == "5":
        run = False
        print("Выход")

    else:
        print("Неверный выбор. Попробуйте снова.")
    
# cur.execute('''
#     INSERT INTO contacts (name, phone, email, notes)
#     Values(%s, %s, %s, %s)
            
        
# ''', ("Ayazhan", "+77086695049", "ayazhan@mail.ru", "My bestie"))

conn.commit()
cur.close()
conn.close()
