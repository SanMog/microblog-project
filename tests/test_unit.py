# tests/test_unit.py

import pytest
from microblog.app import app
import datetime


# Мы используем специальную фикстуру 'mocker', которую предоставляет pytest-mock
def test_index_no_posts(mocker):
    """
    GIVEN: Наше Flask-приложение
    WHEN: Мы делаем GET-запрос на главную страницу, и база данных пуста
    THEN: Мы должны увидеть сообщение "Здесь пока нет ни одного поста"
    """

    # --- ARRANGE (Подготовка) ---
    # Создаем фейковые объекты, которые будут имитировать соединение и курсор
    mock_cursor = mocker.MagicMock()
    mock_cursor.fetchall.return_value = []  # Говорим, что fetchall() вернет ПУСТОЙ список

    mock_conn = mocker.MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # САМАЯ ГЛАВНАЯ МАГИЯ: мы "патчим" (подменяем) функцию get_db_connection
    # Теперь, когда app.py вызовет get_db_connection, на самом деле вызовется
    # наш фейковый mock_conn.
    mocker.patch('microblog.app.get_db_connection', return_value=mock_conn)

    # Создаем тестовый клиент Flask. Это имитация браузера.
    test_client = app.test_client()

    # --- ACT (Действие) ---
    # Выполняем GET-запрос на главную страницу
    response = test_client.get('/')

    # --- ASSERT (Проверка) ---
    # Проверяем, что запрос прошел успешно (код 200)
    assert response.status_code == 200
    # Проверяем, что в полученном HTML-коде есть нужный нам текст
    # response.data - это тело ответа в байтах, поэтому его нужно декодировать
    # Декодируем байты в строку и сравниваем со строкой
    assert "Здесь пока нет ни одного поста" in response.data.decode('utf-8')


def test_index_with_posts(mocker):
    """
    GIVEN: Наше Flask-приложение
    WHEN: Мы делаем GET-запрос на главную страницу, и в базе есть посты
    THEN: Мы должны увидеть тексты этих постов
    """

    # --- ARRANGE (Подготовка) ---
    # Готовим фейковые данные, которые "вернет" наша фейковая база
    # Добавляем фейковую дату вторым элементом
    fake_posts = [
        ('Это первый пост', datetime.datetime.now()),
        ('Это второй пост', datetime.datetime.now())
    ]

    mock_cursor = mocker.MagicMock()
    mock_cursor.fetchall.return_value = fake_posts  # На этот раз fetchall() вернет наши данные

    mock_conn = mocker.MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mocker.patch('microblog.app.get_db_connection', return_value=mock_conn)

    test_client = app.test_client()

    # --- ACT (Действие) ---
    response = test_client.get('/')

    # --- ASSERT (Проверка) ---
    assert response.status_code == 200
    # Проверяем, что оба наших поста отобразились на странице
    # Точно так же, декодируем и сравниваем
    response_text = response.data.decode('utf-8')
    assert "Это первый пост" in response_text
    assert "Это второй пост" in response_text