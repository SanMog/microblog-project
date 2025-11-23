# tests/blog_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BlogPage:
    """
    Page Object для главной страницы микроблога.
    """
    # Указываем URL нашего приложения.
    # Мы используем host 'web', т.к. тесты тоже будут запускаться в Docker.
    # Для локального запуска мы будем его подменять.
    URL = 'http://web:5000'

    def __init__(self, driver: WebDriver):
        self.driver = driver

        # --- Локаторы ---
        self.CONTENT_TEXTAREA = (By.NAME, 'content')
        self.SUBMIT_BUTTON = (By.CSS_SELECTOR, 'input[type="submit"]')
        # Локатор для всех постов на странице
        self.POSTS_LIST = (By.CLASS_NAME, 'post')

    def load(self):
        """Открывает страницу микроблога в браузере."""
        self.driver.get(self.URL)
        return self

    def add_post(self, text: str):
        self.driver.find_element(*self.CONTENT_TEXTAREA).send_keys(text)
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

        # ДОБАВЬТЕ ЭТО ОЖИДАНИЕ:
        # Ждем (максимум 5 секунд), пока на странице не появится
        # хотя бы один видимый элемент, который соответствует локатору POSTS_LIST.
        # Это гарантирует, что страница перезагрузилась, и посты на ней отрисовались.
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.POSTS_LIST)
        )

    def get_posts_text(self) -> list[str]:
        """
        Находит все элементы постов на странице и возвращает их текст.
        """
        post_elements = self.driver.find_elements(*self.POSTS_LIST)
        # Из каждого веб-элемента достаем его текстовое содержимое
        return [element.text for element in post_elements]