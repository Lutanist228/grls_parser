# АВТОР СКРИПТА: Александр Самохин. 
# СОАВТОРЫ СКРИПТА: нету

#_________________________________________________________________________________________________________________
# Блок импорта необходимых библиотек
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time 
import sqlite3
import sys 
sys.path.append(r"C:\Users\user\Desktop\IT-Project\ProjectsPC\SPR_Project\Mnn_dict_files")
from mnn_dict_res import global_dict 

#_________________________________________________________________________________________________________________
# Блок подключения к сайту-реестру grls и задания основных значений 

URL = r"https://grls.rosminzdrav.ru/GRLS.aspx"
chromedriver_autoinstaller.install()
opt = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=opt)
opt.add_experimental_option('excludeSwitches', ['enable-logging'])
driver.get(URL)
time_val = 1
sec = 1
data_find = ""

#_________________________________________________________________________________________________________________
# Этот блок работает с БД

def table_create():
    # создается таблица, в которую помещаются лекарства и их характеристики 

    try:
        with sqlite3.connect(r"C:\Users\user\Desktop\IT-Project\ProjectsPC\SPR_Project\Tables\grls\grls_upd.db") as db:
            sql = db.cursor()
            sql.execute("""CREATE TABLE IF NOT EXISTS grls_drugs_upd ( 
                "Trade_name_rus" TEXT, 
                "Registrator_tran" TEXT,
                "Registrator_country" TEXT,
                "Producer_tran" TEXT,
                "Producer_country" TEXT,
                "Dosage_form_full_name" TEXT,
                "Dose" TEXT,
                "Sc_name" TEXT,
                "Recipe_status" TEXT,
                "As_name_rus" TEXT,
                num INTEGER)""") # в таблицу добавляются основные столбцы-фильтры: уникальный id;
            # Trade_name_rus; название компании; страна производителя;
            # форма принятия препарата; Dose препарата (в будущем возможны дополнения по столбцам)
    except:
        print("Error occured while creating the table.")
        k = input("Print any key to exit...")

    print(f"Table grls_drugs has been successfully created.\n\n")

def table_add(list_of_information, trade_name):
# принимат в себя список (type = list) информации, выгружаяя её в таблицу. А так же принимает trade_name - торговое наименование
# и название таблицы table_name для подключения к ней 
 
    with sqlite3.connect(r"C:\Users\user\Desktop\IT-Project\ProjectsPC\SPR_Project\Tables\grls\grls_upd.db") as db:
        sql = db.cursor()

        # try:
        sql.execute(f'''INSERT INTO grls_drugs_upd ("Trade_name_rus", "Registrator_tran", "Registrator_country", 
                "Producer_tran", "Producer_country", "Dosage_form_full_name", "Dose", 
                "Sc_name", "Recipe_status", "As_name_rus", "num") VALUES 
                ("{trade_name}", "{list_of_information[1]}", "{list_of_information[2]}", "{list_of_information[3]}", 
                "{list_of_information[4]}", "{list_of_information[5]}", "{list_of_information[6]}", "{list_of_information[7]}", 
                "{list_of_information[8]}", "{list_of_information[9]}", {list_of_information[0]})''') 
                
                # данная функция помещает в созданную таблицу значения-характеристики 

#_________________________________________________________________________________________________________________
# Начало парсинг-блока

