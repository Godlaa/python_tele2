import aiohttp
import asyncio
import telebot

# Конфигурация
url = "https://t2-gifts.ru/getgift"
token = "ux85sqrC8dxquM6P0GsPQULgq5Iso7QQHBqRbHV1"

cookies = {
    'XSRF-TOKEN': 'eyJpdiI6IlRRS1pibTZ3SGFxTnpERVBwK0hWWHc9PSIsInZhbHVlIjoicWh6eldkR25RN2hvU1J6bWlkTytXRm1jZDNaT2FnemlYVmwxakd0Zzhwa1VLKzJmTExkdk9hS1dSeEw1MGxxaUNrZHI3blgzNnpTcWNjWCtDN1E1am1YZytGdXR5VUVNU1lyUG1MRHFZOEpwM0l2TnVueUwxSUp1dmJsR0pmaWEiLCJtYWMiOiI0MjUyYzZmMDE4NjFkM2VkZDdjNDkwMWYzNzJlMTUwYzk5NTgzZDZiMzkxNDFiMWRiNDRkN2ZmOTFjOWI5ZmM5IiwidGFnIjoiIn0%3D',
    'laravel_session': 'eyJpdiI6IndHbTg4cndsa21XaVdaSzVIZHRkSlE9PSIsInZhbHVlIjoiQWJzQTFNOFdDSllrWW5OSk5STDd6dlhYbDRTKzhWVCtlRUtOY0lKaVJIZHJCOTkxbWxEK2dDZTBYYzRGOHU1Vlg3OEtQMnhWSEhsZHdldC9LajZQQU5nZTh2WklnWHpZTzM0c1drYk5UQ01lTVI2Z3Jkb2lneVFZbCtsaXcxQkciLCJtYWMiOiIyNmQyMmJmODQ3ZjZjN2JmZWYxYTA5NWZkMzBlZWRmZWM1M2Q1ZTEyOWM0YmQ5ZTA4OGRlODJhZTY3M2FiYmI2IiwidGFnIjoiIn0%3D'
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-CSRF-TOKEN': token
}

data = {
    '_token': token
}

proxies = [
    "194.35.113.68:1050@qBhvJW:FtXKvBMaYs",
    "46.8.154.77:1050@qBhvJW:FtXKvBMaYs",
    "46.8.110.98:1050@qBhvJW:FtXKvBMaYs",
    "109.248.204.127:1050@qBhvJW:FtXKvBMaYs",
    "45.15.72.218:1050@qBhvJW:FtXKvBMaYs",
    '46.8.154.176:1050@qBhvJW:FtXKvBMaYs',
    '188.130.221.65:1050@qBhvJW:FtXKvBMaYs',
    '46.8.154.225:1050@qBhvJW:FtXKvBMaYs',
    '194.32.229.19:1050@qBhvJW:FtXKvBMaYs',
    '45.87.252.122:1050@qBhvJW:FtXKvBMaYs',
    '185.181.244.200:1050@qBhvJW:FtXKvBMaYs'
]

telegram_bot_token = '7017902697:AAF288DgB7XwpyHMkNA5z2hRhm5w1ghtzgs'
telegram_chat_id = '732691733'

def send_telegram_message(token, chat_id, message):
    bot = telebot.TeleBot(token)
    bot.send_message(chat_id, message)

def get_proxy_dict(proxy_str):
    ip_port, credentials = proxy_str.split('@')
    login, password = credentials.split(':')
    return f'http://{login}:{password}@{ip_port}'

async def fetch(session, url, headers, cookies, data, proxy):
    proxy_url = get_proxy_dict(proxy)
    try:
        async with session.post(url, headers=headers, cookies=cookies, data=data, proxy=proxy_url) as response:
            text = await response.text()
            if 'руб' in text:
                print(rf"Found 'рублей' in response {text}")
                send_telegram_message(telegram_bot_token, telegram_chat_id, text)
            else:
                print(rf"Did not find '50000' in response {text}")
    except Exception as e:
        print(f"An error occurred: {e}")

async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [fetch(session, url, headers, cookies, data, proxy) for proxy in proxies]
            await asyncio.gather(*tasks)
            # Delay between rounds of requests (e.g., 10 seconds)
            await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
