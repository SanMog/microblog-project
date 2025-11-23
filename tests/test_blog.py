# tests/test_blog.py

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime

# Импортируем наш Page Object
from microblog.tests.blog_page import BlogPage


@pytest.fixture
def driver():
    """Наша знакомая фикстура для подготовки браузера."""
    chrome_options = Options()
    # Для локального запуска можно закомментировать --headless, чтобы видеть браузер.
    # Для CI/CD и Docker эта опция обязательна.
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()


def test_add_new_post(driver):
    """
    E2E Тест:
    1. Открывает сайт.
    2. Добавляет новый пост с уникальным текстом.
    3. Проверяет, что этот пост появился вверху списка.
    """
    blog_page = BlogPage(driver)

    # !!! КЛЮЧЕВОЙ МОМЕНТ !!!
    # В Page Object у нас URL 'http://web:5000' - это для Docker-сети.
    # Когда мы запускаем тест локально, наш сайт доступен на localhost.
    # Поэтому мы "на лету" подменяем URL для этого конкретного теста.
    blog_page.URL = 'http://localhost:5000'

    # Шаг 1: Открыть страницу
    blog_page.load()

    # Шаг 2: Сгенерировать уникальный текст, чтобы тест не зависел от предыдущих запусков
    post_text = f"Тестовый пост от {datetime.now()}"

    # Шаг 3: Добавить пост, используя метод из Page Object
    blog_page.add_post(post_text)

    # Шаг 4: Получить тексты всех постов на странице
    posts_on_page = blog_page.get_posts_text()

    # Шаг 5: Проверка (Assertion)
    # Убеждаемся, что на странице есть хотя бы один пост
    assert len(posts_on_page) > 0

    # Убеждаемся, что текст нашего нового поста (который должен быть первым в списке)
    # СОДЕРЖИТСЯ в тексте первого поста на странице.
    # Мы используем 'in', а не '==', потому что на странице к тексту поста добавляется дата.
    assert post_text in posts_on_page[0]