def trade_name(num): # торговое наименование препарата 
    # принимает num = тэговая позиция элемента;
    founded = False

    for i in range(10):
        try:
            WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, f"""//*[@id="ctl00_plate_gr"]/tbody/tr[{num}]/td[2]""")))
            text_find = driver.find_element(By.XPATH, f"""//*[@id="ctl00_plate_gr"]/tbody/tr[{num}]/td[2]""") # эта часть кода ответственна за поиск торгового наименования препарата 
            text_find = text_find.text 
            
            if text_find.isalnum() == True:
                founded = True
                break
        except TimeoutException:
            print("Trying to find trade name...")
            driver.refresh()
            print(captcha_freeze())
            continue

        if founded == False:
            try:
                WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ctl00_plate_lerr"]""")))
                fail_find = driver.find_element(By.XPATH, """//*[@id="ctl00_plate_lerr"]""")
                fail_find = fail_find.text 
                if fail_find == "Произошла ошибка, повторите позже":
                    print("Warning, the error occured. Try to fix it with your hands.")
                    k = input("After the bug's fixed, print - ENTER.")
            except TimeoutException:
                pass

        if founded == False:
            try:
                WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, f"""//*[@id="ctl00_plate_gr"]/tbody/tr[{num}]/td[2]""")))
                text_find = driver.find_element(By.XPATH, f"""//*[@id="ctl00_plate_gr"]/tbody/tr[{num}]/td[2]""") # эта часть кода ответственна за поиск торгового наименования препарата 
                text_find = text_find.text
            except TimeoutException:
                print("Failed to find the information about trade name...")
                l = input("Print any key to exit...")

    if '\"' in text_find: # эта часть кода отвечает за обработку и замену символа двойных кавычек "" на 
            # одинарные '' во избежание ошибок компилляции 
        text_find = list(text_find)
        for i in range(len(text_find)):
            if text_find[i] == '\"':
                text_find[i] = "\'"
        text_find = "".join(text_find)

    
    return text_find # возвращается торговое наименование препарата type = string

def company_name_reg(): # наименование держателя препарата

    try:
        WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ctl00_plate_MnfClNmR"]""")))
        time.sleep(sec)
        text_find = driver.find_element(By.XPATH, """//*[@id="ctl00_plate_MnfClNmR"]""")
        text_find = text_find.text # эта часть кода ответственна за поиск наименования держателя препарата 

        if '\"' in text_find: # эта часть кода отвечает за обработку и замену символа двойных кавычек "" на 
            # одинарные '' во избежание ошибок компилляции 
            text_find = list(text_find)
            for i in range(len(text_find)):
                if text_find[i] == '\"':
                    text_find[i] = "\'"
            text_find = "".join(text_find)

    except TimeoutException:
        print("Failed to find the information about company reg name.")
        k = input("Print any key to exit...")

    return text_find # возвращается наименование компании препарата type = string

def reg_country(): # наименование страны держателя рег удостоверения препарата

    try:
        WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ctl00_plate_CountryClR"]""")))
        time.sleep(sec)
        text_find = driver.find_element(By.XPATH, """//*[@id="ctl00_plate_CountryClR"]""")
        text_find = text_find.text # эта часть кода ответственна за поиск страны преперата
    except TimeoutException:
        print("Failed to find the information about country.")
        k = input("Print any key to exit...")
    
    return text_find # возвращается торговое страна препарата type = string 

def company_name_prod(num, stat): # наименование производителя препарата

    try:
        
        if stat == None:
            WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, f"""//*[@id="ctl00_plate_gr_mnf"]/tbody/tr[{num}]/td[3]""")))
            time.sleep(sec)
            text_find = driver.find_element(By.XPATH, f"""//*[@id="ctl00_plate_gr_mnf"]/tbody/tr[{num}]/td[3]""")
            text_find = text_find.text # эта часть кода ответственна за поиск наименования производителя препарата 
            # //*[@id="ctl00_plate_gr_mnf"]/tbody/tr[3]/td[3]
            if '\"' in text_find: # эта часть кода отвечает за обработку и замену символа двойных кавычек "" на 
                # одинарные '' во избежание ошибок компилляции 
                text_find = list(text_find)
                for i in range(len(text_find)):
                    if text_find[i] == '\"':
                        text_find[i] = "\'"
                text_find = "".join(text_find)
        else:
            return stat

    except TimeoutException:
        print("Failed to find the information about company prod name.")
        k = input("Print any key to exit...")

    return text_find # возвращается наименование компании препарата type = string  

def prod_country(num, stat): # наименование страны держателя рег удостоверения препарата

    try:
        if stat == None:
            WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, f"""//*[@id="ctl00_plate_gr_mnf"]/tbody/tr[{num}]/td[5]""")))
            time.sleep(sec)
            text_find = driver.find_element(By.XPATH, f"""//*[@id="ctl00_plate_gr_mnf"]/tbody/tr[{num}]/td[5]""")
            text_find = text_find.text # эта часть кода ответственна за поиск страны преперата
        else:
            return stat
        
    except TimeoutException:
        print("Failed to find the information about country.")
        k = input("Print any key to exit...")
    
    return text_find # возвращается торговое страна препарата type = string   

