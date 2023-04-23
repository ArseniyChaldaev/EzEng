from typing import List

import requests

from constants import RAPID_API_KEY, RAPID_API_HOST


class RapidApi:
    def __init__(self):
        self.url = f"https://{RAPID_API_HOST}/language/translate/v2"
        self.headers = {
            "content-type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "application/gzip",
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": RAPID_API_HOST
        }

    def translate(self, word) -> List[str]:
        payload = f"q={word.word}&target=ru&source=en"
        response = requests.request("POST", self.url, data=payload, headers=self.headers)

        if response.status_code == 200:
            res_json = response.json()
            translations = res_json['data']['translations']
            return list(map(lambda x: x['translatedText'], translations))
        else:
            return []
