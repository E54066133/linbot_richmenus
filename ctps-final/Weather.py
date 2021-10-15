from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

def get_weather(): #台南東區
    chrome_options = Options() # 啟動無頭模式
    chrome_options.add_argument('--headless')  #規避google bug
    chrome_options.add_argument("--incognito")
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56"
    chrome_options.add_argument("user-agent={}".format(ua))  

    path="chromedriver.exe"
    driver = webdriver.Chrome(executable_path=path,options=chrome_options)
    # driver=webdriver.Chrome()
    driver.get("https://www.google.com/search?q=%E5%8F%B0%E5%8D%97%E6%9D%B1%E5%8D%80%E5%A4%A9%E6%B0%A3&oq=%E5%8F%B0%E5%8D%97%E6%9D%B1%E5%8D%80%E5%A4%A9%E6%B0%A3&aqs=edge..69i57j0.2782j0j1&sourceid=chrome&ie=UTF-8")
    temperature=driver.find_element_by_xpath('//*[@id="wob_tm"]')
    cloud=driver.find_element_by_xpath('//*[@id="wob_dc"]')
    rain_prob=driver.find_element_by_xpath('//*[@id="wob_pp"]')

    temperature=temperature.text
    cloud=cloud.text
    rain_prob=rain_prob.text

    env_condition = {}
    env_condition["temp"] = temperature
    env_condition["cloud"] = cloud
    env_condition["rain"] = rain_prob

    return env_condition

if __name__ == "__main__":
    weather_info=get_weather()
    print(weather_info)