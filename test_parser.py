# import os
# import json
import time
from datetime import datetime
# import httplib2
#
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import NoSuchElementException
from parser_tm import Fips_parser




print("Ввод данных по которому нужно отфильтровать торговые знаки")


def check_mkty(m):
    """
    Функция проверки ввода правильности mkty
    :param m:
    :return: m
    """
    while True:
        try:
            if (m <= 45):
                print("Ok")
                return m
                break
            else:
                m = int(input("Введите MKTY от 1 до 45 включительно: "))
                continue
        except ValueError:
            m = int(input("Это не число. Введите число: "))
            break




def check_date(date):
    """
    Функция проверки правильности ввода даты
    :param date:
    :return: date
    """
    # проверка формата даты
    get_date = lambda d: datetime.strptime(d, '%Y.%m.%d').date() <= datetime.today().date()
    ex = False
    while ex != True:
        try:
            if get_date(date) != True:
                print(f"Вы неправильно ввели дату {date} Введите заново")
                date = input("Введите заново и нажмите ENTER: ")

            else:
                print("Ok ")
                ex = True
                return date
        except ValueError:
                date = input("Введите заново и нажмите ENTER: ")




vis = input("Введите 1 - если хотите видеть работу браузера, и 0 - если не хотите видеть работу браузера ->  ")
folder = input("Введите название каталога куда сохранять данные: ")
mkty = int(input("Введите интересуещее Вас МКТУ и нажмите ENTER: "))
check_mkty(mkty)

start = input("Введите начало периода (в формате год.месяц.чило) и нажмите ENTER: ")
start = check_date(start)

end = input("Введите конец периода (в формате год.месяц.чило) и нажмите ENTER: ")
end = check_date(end)
while True:
    if end < start:
        print("Вы ввели конец периода по дате меньше чем начало периода")
        end = input("Введите конец периода повторно (в формате год.месяц.чило) и нажмите ENTER: ")
        end = check_date(end)
    else:
        print("Oтлично")
        break

period = start + "-" + end


parser = Fips_parser(vis, mkty, period,folder)
parser.parse()