def dosage_form(): # форма принятия препарата

    try:
            WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ctl00_plate_drugforms"]/table/tbody/tr[3]/td[1]""")))
            time.sleep(sec)
            text_find = driver.find_element(By.XPATH, """//*[@id="ctl00_plate_drugforms"]/table/tbody/tr[3]/td[1]""")
            text_find = text_find.text # эта часть кода ответственна за поиск наименования производителя препарата 

            if '\"' in text_find: # эта часть кода отвечает за обработку и замену символа двойных кавычек "" на 
                # одинарные '' во избежание ошибок компилляции 
                text_find = list(text_find)
                for i in range(len(text_find)):
                    if text_find[i] == '\"':
                        text_find[i] = "\'"
                text_find = "".join(text_find)

    except TimeoutException:
        print("Failed to find the information about dosage form.")
        return "Не указано"

    return text_find # возвращается торговое форма принятия препарата type = string 

def dosage(): # дозировка препарата

    try:
        WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ctl00_plate_drugforms"]/table/tbody/tr[3]/td[2]""")))
        time.sleep(sec)
        text_find = driver.find_element(By.XPATH, """//*[@id="ctl00_plate_drugforms"]/table/tbody/tr[3]/td[2]""")
        text_find = text_find.text # эта часть кода ответственна за поиск дозировки препарата  

        if '\"' in text_find: # эта часть кода отвечает за обработку и замену символа двойных кавычек "" на 
            # одинарные '' во избежание ошибок компилляции 
            text_find = list(text_find)
            for i in range(len(text_find)):
                if text_find[i] == '\"':
                    text_find[i] = "\'"
            text_find = "".join(text_find)

    except TimeoutException:
        print("Failed to find the information about dosage.")
        return "Не указано"

    return text_find # возвращается торговое Dose препарата type = string 

def containment_condition(): # условия содержания препарата

    try:
        WebDriverWait(driver=driver, timeout=time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ctl00_plate_drugforms"]/table/tbody/tr[3]/td[4]""")))
        time.sleep(sec)
        element = driver.find_element(By.XPATH, """//*[@id="ctl00_plate_drugforms"]/table/tbody/tr[3]/td[4]""")
        element = element.text

        if '\"' in element: # эта часть кода отвечает за обработку и замену символа двойных кавычек "" на 
            # одинарные '' во избежание ошибок компилляции 
            element = list(element)
            for i in range(len(element)):
                if element[i] == '\"':
                    element[i] = "\'"
            element = "".join(element)

    except TimeoutException:
        print("Failed to find the information about containment condition.")
        return "Не указано"
    
    return element

def recipe(): # состояние рецептурности препарата

    try:
        WebDriverWait(driver=driver, timeout=time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ctl00_plate_drugforms"]/table/tbody/tr[4]/td/ul""")))
        time.sleep(sec)
        element = driver.find_element(By.XPATH, """//*[@id="ctl00_plate_drugforms"]/table/tbody/tr[4]/td/ul""")
        element = element.text

    except TimeoutException:
        print("Failed to find the information about recipe.")
        return "Не указано"

    if "По рецепту" in element and "Без рецепта" not in element and "для стационаров" not in element and "для лечебно-профилактических учреждений" not in element and "Не указано" not in element: # если только по рецепту 
        return "По рецепту" # возвращается рецептурное состояние препарата type = string
    elif ("По рецепту" in element and ("Без рецепта" in element or "для стационаров" in element or "для лечебно-профилактических учреждений" in element or "Не указано" in element)): # если по рецепту + без рецепта\стационар
        return "Требуется консультация со специалистом" # возвращается рецептурное состояние препарата type = string

    if "По рецепту" not in element and "Без рецепта" in element and "для стационаров" not in element and "для лечебно-профилактических учреждений" not in element and "Не указано" not in element: # если только без рецепта
        return "Без рецепта" # возвращается рецептурное состояние препарата type = string
    elif ("Без рецепта" in element and ("для стационаров" in element or "По рецепту" in element or "для лечебно-профилактических учреждений" in element or "Не указано" in element)): # если без рецепта + с рецептом\стационар
        return "Требуется консультация со специалистом" # возвращается рецептурное состояние препарата type = string
    
    if "По рецепту" not in element and "Без рецепта" not in element and "для стационаров" in element and "для лечебно-профилактических учреждений" not in element and "Не указано" not in element: # если только стационар
        return "Не указано" # возвращается рецептурное состояние препарата type = string
    elif ("для стационаров" in element and ("Без рецепта" in element or "По рецепту" in element or "для лечебно-профилактических учреждений" in element or "Не указано" in element)): # если стационар + с рецептом\без рецепта
        return "Требуется консультация со специалистом" # возвращается рецептурное состояние препарата type = string

    if "По рецепту" in element and "Без рецепта" in element and "для стационаров" in element and "для лечебно-профилактических учреждений" in element and "Не указано" in element:
        return "Требуется консультация со специалистом" # возвращается рецептурное состояние препарата type = string
    
    if "Не указано" in element and ("По рецепту" in element or "Без рецепта" in element or "для стационаров" in element or "для лечебно-профилактических учреждений" in element):
        return "Требуется консультация со специалистом" # возвращается рецептурное состояние препарата type = string
    elif "Не указано" in element and ("По рецепту" not in element and "Без рецепта" not in element and "для стационаров" not in element and "для лечебно-профилактических учреждений" not in element):
        return "Не указано"
    
    if "для лечебно-профилактических учреждений" in element and ("По рецепту" in element or "Без рецепта" in element or "для стационаров" in element or "Не указано" in element):
        return "Требуется консультация со специалистом"
    elif "для лечебно-профилактических учреждений" in element and ("По рецепту" not in element and "Без рецепта" not in element and "для стационаров" not in element and "Не указано" not in element and "для стационаров" not in element):
        return "Не указано"
    
