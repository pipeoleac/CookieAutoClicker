from selenium import webdriver
import time

from selenium.webdriver.common.by import By


chrome_driver_path = "C:\\Users\\pipeo\\Desktop\\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_path)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

#css = """div[onclick="Buy('Grandma');"] """
#Get cookie to click on.
#cookie = driver.find_element_by_id("cookie")
cookie = driver.find_element(By.ID, "cookie")

#Get upgrade item ids.

items = driver.find_elements(By.CSS_SELECTOR, """div[onclick="Buy('Grandma');"] """)

item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 60*5 # 5minutes

while True:
    cookie.click()


    #Cada 5 segundos:
    if time.time() > timeout:

        #Upgradea las <b> tags
        all_prices = driver.find_elements(By.CSS_SELECTOR, """div[onclick="Buy('Grandma');"] """)
        item_prices = []

        #Convierte <b> texto en int.
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace("'", ""))
                item_prices.append(cost)

        #Crea diccionario le los items y prices guardados
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        #Contador de cookies actualizado
        money_element = driver.find_element_by_id("money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        #Upgrades que podemos pagar
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                 affordable_upgrades[cost] = id

        #Compra el Upgrade mas caro que podamos pagar
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element_by_id(to_purchase_id).click()

        #Añade 5 segundos mas hasta el porximo checkeo
        timeout = time.time() + 5

    #Despues de 5 secs, para el bot y ccheckea las cookies por segundo
    if time.time() > five_min:
        cookie_per_s = driver.find_element_by_id("cps").text
        print(cookie_per_s)
        break

