from selenium import webdriver
from tyre import Tyre
from setup import Setup
from selenium.webdriver.support.select import Select
import base64

class GPRO:

    def __init__(self, username, password):
        global browser
        opt = webdriver.ChromeOptions()
        # opt.headless = True
        browser = webdriver.Chrome(chrome_options=opt)
        browser.get('http://gpro.net/gb/gpro.asp')

        txtLogin = browser.find_element_by_id('Text1')
        txtSenha = browser.find_element_by_id('Password2')
        btnSubmit = browser.find_element_by_id('Submit2')

        txtLogin.send_keys(username)
        txtSenha.send_keys(password)
        btnSubmit.click()
        
    def __del__(self):
        browser.quit()

    def setup_race(self, tyres, setup: Setup, max_pitstops:str):
        ideal_tyre = self.get_ideal_tyre(setup, tyres, max_pitstops)

        if setup.qualifying == 'Q1':
            browser.get('https://gpro.net/gb/Qualify.asp')
            radio_qualify_element = browser.find_element_by_id('radioQual')
            radio_qualify_element.click()
        elif setup.qualifying == 'Q2':
            browser.get('https://gpro.net/gb/Qualify2.asp')
            fuel_input_element = browser.find_element_by_id('Fuel')
            fuel_input_element.clear()
            fuel_input_element.send_keys(int(ideal_tyre.fuel_load) + 2)
        else: # Race
            browser.get('https://gpro.net/gb/RaceSetup.asp')
            fuel1_input_element = browser.find_element_by_name('FuelStop1')
            fuel1_input_element.clear()
            fuel1_input_element.send_keys(int(ideal_tyre.fuel_load) + 2)
            fuel2_input_element = browser.find_element_by_name('FuelStop2')
            fuel2_input_element.clear()
            fuel2_input_element.send_keys(int(ideal_tyre.fuel_load) + 2)
            fuel3_input_element = browser.find_element_by_name('FuelStop3')
            fuel3_input_element.clear()
            fuel3_input_element.send_keys(int(ideal_tyre.fuel_load) + 2)
            fuel4_input_element = browser.find_element_by_name('FuelStop4')
            fuel4_input_element.clear()
            fuel4_input_element.send_keys(int(ideal_tyre.fuel_load) + 2)
            fuel5_input_element = browser.find_element_by_name('FuelStop5')
            fuel5_input_element.clear()
            fuel5_input_element.send_keys(int(ideal_tyre.fuel_load) + 2)

            start_tyre_select_element = browser.find_element_by_id('StartTyres')
            start_tyre_select = Select(start_tyre_select_element)
            rain_tyre_select_element = browser.find_element_by_id('RainTyres')
            rain_tyre_select = Select(rain_tyre_select_element)
            dry_tyre_select_element = browser.find_element_by_id('DryTyres')
            dry_tyre_select = Select(dry_tyre_select_element)
            
            start_tyre_select.select_by_visible_text(ideal_tyre.name)
            rain_tyre_select.select_by_visible_text('Rain')
            dry_tyre_select.select_by_visible_text(ideal_tyre.name)

            riskover_input_element = browser.find_element_by_name('RiskOver')
            riskover_input_element.clear()
            riskover_input_element.send_keys('0')
            riskdefend_input_element = browser.find_element_by_name('RiskDefend')
            riskdefend_input_element.clear()
            riskdefend_input_element.send_keys('0')
            driverrisk_input_element = browser.find_element_by_name('DriverRisk')
            driverrisk_input_element.clear()
            driverrisk_input_element.send_keys('0')
            riskwet_input_element = browser.find_element_by_name('RiskWet')
            riskwet_input_element.clear()
            riskwet_input_element.send_keys('0')
            driverriskprob_input_element = browser.find_element_by_name('DriverRiskProb')
            driverriskprob_input_element.clear()
            driverriskprob_input_element.send_keys('0')
            boostlap1_input_element = browser.find_element_by_name('BoostLap1')
            boostlap1_input_element.clear()
            boostlap1_input_element.send_keys('0')
            boostlap2_input_element = browser.find_element_by_name('BoostLap2')
            boostlap2_input_element.clear()
            boostlap2_input_element.send_keys('0')
            boostlap3_input_element = browser.find_element_by_name('BoostLap3')
            boostlap3_input_element.clear()
            boostlap3_input_element.send_keys('0')

            startrisk_select_element = browser.find_element_by_name('StartRisk')
            startrisk_select = Select(startrisk_select_element)
            startrisk_select.select_by_value('3')

        front_wing_element = browser.find_element_by_name('FWing')
        front_wing_element.clear()
        front_wing_element.send_keys(setup.calculated_front_wing)

        rear_wing_element = browser.find_element_by_name('RWing')
        rear_wing_element.clear()
        rear_wing_element.send_keys(setup.calculated_rear_wing)

        engine_element = browser.find_element_by_name('Engine')
        engine_element.clear()
        engine_element.send_keys(setup.engine)

        brakes_element = browser.find_element_by_name('Brakes')
        brakes_element.clear()
        brakes_element.send_keys(setup.brakes)

        gear_element = browser.find_element_by_name('Gear')
        gear_element.clear()
        gear_element.send_keys(setup.gear)

        suspension_element = browser.find_element_by_name('Suspension')
        suspension_element.clear()
        suspension_element.send_keys(setup.suspension)

        tyre_element_exists = len(browser.find_elements_by_id('Tyres')) > 0
        if tyre_element_exists:
            tyre_select_element = browser.find_element_by_id('Tyres')
            tyre_select = Select(tyre_select_element)
            tyre_select.select_by_visible_text(ideal_tyre.name)

        risk_element_exists = len(browser.find_elements_by_id('Risk')) > 0
        if risk_element_exists:
            risk_select_element = browser.find_element_by_name('Risk')
            risk_select = Select(risk_select_element)
            risk_select.select_by_value('3')
        
        if setup.qualifying == 'Race':
            btnracesubmit_element = browser.find_element_by_name('btnConfirmSettings')
            btnracesubmit_element.click()
        else:
            btn_submit_element = browser.find_element_by_name('DriveLap')
            btn_submit_element.click()
            
            exist_element = len(browser.find_elements_by_id('DryTyres')) > 0
            if exist_element:
                dry_tyres_select_element = browser.find_element_by_id('DryTyres')
                dry_tyres_select = Select(dry_tyres_select_element)
                dry_tyres_select.select_by_visible_text(ideal_tyre.name)

        return

    def get_ideal_tyre(self, setup, tyres, max_pitstops):
        ideal_tyre = Tyre()
        if setup.weather == 'Wet':
            for t in tyres:
                if t.name == 'Rain':
                    ideal_tyre = t
                    break
        else:
            for t in tyres:
                if t.name != 'Rain':
                    if t.stops == max_pitstops:
                        ideal_tyre = t
                        break
        return ideal_tyre
    
    def end_navigation(self):
        browser.quit()

