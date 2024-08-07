from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置 ChromeDriver 路径
service = Service('/usr/bin/chromedriver')

# 设置 ChromeOptions 以启用无头模式
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

# 初始化 WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 打开注册页面
    driver.get("https://www.yakuza.bet/?sign-up=modal")

    # 增加等待时间和改进等待条件
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.TAG_NAME, "form"))
    )

    # 获取表单元素
    form = driver.find_element(By.TAG_NAME, "form")

    # 查找表单中的所有输入字段
    input_elements = form.find_elements(By.TAG_NAME, "input")

    # 输出每个输入字段的名称
    for input_element in input_elements:
        print(f"Input name: {input_element.get_attribute('name')}, type: {input_element.get_attribute('type')}")

    # 查找 select 元素
    select_elements = form.find_elements(By.TAG_NAME, "select")
    for select_element in select_elements:
        print(f"Select name: {select_element.get_attribute('name')}")

finally:
    # 关闭浏览器
    driver.quit()
