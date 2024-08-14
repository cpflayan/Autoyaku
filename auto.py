import sqlite3
import requests

def get_unused_email():
    # 连接到SQLite数据库
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    try:
        # 查询一条未使用的电子邮件
        cursor.execute("SELECT id, email FROM emails WHERE used = 0 LIMIT 1")
        result = cursor.fetchone()

        if result:
            email_id, email_address = result

            # 标记为已使用
            cursor.execute("UPDATE emails SET used = 1 WHERE id = ?", (email_id,))
            conn.commit()

            return email_address
        else:
            return None

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # 关闭数据库连接
        conn.close()

def send_request_with_email(email):
    url = 'https://www.yakuza.bet/api/users'
    headers = {
        'accept': 'application/vnd.softswiss.v1+json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.yakuza.bet',
        'priority': 'u=1, i',
        'referer': 'https://www.yakuza.bet/entry?bar=modal&sign-up=modal',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36',
        'x-display-mode': 'browser'
    }

    data = {
        "user": {
            "email": email,
            "password": "12345678",
            "password_confirmation": "12345678",
            "country": "JP",
            "receive_promos": True,
            "receive_sms_promos": True,
            "receive_promos_via_phone_calls": True,
            "agreed_to_partner_promotions": True,
            "currency": "BTC",
            "terms_acceptance": True,
            "age_acceptance": True,
            "groups": [],
            "context": "registration"
        }
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, json=data)
    return response

# 获取未使用的电子邮件
email = get_unused_email()
if email:
    print(f"使用的电子邮件: {email}")

    # 发送请求
    response = send_request_with_email(email)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
else:
    print("没有可用的电子邮件")
