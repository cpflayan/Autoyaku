from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 设定ChromeDriver路径
service = Service('/usr/bin/chromedriver')

# 初始化WebDriver
driver = webdriver.Chrome(service=service)

try:
    # 打开注册页面
    driver.get("https://www.yakuza.bet/?sign-up=modal")

    # 等待注册表单加载完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "form"))
    )

    # 获取表单元素
    form = driver.find_element(By.TAG_NAME, "form")

    # 查找表单中的所有输入字段
    input_elements = form.find_elements(By.TAG_NAME, "input")

    # 输出每个输入字段的名称
    for input_element in input_elements:
        print(f"Input name: {input_element.get_attribute('name')}, type: {input_element.get_attribute('type')}")

    # 如果需要查找其他类型的字段，比如select，可以按需添加
    select_elements = form.find_elements(By.TAG_NAME, "select")
    for select_element in select_elements:
        print(f"Select name: {select_element.get_attribute('name')}")

finally:
    # 关闭浏览器
    driver.quit()
