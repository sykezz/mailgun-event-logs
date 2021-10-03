import os
from dotenv import load_dotenv
import requests
import json
import pendulum
import sys


class MailgunEvents:
    def __init__(self, start_time):
        load_dotenv()
        self.start_time = start_time
        self.url = os.getenv("MAILGUN_URL", "https://api.mailgun.net")
        self.apikey = os.getenv("MAILGUN_APIKEY")
        self.domain = os.getenv("MAILGUN_DOMAIN")
        self.limit = int(os.getenv("MAILGUN_LIMIT", 300))
        self.log_dir = os.getenv("LOG_DIR")
        self.total_items = 0
        self.page = 0

    # Mailgun request handling
    def req(self, url, options={}):
        try:
            response = requests.get(url, auth=("api", self.apikey), params=options)
            response.raise_for_status()  # Raise 4xx errors
            return response
        except requests.exceptions.HTTPError as e:
            raise SystemExit(e)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    # Request events (first page) from Mailgun
    def req_first_page(self):
        response = self.req(
            self.url + "/v3/" + self.domain + "/events",
            {
                "begin": self.start_time.to_rfc822_string(),
                "ascending": "yes",
                "limit": self.limit,
            },
        )
        return response

    # Get and return all event logs from Mailgun
    def get_events(self):
        # First page
        processed = self.process_events(self.req_first_page())

        # Next pages
        while processed["count"] == self.limit:  # Item limit
            processed = self.process_events(self.req(processed["next_page"]))

        sys.stdout.write(f"Done. Total pages: {str(self.page)}. Total items: {str(self.total_items)}")

    def process_events(self, events):
        # Get items and next page token from response
        try:
            items = events.json()["items"]
            next_page = events.json()["paging"]["next"]
        except KeyError as kee:
            sys.stdout.write("No events returned.")
            sys.exit()

        self.page += 1
        self.total_items += len(items)
        self.save_events(items)
        sys.stdout.write(f"Events fetched ({str(len(items))}). Page: {str(self.page)}" + "\n")
        return {"count": len(items), "next_page": next_page}

    # Save event logs into file
    def save_events(self, events):
        timestamp = pendulum.now()
        log_dir = self.log_dir + "/" + timestamp.format("Y-MM")
        filename = f"{timestamp.format('Y-MM-DD-HHmmss')}-{str(self.page)}.json"

        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        with open(log_dir + "/" + filename, "w") as f:
            json.dump(events, f)
