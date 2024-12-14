import os
from dotenv import load_dotenv
load_dotenv()
import httpx

class Login:
    def __init__(self, user_id, user_password):
        self.user_id = user_id
        self.user_password = user_password

        self.url = "https://kroko.jp/ffbattle/ffadventure.cgi"
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ja,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": "FFADV=id<>,pass<>; _ga=GA1.1.2063015341.1734162212; _ga_6SLQ5EGJRN=GS1.1.1734162456.1.1.1734162470.0.0.0; _ga_FXYKT0F1ET=GS1.1.1734167328.2.1.1734168172.0.0.0",
            "origin": "https://kroko.jp",
            "pragma": "no-cache",
            "referer": "https://kroko.jp/ffbattle/others.cgi",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

    def auth(self):
        payload = {
            "mode": "log_in",
            "id": self.user_id,
            "pass": self.user_password,
        }

        with httpx.Client() as client:
            response = client.post(self.url, headers=self.headers, data=payload)
            response.encoding = "utf-8"

            # レスポンス確認(詳細な結果を見たい人はコメントアウト外してもろて)
            # print(f"ステータスコード: {response.status_code}")
            # print(f"レスポンス本文: {response.text}")

            return response.status_code

if __name__ == "__main__":
    # IDとPWは自由に書き換えてもろて
    login = Login(
                    user_id=os.environ.get("USER_ID"),
                    user_password=os.environ.get("USER_PASSWORD")
                    )
    result = login.auth()
    print(result)
