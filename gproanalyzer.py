from selenium import webdriver
from selenium.webdriver.support.select import Select
from tyre import Tyre
from setup import Setup
import base64

class GPROAnalyzer:

    def __init__(self, username, password):
        global browser
        opt = webdriver.ChromeOptions()
        opt.headless = True
        browser = webdriver.Chrome(chrome_options=opt)
        browser.get('http://gproanalyzer.info/login.php')

        txtLogin = browser.find_element_by_name('username')
        txtSenha = browser.find_element_by_name('password')
        btnSubmit = browser.find_element_by_class_name('SubmitButton')

        txtLogin.send_keys(username)
        txtSenha.send_keys(password)
        btnSubmit.click()
        
    def __del__(self):
        browser.quit()

    def get_temp(self, qualifying):
        temp_elements = browser.find_elements_by_xpath('//form[@action="setup.php"]/table/tbody/tr')
        temp_row = temp_elements[8]
        temp_data = temp_row.find_elements_by_tag_name('span')

        temperature = '0'
        if qualifying == 'Q1':
            temperature = temp_data[0].text
        elif qualifying == 'Q2':
            temperature = temp_data[1].text
        else:
            temperature = temp_data[2].text

        return temperature

    def extract_race_strategy(self):

        browser.get('http://gproanalyzer.info/racestrategy.php')

        tyre_elements = browser.find_elements_by_xpath('//th[contains(@class,"Blue") or contains(@class,"Purple")]/input')

        # extra_soft_tyre = 0 ao 6
        # soft_tyre       = 7 ao 13
        # medium_tyre     = 14 ao 20
        # hard_tyre       = 21 ao 27
        # rain_tyre       = 28 ao 34

        # por preguiça, não fiquei pensando em uma forma mais "correta" pra montar os dados abaixo
        # vai ficar assim mesmo kkkkk
        tyres = []

        tyre = Tyre()
        tyre.name = 'Extra Soft'
        tyre.stops = tyre_elements[0].get_attribute('value')
        tyre.fuel_load = tyre_elements[1].get_attribute('value')
        tyre.pit_time = tyre_elements[2].get_attribute('value')
        tyre.lost_time_tcd = tyre_elements[3].get_attribute('value')
        tyre.lost_time_fld = tyre_elements[4].get_attribute('value')
        tyre.lost_time_pits = tyre_elements[5].get_attribute('value')
        tyre.lost_time_total = tyre_elements[6].get_attribute('value')
        tyres.append(tyre)

        tyre = Tyre()
        tyre.name = 'Soft'
        tyre.stops = tyre_elements[7].get_attribute('value')
        tyre.fuel_load = tyre_elements[8].get_attribute('value')
        tyre.pit_time = tyre_elements[9].get_attribute('value')
        tyre.lost_time_tcd = tyre_elements[10].get_attribute('value')
        tyre.lost_time_fld = tyre_elements[11].get_attribute('value')
        tyre.lost_time_pits = tyre_elements[12].get_attribute('value')
        tyre.lost_time_total = tyre_elements[13].get_attribute('value')
        tyres.append(tyre)
        
        tyre = Tyre()
        tyre.name = 'Medium'
        tyre.stops = tyre_elements[14].get_attribute('value')
        tyre.fuel_load = tyre_elements[15].get_attribute('value')
        tyre.pit_time = tyre_elements[16].get_attribute('value')
        tyre.lost_time_tcd = tyre_elements[17].get_attribute('value')
        tyre.lost_time_fld = tyre_elements[18].get_attribute('value')
        tyre.lost_time_pits = tyre_elements[19].get_attribute('value')
        tyre.lost_time_total = tyre_elements[20].get_attribute('value')
        tyres.append(tyre)

        tyre = Tyre()
        tyre.name = 'Hard'
        tyre.stops = tyre_elements[21].get_attribute('value')
        tyre.fuel_load = tyre_elements[22].get_attribute('value')
        tyre.pit_time = tyre_elements[23].get_attribute('value')
        tyre.lost_time_tcd = tyre_elements[24].get_attribute('value')
        tyre.lost_time_fld = tyre_elements[25].get_attribute('value')
        tyre.lost_time_pits = tyre_elements[26].get_attribute('value')
        tyre.lost_time_total = tyre_elements[27].get_attribute('value')
        tyres.append(tyre)

        tyre = Tyre()
        tyre.name = 'Rain'
        tyre.stops = tyre_elements[28].get_attribute('value')
        tyre.fuel_load = tyre_elements[29].get_attribute('value')
        tyre.pit_time = tyre_elements[30].get_attribute('value')
        tyre.lost_time_tcd = tyre_elements[31].get_attribute('value')
        tyre.lost_time_fld = tyre_elements[32].get_attribute('value')
        tyre.lost_time_pits = tyre_elements[33].get_attribute('value')
        tyre.lost_time_total = tyre_elements[34].get_attribute('value')
        tyres.append(tyre)

        return tyres

    def get_calculated_wings_data(self, wing_value, weather, temp):
        wings = []
        browser.get('http://gproanalyzer.info/wingsplit.php')

        wing_value_element = browser.find_element_by_name('fwrw')
        wing_value_element.clear()
        wing_value_element.send_keys(wing_value)
        
        weather_select_element = browser.find_element_by_xpath('//select[@name="weather"]')
        weather_select = Select(weather_select_element)
        weather_select.select_by_visible_text(weather)

        temp_element = browser.find_element_by_name('temp')
        temp_element.clear()
        temp_element.send_keys(temp)

        button_calculate_element = browser.find_element_by_class_name('SubmitButton')
        button_calculate_element.click()

        front_wing_element = browser.find_element_by_name('fwd')
        rear_wing_element = browser.find_element_by_name('rwd')

        fwd = front_wing_element.get_attribute('value')
        rwd = rear_wing_element.get_attribute('value')

        wings.append(fwd)
        wings.append(rwd)

        return wings

    def get_weather(self, qualifying):
        if browser.current_url != 'http://gproanalyzer.info/setup.php':
            browser.get('http://gproanalyzer.info/setup.php')
        
        weather = ''
        weather_row_element = browser.find_elements_by_xpath('//form[@action="setup.php"]/table/tbody/tr')
        weather_row = weather_row_element[7]
        weather_data = weather_row.find_elements_by_tag_name('span')
        if qualifying == 'Q1':
            if weather_data[0].text == 'Rain':
                weather = 'Wet'
            else:
                weather = weather_data[0].text
        else:
            if weather_data[1].text == 'Rain':
                weather = 'Wet'
            else:
                weather = weather_data[1].text

        return weather


    def set_setup(self, qualifying):
        weather = self.get_weather(qualifying)
        temp = self.get_temp(qualifying)

        if qualifying == 'Q2' or 'Race':
            weather_select_element = browser.find_element_by_name('weatherr')
            weather_select = Select(weather_select_element)
            new_weather = weather
            if weather == 'Rain':
                new_weather = 'Wet'
            weather_select.select_by_visible_text(new_weather)
            weather_input_element = browser.find_element_by_name('tempr')
            weather_input_element.clear()
            weather_input_element.send_keys(temp)

            btn_recalc_element = browser.find_element_by_class_name('SubmitButton')
            btn_recalc_element.click()

        setup_elements = browser.find_elements_by_xpath('//th[@class="Calc Blue"]/input')

        setup = Setup()
        setup.original_front_wing = setup_elements[0].get_attribute('value')
        setup.original_rear_wing = setup_elements[1].get_attribute('value')
        setup.engine = setup_elements[2].get_attribute('value')
        setup.brakes = setup_elements[3].get_attribute('value')
        setup.gear = setup_elements[4].get_attribute('value')
        setup.suspension = setup_elements[5].get_attribute('value')
        setup.qualifying = qualifying
        setup.temperature = temp
        setup.weather = weather

        return setup

    def get_setup_data(self, qualifying):
        browser.get('http://gproanalyzer.info/setup.php')

        setup = self.set_setup(qualifying)

        wings = self.get_calculated_wings_data(setup.original_front_wing, setup.weather, setup.temperature)
        setup.calculated_front_wing = wings[0]
        setup.calculated_rear_wing = wings[1]

        return setup

    def end_navigation(self):
        browser.quit()

