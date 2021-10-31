import os
from dotenv import load_dotenv
import json
import requests


class SplunkHEC:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("SPLUNK_URL")  # https://http-inputs-xxxxx.splunkcloud.com/services/collector/event
        self.key = int(os.getenv("SPLUNK_KEY"))

    def send_events(self, events):
        payload = ""

        for event in events:
            payload += str(json.dumps(event))

        self.req(payload)

    def req(self, payload):
        try:
            response = requests.post(
                self.url,
                payload,
                None,
                None,
                headers={"Authorization": "Splunk " + self.key},
            )
            response.raise_for_status()  # Raise 4xx errors
            return response
        except requests.exceptions.HTTPError as e:
            raise SystemExit(e)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
