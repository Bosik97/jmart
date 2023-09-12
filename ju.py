import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import colorama
from colorama import Fore
import pandas as pd

# Инициализация colorama
colorama.init()

# Путь к geckodriver
path_to_geckodriver = 'C:\\Users\\byedil\\Desktop\\vgr\\geckodriver.exe'

# CSS-селектор целевого элемента
target_element_selector = "#main_body > div > div.Row--fpkawn.ceBnoU > div.Col--1enwmnn.duZPYR > div.StyledBox--1stdqie.fCiATz > div.StyledBox--1stdqie.StyledFlexBox--14yxo3s.iSAORq.geRqVF > div:nth-child(1) > div > div.StyledBox--1stdqie.StyledFlexBox--14yxo3s.cMtUGn.hYwjyG > div:nth-child(2) > button"

# Путь к файлу Excel с ссылками
excel_file_path = 'links.xlsx'

# Создание экземпляра сервиса GeckoDriver
service = Service(path_to_geckodriver)

# Создание экземпляра опций Firefox
options = Options()
options.add_argument('-headless')  # Запуск браузера в фоновом режиме

# Создание экземпляра веб-драйвера Firefox
driver = webdriver.Firefox(service=service, options=options)

# Функция для вывода строки в красном цвете
def print_red(*args):
    print(Fore.RED + ' '.join(map(str, args)) + Fore.RESET)

# Сохранение ссылок с уведомлениями в Excel файл
def save_notification_links(links):
    data = {'Ссылка': links}
    df = pd.DataFrame(data)
    df.to_excel('notification_links.xlsx', index=False)

# Чтение ссылок из файла Excel
df = pd.read_excel(excel_file_path)
links = df['Ссылка'].tolist()
notification_links = []

for link in links:
    # Установка неявного ожидания в течение 15 секунд
    driver.implicitly_wait(15)

    # Открытие веб-страницы
    driver.get(link)

    # Проверка наличия элемента на веб-странице
    target_element = driver.find_elements(By.CSS_SELECTOR, target_element_selector)
    if target_element:
        print("Ссылка:", link)
        print("Элемент найден!")
        print("Текст элемента:", target_element[0].text)
    else:
        if link not in notification_links:
            print_red("Ссылка:", link)
            print_red("Уведомление: Элемент пропал!")
            notification_links.append(link)

# Сохранение ссылок с уведомлениями в Excel файл
if notification_links:
    save_notification_links(notification_links)

# Вывод надписи "Завершено!" выделенной зеленым цветом
print(Fore.GREEN + "Завершено!")

# Ожидание ввода для завершения программы
input("Нажмите Enter для выхода...")