def active_substance(): # активные вещества, которые содержатся в препарате

    try:
        WebDriverWait(driver=driver, timeout=time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ctl00_plate_Innr"]""")))
        time.sleep(sec)
        element = driver.find_element(By.XPATH, """//*[@id="ctl00_plate_Innr"]""")
        element = element.text

        if '\"' in element: # эта часть кода отвечает за обработку и замену символа двойных кавычек "" на 
            # одинарные '' во избежание ошибок компилляции 
            element = list(element)
            for i in range(len(element)):
                if element[i] == '\"':
                    element[i] = "\'"
            element = "".join(element)

    except TimeoutException:
        print("Failed to find the information about active substance.")
        k = input("Print any key to exit.")
    
    return element

# Конец парсинг-блока
#_________________________________________________________________________________________________________________

#_________________________________________________________________________________________________________________
# Начало функционального блока

def page_reassignment(digit, page):

    match digit:
        case 1:
            page = 2
            return page
        case 2:
            page = 3
            return page
        case 3:
            page = 4
            return page
        case 4:
            page = 5
            return page
        case 5:
            page = 6
            return page
        case 6:
            page = 7
            return page
        case 7:
            page = 8
            return page
        case 8:
            page = 9
            return page
        case 9:
            page = 10
            return page

def company_count():

    for i in range(2, 20):
        try:
            WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, f"""//*[@id="ctl00_plate_gr_mnf"]/tbody/tr[{i}]""")))
            text_find = driver.find_element(By.XPATH, f"""//*[@id="ctl00_plate_gr_mnf"]/tbody/tr[{i}]""")
            text_find = text_find.text ; text_find = text_find.lower()

            if "производитель" in text_find:
                return i, None
        except TimeoutException:
            return None, "Не указано"

def captcha_freeze():

    try:
        WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="dCaptcha"]/center/table/tbody/tr/td/div/div/span""")))
        time.sleep(sec)
        driver_find = driver.find_element(By.XPATH, """//*[@id="dCaptcha"]/center/table/tbody/tr/td/div/div/span""")
        driver_find = driver_find.text.lower()
    
        if "код" in driver_find:
            print_key = input("""Captcha has been spotted. Once you solved it
            print any key to go on with the script.\n""")

            time.sleep(3)
            return "Captcha has been passed."
    except TimeoutException:
        return "No captcha found"

def clear_request(input_field): # очистка поля ввода МНН
    #принимает в себя тип данных Web_element 
    input_field.send_keys(Keys.CONTROL+"a")
    input_field.send_keys(Keys.DELETE)

