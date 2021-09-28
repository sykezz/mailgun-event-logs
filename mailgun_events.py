import os
from dotenv import load_dotenv
import requests
import json
import pendulum
import sys


class MailgunEvents:
    def __init__(self):
        load_dotenv()
        self.log_date = pendulum.yesterday("Asia/Kuala_Lumpur")
        self.apikey = os.getenv("MAILGUN_APIKEY")
        self.domain = os.getenv("MAILGUN_DOMAIN")
        self.limit = int(os.getenv("MAILGUN_LIMIT"))
        self.log_dir = os.getenv("LOG_DIR")
        self.total_items = 0
        self.page = 0
        self.timestamp = pendulum.now().format("Y-MM-DD-HHmmss")

    # Request events (first page) from Mailgun
    def request_first_page(self):
        return requests.get(
            os.getenv("MAILGUN_URL") + "/v3/" + self.domain + "/events",
            auth=("api", self.apikey),
            params={
                "begin": self.log_date.to_rfc822_string(),
                "ascending": "yes",
                "limit": self.limit,
            },
        )

    # Request for the next page of events
    def request_next_page(self, url):
        return requests.get(url, auth=("api", self.apikey))

    # Get and return all event logs from Mailgun
    def get_events(self):

        # First page
        response = self.request_first_page()
        items = response.json()["items"]
        self.page += 1
        self.save_events(items)
        next_page = response.json()["paging"]["next"]
        self.total_items = len(items)
        sys.stdout.write(f"Events fetched ({str(len(items))}). Page: {str(self.page)}" + "\n")

        # Next pages
        while len(items) == self.limit:  # Item limit
            print("next page")
            response = self.request_next_page(next_page)
            items = response.json()["items"]
            self.page += 1
            self.save_events(items)
            next_page = response.json()["paging"]["next"]
            self.total_items += len(items)
            sys.stdout.write(f"Events fetched ({str(len(items))}). Page: {str(self.page)}" + "\n")

        sys.stdout.write(f"Done. Total pages: {str(self.page)}. Total items: {str(self.total_items)}")

    # Save event logs into file
    def save_events(self, events):
        log_dir = self.log_dir + "/" + self.log_date.format("Y-MM")
        filename = f"{self.timestamp}-{str(self.page)}.json"

        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        with open(log_dir + "/" + filename, "w") as f:
            json.dump(events, f)
