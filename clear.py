import requests
import time

class VKAPI:
    def __init__(self, token: str):
        self._session = requests.Session()
        self._session.headers.update({'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'})
        self.token = token
        while True:
            chat = input('Enter the chat id:\n')
            self.parse_messages(int(chat))

    def call_api(self, method: str, params: str) -> str:
        URL = f'https://api.vk.com/method/{method}?{params}&access_token={self.token}&v=5.124'
        resp = self._session.get(URL).json()
        return resp

    def parse_messages(self, user_id: int) -> list:
        messages_to_delete = []
        resp = self.call_api("messages.getHistory", f'count=200&user_id={user_id}')
        for i in resp['response']['items']:
            if i['from_id'] == 531197150:
                result = self.check_time(i['date'])
                if result < 1440:
                    messages_to_delete.append(i['id'])
        self.delete_messages(messages_to_delete)

    def check_time(self, t: int) -> int:
        return (time.time() - t) / 60

    def delete_messages(self, messages: list):
        for i in messages:
            self.call_api('messages.delete', f'message_ids={i}&delete_for_all=1')
            time.sleep(0.2)

VKAPI(input('Enter your VK token:\n'))
