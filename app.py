# app.py

import os
import time
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    """Устанавливает соединение с базой данных."""
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host="db",
                database=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD")
            )
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            print("Не удалось подключиться к БД, пробую еще раз...")
            time.sleep(5)
    raise Exception("Не удалось подключиться к базе данных.")

# Этот маршрут теперь обрабатывает и GET, и POST запросы
@app.route('/', methods=('GET', 'POST'))
def index():
    # Если пользователь отправил форму (POST-запрос)
    if request.method == 'POST':
        # Получаем текст поста из формы
        content = request.form['content']
        if content: # Проверяем, что пост не пустой
            conn = get_db_connection()
            cur = conn.cursor()
            # Выполняем SQL-запрос для вставки нового поста
            cur.execute('INSERT INTO posts (content) VALUES (%s)', (content,))
            conn.commit() # Фиксируем транзакцию
            cur.close()
            conn.close()
        # Перенаправляем пользователя обратно на главную страницу,
        # чтобы он увидел обновленный список постов.
        return redirect(url_for('index'))

    # Если пользователь просто открыл страницу (GET-запрос)
    conn = get_db_connection()
    cur = conn.cursor()
    # Выполняем SQL-запрос для получения всех постов, сортируя по дате
    cur.execute('SELECT content, created_at FROM posts ORDER BY created_at DESC;')
    posts = cur.fetchall() # Забираем все результаты
    cur.close()
    conn.close()

    # "Рисуем" HTML-страницу, передавая в нее список постов
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)