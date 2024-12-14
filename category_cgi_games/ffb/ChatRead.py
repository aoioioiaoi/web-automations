import os
from dotenv import load_dotenv
load_dotenv()
import httpx
from bs4 import BeautifulSoup

class ChatScraper:
    def __init__(self, login_user_info, chat_channel, headers=None, cookies=None):

        self.login_user_id = login_user_info.get("id")
        self.login_user_name = login_user_info.get("name")
        self.chat_channel = chat_channel
        self.headers = headers or {}
        self.cookies = cookies or {}

    def build_url(self):

        global_ip_address = httpx.get("https://api.ipify.org?format=json").json().get("ip")
        return f"https://kroko.jp/ffbattle/chat.cgi?id={self.login_user_id}&nel={self.chat_channel}&host={global_ip_address}&name={self.login_user_name}"

    def fetch_chat_page(self):

        url = self.build_url()
        try:
            response = httpx.get(url, headers=self.headers, cookies=self.cookies, timeout=10)
            response.raise_for_status()
            response.encoding = "utf-8"
            return response.text
        except httpx.RequestError as e:
            raise RuntimeError(f"An error occurred while requesting {url}: {e}")

    def parse_chat_messages(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        chat_messages = []

        for chat_entry in soup.find_all('b'):
            user_id = chat_entry.get('title')
            user_name = chat_entry.get_text(strip=True)
            
            message_tag = chat_entry.find_next_sibling(text=True)
            message = message_tag.strip() if message_tag else None

            if user_id and user_name and message:
                chat_messages.append({
                    'user_id': user_id,
                    'username': user_name,
                    'message': message
                })

        return chat_messages

    def scrape(self):
        html = self.fetch_chat_page()
        return self.parse_chat_messages(html)

if __name__ == "__main__":

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": "https://kroko.jp/ffbattle/others.cgi",
        "Sec-CH-UA": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "iframe",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    cookies = {
        "FFADV": "id<>; pass<>"
    }

    # ここは自由に書き換えてもろて
    login_user_info = {
        "id": os.environ.get("USER_ID"),
        "name": os.environ.get("USER_NAME"),
    }
    chat_channels = ["ffb", "ffb2", "hot", "cool", "auc", "pt", "hoge"]

    scraper = ChatScraper(
                            login_user_info=login_user_info,
                            chat_channel=chat_channels[0],
                            headers=headers,
                            cookies=cookies,
                            )

    try:
        chat_messages = scraper.scrape()
        for msg in chat_messages:
            print(f"{msg['user_id']} {msg['username']} {msg['message']}")
    except RuntimeError as e:
        print(e)