def inner_page_find(link_num): # поиск информации внутри "паспорта препарата", принимает link_num - тэговая позиция элемента 

    print(captcha_freeze())

    try:
        time.sleep(sec)
        tr_name = trade_name(link_num) 
        WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, f"""//*[@id="ctl00_plate_gr"]/tbody/tr[{link_num}]""")))
        link_find = driver.find_element(By.XPATH, f"""//*[@id="ctl00_plate_gr"]/tbody/tr[{link_num}]""") 
        time.sleep(3)
        link_find.click() # алгоритм "кликает" на препарат, переходя в "паспорт препарата"
    except TimeoutException:
        print("The page's out of elements.")
        k = input("Enter any key to exit the programm...")

    print(captcha_freeze())

    number, status = company_count()


    table_add([company_name_reg(), reg_country(), company_name_prod(number, status), prod_country(number, status), 
               dosage_form(), dosage(), containment_condition(), recipe(), active_substance()], tr_name) # определенные значения-характеристики помещаются в таблицу
     
    print(f"Finished with adding the information about {tr_name}.\n")

    time.sleep(3)
    driver.back() # возврат на предудущую страницу (выход из "паспорта препарата") 

def page_roller(total_page_num, tag_inner_num):
    two_pages = False

    if total_page_num == 2:

        WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, f"""//*[@id="aspnetForm"]/div[3]/div[3]/table[3]/tbody/tr/td[{tag_inner_num}]""")))
        time.sleep(sec)
        page_find = driver.find_element(By.XPATH, f"""//*[@id="aspnetForm"]/div[3]/div[3]/table[3]/tbody/tr/td[{tag_inner_num}]""")
        page_find.click()
        two_pages = True 
        return two_pages
    elif total_page_num > 2: 
        
        if tag_inner_num > 2:
            tag_inner_num += 1 
        try:
            WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, f"""//*[@id="aspnetForm"]/div[3]/div[3]/table[3]/tbody/tr/td[{tag_inner_num}]""")))
            time.sleep(sec)
            page_find = driver.find_element(By.XPATH, f"""//*[@id="aspnetForm"]/div[3]/div[3]/table[3]/tbody/tr/td[{tag_inner_num}]""")
            page_find.click()
        except TimeoutException:
            print("Out of pages")

def amount_of_elements(): # общее количество найденных препаратов (всего найденных элементов)

    WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ctl00_plate_lrecn"]""")))
    time.sleep(sec)
    element_check = driver.find_element(By.XPATH, """//*[@id="ctl00_plate_lrecn"]""")
    element_check = element_check.text
    num = ""
    lst = []

    for i in range(len(element_check)):
        num = ""
        if element_check[i].isdigit() == True:
            num = element_check[i]
            lst.append(num)

    num = "".join(lst)
    num = int(num)

    if num >= 100:
        percent = 1
    else:
        percent = 100 / num

    return [num, percent] # возвращает общее число элементов в виде целого числа (всего найденных препаратов) и процент для загрузки. type = list 

def exeption_check(): # проверка на общее количество страниц

    try:
        p = 2

        while p < 100:

            # print("Page val =", p)
            WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, f"""//*[@id="aspnetForm"]/div[3]/div[3]/table[3]/tbody/tr/td[{p}]""")))
            time.sleep(sec)
            page_find = driver.find_element(By.XPATH, f"""//*[@id="aspnetForm"]/div[3]/div[3]/table[3]/tbody/tr/td[{p}]""")

            p += 1 
    except TimeoutException: 
        return p # возвращает всего общее количество число страниц (значение возвращается тэговое, реальное значение = p - 2) type = integer

def extract_value(gl_dict, num): # извлечение МНН из global_dict

    mnn_value = gl_dict.get(num)[0] # эта функция извлекает из dict = global_dict (скрипт mnn_dict_res) значение num
    input_value = list(mnn_value) ; input_value[0] = input_value[0].upper() ; input_value = "".join(mnn_value)
    table_value = mnn_value.split(" ") ; table_value = "_".join(table_value) 

    return [input_value, table_value] # возвращает МНН препарата для вставки в строку input и для вставку в таблицу бд type = string

