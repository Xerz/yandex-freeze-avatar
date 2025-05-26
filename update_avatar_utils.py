import os
from botasaurus.browser import browser, Driver
from dotenv import load_dotenv
load_dotenv()

def authorize(driver):
    #       кликаем #passp\:exp-register
    driver.click("#passp\\:exp-register")
    # кликаем #root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.passp-auth-content > div:nth-child(3) > div > div > div > div > form > div > div.layout_controls > div.passp-login-form-other-controls > div > div.AuthAddButtons-rowButtons > div > div > ul > li:nth-child(4) > button
    driver.click(
        "#root > div > div.passp-page > div.passp-flex-wrapper > div > div > div.passp-auth-content > div:nth-child(3) > div > div > div > div > form > div > div.layout_controls > div.passp-login-form-other-controls > div > div.AuthAddButtons-rowButtons > div > div > ul > li:nth-child(4) > button")
    #   ждём когда появится  #passp-field-login
    driver.wait_for_element("#passp-field-login")
    # вводим логин
    login = os.environ.get("UTMN_LOGIN")
    password = os.environ.get("UTMN_PASSWORD")
    driver.type("#passp-field-login", login)
    # кликаем на кнопку "Войти" #passp\:sign-in
    driver.click("#passp\\:sign-in")
    #     ждём #userNameInput
    driver.wait_for_element("#userNameInput")
    # вводим имя пользователя
    driver.type("#userNameInput", login)
    driver.type("#passwordInput", password)
    driver.click("#submitButton")

def update_avatar(driver):
    # ждём появления div с классом начинающимся на profile-card_avatar
    driver.wait_for_element("div[class^='profile-card_avatar__']")
    #  Кликаем
    driver.click("div[class^='profile-card_avatar__']")
    # Ждём появления div с параметром data-key="EditAvatar"
    driver.wait_for_element("div[data-key='EditAvatar']")
    # Кликаем
    driver.click("div[data-key='EditAvatar']")
    # Ждём появления img c class содержащим profile-avatar-editor-dialog_avatar__
    driver.wait_for_element("img[class*='profile-avatar-editor-dialog_avatar__']")

    img_path = os.path.join("avatars", os.environ.get("AVATAR_FILENAME", "islands-200.webp"))
    absolute_path = os.path.abspath(img_path)
    # Находим input[type=file] который внутри div с классом начинающимся на image-picker_cell__
    driver.wait_for_element("div[class^='image-picker_cell__'] input[type='file']")
    # выбираем его
    img_input = driver.select("div[class^='image-picker_cell__'] input[type='file']")
    # Вставляем в этот input путь к файлу
    img_input.upload_file(absolute_path)
    # Щёлкаем по "Готово" → div с параметром data-testid="upload-button"
    driver.click("button[data-testid='upload-button']")
    # Ищем элемент span с текстом Сохранить
    save_button = driver.get_element_with_exact_text("Сохранить")
    save_button.click()
    # ждём появления div с data-testid="snackbar-content" и span внутри. Выводим текст
    driver.wait_for_element("div[data-testid='snackbar-content'] span")
    return driver.get_text("div[data-testid='snackbar-content'] span")

@browser(max_retry=2, block_images=True, tiny_profile=True, profile='pikachu', headless=True)
def auth_and_update(driver: Driver, data):
    # driver.enable_human_mode()
    # Visit the yandex id website via Google Referrer
    driver.google_get("https://id.yandex.ru/")
    # driver.prompt()

    # Wait for the page to load and display the title
    driver.wait_for_element("title")

    title = driver.get_text("title")

    if title == "Are you not a robot?":
        print("Failed to bypass Yandex protection")
        raise Exception("Failed to bypass Yandex protection")

    if title == "Авторизация":
        authorize(driver)
        # Ждём появления div с data-testid="profile-card-avatar"
        driver.wait_for_page_to_be("https://id.yandex.ru/")
        title = driver.get_text("title")

    if title == "Яндекс ID":
        update_avatar(driver)
        # driver.close()
        return
    else:
        raise Exception(f"Unexpected title: {title}")
