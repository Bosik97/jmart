import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import tkinter as tk
from threading import Thread
from tkinter import messagebox


# Путь к geckodriver
path_to_geckodriver = 'C:\\Users\\byedil\\Desktop\\vgr\\geckodriver.exe'

# Дефолтный CSS-селектор целевого элемента
default_target_element_selector = "#main_body > div > div.Row--fpkawn.ceBnoU > div.Col--1enwmnn.duZPYR > div.StyledBox--1stdqie.fCiATz > div.StyledBox--1stdqie.StyledFlexBox--14yxo3s.iSAORq.geRqVF > div:nth-child(1) > div > div.StyledBox--1stdqie.StyledFlexBox--14yxo3s.cMtUGn.hYwjyG > div:nth-child(2) > button"

# Список ссылок для мониторинга
links = []

# Создание экземпляра сервиса GeckoDriver
service = Service(path_to_geckodriver)

# Создание экземпляра опций Firefox
options = Options()
options.add_argument('-headless')  # Запуск браузера в фоновом режиме

# Создание экземпляра веб-драйвера Firefox
driver = webdriver.Firefox(service=service, options=options)


def monitor_links():
    # Бесконечный цикл мониторинга
    while True:
        # Установка неявного ожидания в течение 15 секунд
        driver.implicitly_wait(15)

        # Перебор ссылок
        for link in links:
            # Открытие веб-страницы
            driver.get(link)

            # Проверка наличия элемента на веб-странице
            target_element = driver.find_elements(By.CSS_SELECTOR, default_target_element_selector)
            if target_element:
                print("Элемент найден на странице:", link)
                print("Текст элемента:", target_element[0].text)
            else:
                print("Элемент не найден на странице:", link)

                # Отображение уведомления в окне
                messagebox.showwarning("Уведомление", f"Элемент пропал на странице: {link}")

        # Пауза в 1 минуту перед следующей проверкой
        time.sleep(60)


def add_link():
    link = entry.get()
    links.append(link)
    entry.delete(0, tk.END)


def start_monitoring():
    # Запуск мониторинга в отдельном потоке
    thread = Thread(target=monitor_links)
    thread.start()


# Создание графического окна
root = tk.Tk()
root.title("Мониторинг ссылок")

# Добавление элементов интерфейса
label = tk.Label(root, text="Введите ссылку:")
label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

add_button = tk.Button(root, text="Добавить ссылку", command=add_link)
add_button.pack()

start_button = tk.Button(root, text="Начать мониторинг", command=start_monitoring)
start_button.pack()

close_button = tk.Button(root, text="Закрыть", command=root.destroy)
close_button.pack()

# Запуск главного цикла обработки событий
root.mainloop()