def value_check(): # проверка состояния ввода

    try:
        time.sleep(sec)
        WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ctl00_plate_lrecn"]""")))
        element_check = driver.find_element(By.XPATH, """//*[@id="ctl00_plate_lrecn"]""")
        elements_flag = True
        print(f"Elements state: {elements_flag}")
    except TimeoutException:
        elements_flag = False
        print(f"Elements state: {elements_flag}")

    try:
        time.sleep(sec)
        WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ctl00_plate_lerr"]""")))
        fail_find = driver.find_element(By.XPATH, """//*[@id="ctl00_plate_lerr"]""")
        fail_find = fail_find.text # тут идёт проверка на наличие препарата в реестре grls (если его нету
        # то функция возвращает "Данные не найдены")
        print('Warning: ', fail_find)

        return [fail_find, elements_flag] # возвращается "состояние поиска" препарата (найден или нет) type = string 
    except TimeoutException:
        fail_find = "Данные найдены"
        print('Warning: ', fail_find)

        return [fail_find, elements_flag] # возвращается "состояние поиска" препарата (найден или нет) type = string

def value_return(mnn_value): # проверка предложенных вариантов ввода, при помещении МНН в строку поиска 
    
    value_flag = False
    mnn_value = mnn_value.lower()
    mnn_value_list = mnn_value.split()

    if len(mnn_value_list) > 1:
        return True # если вводимое значение МНН составляет больше двух слов, то возвращается True

    try:    
        WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="aspnetForm"]/div[3]/div[3]/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/span/span[2]/div/span/div[1]/b/p""")))
        variants_val = driver.find_element(By.XPATH, """//*[@id="aspnetForm"]/div[3]/div[3]/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/span/span[2]/div/span/div[1]/b/p""")
        time.sleep(sec)
        variants_val = variants_val.text

        if "+" in variants_val: # обработка вариантов с символами "+"
            variants_val = variants_val.split("+")
        else:
            variants_val = variants_val.split()

        #print("Var val=", variants_val)
        for value in variants_val:
    
                if "[" in value or "]" in value: # обработка вариантов с символами "[" или "]"
                    position = variants_val.index(value)
        
                    for chr in range(len(value)):
                        if value[chr] == "[" or value[chr] == "]":
                            value = list(value) ; value[chr] = ""
                
                    value = "".join(value) ; value.strip() ; variants_val[position] = value

                #print("Value =", value)

                if value.lower() == mnn_value:
                    value_flag = True
        
        return value_flag # возвращает флаг type == bool. Если True, то предлагаемое значение совпадает с вводимым МНН значением. 

    except TimeoutException:
        
        try:
            WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="aspnetForm"]/div[3]/div[3]/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/span/span[2]/div/span/div/b/p""")))
            variants_val = driver.find_element(By.XPATH, """//*[@id="aspnetForm"]/div[3]/div[3]/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/span/span[2]/div/span/div/b/p""")
            time.sleep(sec)
            variants_val = variants_val.text
            print("Var val=", variants_val)

            if "+" in variants_val:
                variants_val = variants_val.split("+")
            else:
                variants_val = variants_val.split()

            for value in variants_val:
    
                if "[" in value or "]" in value:
                    position = variants_val.index(value)
        
                    for chr in range(len(value)):
                        if value[chr] == "[" or value[chr] == "]":
                            value = list(value) ; value[chr] = ""
                
                    value = "".join(value) ; value.strip() ; variants_val[position] = value
                
                #print("Value =", value)
         
                if value.lower() == mnn_value:
                    value_flag = True
            
            return value_flag
        except TimeoutException:
            return False # Если нету предложенных значений вообще, то возвражается False

def value_input(value): # ввод МНН 
# принимает значение МНН из global_dict 
    WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, """//*[@id="ctl00_plate_txtMNN"]""")))
    time.sleep(sec)
    search_find = driver.find_element(By.XPATH, """//*[@id="ctl00_plate_txtMNN"]""")
    clear_request(search_find) # перед новой записью поле чистится 
    search_find.send_keys(value) # внутрь подается одно значение из списка взятого из скрипта mnn_dict_res (global_dict).
    value_flag = value_return(value) # идёт закрепление статуса соответствия вводимого значения предлагаемым

    return [value_flag, search_find]

# Конец функционального-блока
#_________________________________________________________________________________________________________________

#_________________________________________________________________________________________________________________
# Тело алгоритма. Сюда мы помещаем все функции так, чтобы они корректно работали 

