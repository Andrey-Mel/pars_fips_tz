import os
import json
import time
import httplib2

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class Fips_parser(object):

    def __init__(self, vis, mkty, period,folder):
        """
        :param vis,mkty,period:
        """
        self.vis = vis
        self.mkty = mkty
        self.period = period
        self.folder = folder

    def visual_for_sel(self,vis):
        """
        функция показывает или нет ход отображения работы в браузере
        :param vis:
        :return:self.driver
        """
        self.url = "https://www1.fips.ru/iiss/"
        if self.vis == '1':
            self.driver = webdriver.Chrome("/Users/macbook/PycharmProjects/test_task_for_Maxim/chromedriver")

        elif self.vis == '0':
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome("/Users/macbook/PycharmProjects/test_task_for_Maxim/chromedriver", options=chrome_options)

        else:
            print("Вы неправильно ввели значение")
        return self.driver


    def parse(self):
        """
        Функция объеденяющая все запуски функций парсера
        :return:
        """
        self.go_to_page_fips()
        self.goon_on_params()
        self.find_needs_tm()
        self.items_count_tm()
        self.data_collecting_tm()

    def go_to_page_fips(self):
        """
        Переход на сайт fips.ru, согласно заданию
        :return:
        """
        self.driver = self.visual_for_sel(self.vis)
        self.driver.get(self.url)


    def goon_on_params(self):
        """
        Переход по заданым параметрам согласно заданию
        :return:
        """
        # выбираем "российские товарные знаки"
        elem_id_tz = self.driver.find_element_by_id("db-selection-form:j_idt134")
        elem_id_tz.click()

        # Находим и нажимаем checkbox " из последних двух бюлетней", но он нажат по умолчанию
        check_btn = self.driver.find_element_by_xpath('//*[@id="db-selection-form:dbsGrid4:0:dbsGrid4checkbox"]')
        check_btn.is_selected()

        # Находим и нажимаем тег input "Перейти к поиску"
        btn_go_find = self.driver.find_element_by_tag_name("input")
        btn_go_find.submit()
        self.driver.get(self.url + "search.xhtml")
        time.sleep(2)


    def find_needs_tm(self):
        """
        Функция отбора торговых марок по заданым данным
        :return:
        """
        elem_mkty = self.driver.find_element_by_id("fields:6:j_idt109")
        elem_mkty.send_keys(self.mkty)  # вход mkty

        # find element "дата регистрации" по id

        elem_date = self.driver.find_element_by_id("fields:7:j_idt109")
        elem_date.is_enabled()
        elem_date.send_keys(self.period)  # вход period

        # find elem "статус документа" и отметить его "Действующий"
        elem_status_work = self.driver.find_element_by_id("fields:21:j_idt113:1:j_idt115")
        elem_status_work.click()

        # find кнопку поиск и нажать ее

        btn_search = self.driver.find_element_by_name("j_idt128")
        btn_search.click()



    def items_count_tm(self):
        """
        Возвращает количество найденных торговых марок count_tm
        :param:
        :return: count_tm
        """
        self.count_tm = self.driver.find_element_by_class_name("bigtit").text
        self.count_tm = int(self.count_tm.split(" ")[-1])  # Количество торговых знаков
        #print("Найдено количество торговых марок:", self.count_tm)

        return self.count_tm



    def data_collecting_tm(self):
        """
        функция отбора торговых знаков и описания их по заданым данным
        из условия задания и сохраняет изображения и описание их в файлы в папку Data
        :return:

        """
        try:
            self.count = self.items_count_tm()
            print("Найдено количество торговых марок:", self.count)
            print("Это займет какое-то время!!!")
            time.sleep(3)
            self.items = self.driver.find_elements_by_class_name("tr")
            self.items[0].click()
            # print(self.count)
            #folder = input("Введите название каталога куда сохранять данные: ")
            os.mkdir(f"{self.folder}")
            for i in range(1, self.count+1):

                os.mkdir(f"{self.folder}/tr_mark_{i}")
                #-----------Получение ссылки на страницу тм------------------------------
                try:
                    self.get_link_tm = self.driver.current_url
                    #print("Ссылка текущей торговой марки", get_link_tm)
                    print(f"Ссылка на ТЗ : {self.get_link_tm}")#####

                except NoSuchElementException:
                    print("Нет ссылки на отсортированные тз")

                #-------------------Изображение  !!!---------------
                try:
                    print("URL изображения: ")
                    xpath = '/html/body/div[3]/div/div/div[1]/div[2]/form/div/div/div[2]/div/div/p[1]/a/img'
                    box_img = self.driver.find_element_by_xpath(xpath)
                    url = box_img.get_attribute('src') #ссылка на получение изображения
                    print("URL изображения: ",url)


                    h = httplib2.Http(f'.cache')
                    response, content = h.request(url)

                    with open(f"{self.folder}/tr_mark_{i}/img_tr_mark.jpg",'wb') as file:
                        file.write(content)
                except NoSuchElementException:
                    print("Нет элемента изображения")

                #---------------Нужно получить информацию правообладателя---------------
                try:

                    self.copyright_holder = self.driver.find_element_by_xpath("/html/body/div[3]/div/div/div[1]/div[2]/form/div/div/div[2]/div/div/p[2]/b").text
                    if self.copyright_holder is not None:
                        print(f'Информация о правообладателе:\n {self.copyright_holder}')

                except NoSuchElementException:
                    print("Нет элемента о правообладателе")

                #---Получить дату регистрации-----------
                try:
                    #print("Регистрация")
                    self.reg_date = self.driver.find_element_by_id("BibR").text
                    self.reg_date = self.reg_date.split('\n')[2]
                    print("Регистрация: ",self.reg_date)

                except NoSuchElementException:
                    print('Нет элемента даты регистрации')

                #---Получить все МКТУ правообладателя--------
                try:
                    self.all_mkty = self.driver.find_element_by_id("mainDoc2").find_elements_by_class_name("bib")
                    self.mkty = self.all_mkty[-1].text

                except NoSuchElementException:
                    print('Нет элемента мкту')

                #----Создаю словарь с данными для сохранения в файл--
                info_about_trade_mark = []
                info_about_trade_mark.append(
                    {
                        "Ссылка на ТМ": self.get_link_tm,
                        "Дата регистрации (split)":self.reg_date,
                        "Правообладатель": self.copyright_holder,
                        "МКТУ": self.mkty
                    }
                )
                #---Создаем текст файл и сохраняем данные в него

                with open(f"{self.folder}/tr_mark_{i}/info.txt", 'a') as file:
                    json.dump(info_about_trade_mark,  file, indent=4, ensure_ascii=False)


                # for i in range(2):
                #     self.driver.find_element_by_id("j_idt71:j_idt108").click()
                self.driver.get(f'https://www1.fips.ru/iiss/document.xhtml?index={i + 1}')

                if self.count == self.count:
                    print("Отбор торговых знаков закончился")

        except Exception as ex:
            print(ex)
            print("Нет торговых знаков")

        finally:
            self.driver.close()