def search_enum():
    global test_value
    global test
    end = False
    last_page = False
    end_of_pages = False
    loading = 0

    num_of_elem = int(amount_of_elements()[0])
    print(f"The number of elements is {num_of_elem}", end="\n")

    percent = round(amount_of_elements()[1], 2) # округление и дальнейший вывод процентажа при загрузке

    page_num = exeption_check() - 2 
    print(f"The number of pages is {page_num}")

    if num_of_elem > 10:
        tag_page = 2 
        last_el = num_of_elem - ((page_num - 1) * 10)

        while tag_page < page_num + 2:

            if test == False:
                new_start = 2 
            else:
                test_value = int(test_value)
                fst_digit = test_value // 10
                if test_value > 10:
                    test_value -= 10 * (fst_digit)
                    tag_page = page_reassignment(fst_digit, tag_page)

                    WebDriverWait(driver, time_val).until(EC.presence_of_element_located((By.XPATH, f"""//*[@id="aspnetForm"]/div[3]/div[3]/table[3]/tbody/tr/td[{tag_page}]""")))
                    time.sleep(2)
                    driver.find_element(By.XPATH, f"""//*[@id="aspnetForm"]/div[3]/div[3]/table[3]/tbody/tr/td[{tag_page}]""").click()
                
                    tag_page += 1
                    new_start = test_value + 1
                else:
                    new_start = test_value + 1

            for link_num in range(new_start, 12):
                 # Данный блок бегает по всем элементам страницы 

                if (tag_page - 1 != page_num): # до момента, пока алгоритм не дойдет до последней страницы 
                    # будет происходить классчиеский парсинг вплоть до 11-ого элемента 
                    last_page = False
                    inner_page_find(link_num)
                    loading += percent  
                    print(f"Loading data: {loading}%")
                elif (tag_page - 1 == page_num): # на как только алгоритм дойдет до последней страницы 
                    # он во первых сохранит флаг, во вторых - будет работать до тех пор пока не дойдет до крайнего элемента 
                    last_page = True
                    if link_num - 1 != last_el:
                        inner_page_find(link_num)
                        print(captcha_freeze())
                        loading += percent  
                        print(f"Loading data: {loading}%")
                        end = False
                    elif link_num - 1 == last_el:
                        inner_page_find(link_num)
                        print(captcha_freeze())
                        loading += percent  
                        print(f"Loading data: {loading}%")
                        end = True 
                        break
            
            if end_of_pages == True:
                break

            if last_page == False and end == False:
                test = False
                if page_num > 2:  
                    time.sleep(sec)
                    print(page_roller(page_num, tag_page))
                elif page_num == 2:
                    end_of_pages = page_roller(page_num, tag_page)
            else:
                break

            tag_page += 1 
    else:

        if test == False:
                new_start = 2 
        else:
                new_start = int(test_value) + 1

        for link_num in range(new_start, num_of_elem + 2): 
                    inner_page_find(link_num)
                    print(captcha_freeze())
                    loading += percent  
                    print(f"Loading data: {loading}%")

#_________________________________________________________________________________________________________________
# Ниже идёт заключительный алгоритм 

print(f"The dict max value = {len(global_dict)}")
start = int(input("Print down the start-value.\n"))
end = int(input("Print down the end-value.\n"))
test_value = input("""Print down (if neccessary) the start-element value (from 1 to 10). If you dont want to use 
the test value - push ENTER.\n""")
table_create()


for i in range(start, end + 1):

    if test_value != "":
        test = True 
    else:
        test = False

    input_value = extract_value(global_dict, i)[0] ; table_value = extract_value(global_dict, i)[1]
    value_status = value_input(input_value) ; v_input = value_status[0] ; v_search = value_status[1]

    if v_input == True:
        time.sleep(sec)
        v_search.send_keys(Keys.RETURN)
        print(captcha_freeze())
    else:
        print(f"Value {input_value} wasnt't found")
        continue

    data_find = value_check()[0] ; elements_find = value_check()[1]

    while True:
        if data_find == "Произошла ошибка, повторите позже":
            driver.refresh()
            print(captcha_freeze())
            data_find = value_check()[0]
            elements_find = value_check()[1]
        else:
            break
    
    if data_find != "Данные не найдены" and elements_find != False:

        time.sleep(3)
        search_enum() 

        print(end="\n\n")
        print(f"{input_value} was completely parsed.")
    else:
        print(f"Value {input_value} wasn't found.\n\n")
        continue


time.sleep(5)
k = input("Enter any key to exit.")
driver.close()

k = input()

