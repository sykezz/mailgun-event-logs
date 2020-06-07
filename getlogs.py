import os
from dotenv import load_dotenv
import requests
import json
import pendulum

load_dotenv()
log_date = pendulum.yesterday("Asia/Kuala_Lumpur")

# Request logs (first page) from Mailgun
def request_logs():
    return requests.get(
        os.getenv("MAILGUN_URL") + "/v3/" + os.getenv("MAILGUN_DOMAIN") + "/events",
        auth=("api", os.getenv("MAILGUN_APIKEY")),
        params={
            "begin": pendulum.yesterday("Asia/Kuala_Lumpur").to_rfc822_string(),
            "ascending": "yes",
            "limit": 300,
        },
    )


# Request for the next page of logs
def request_page(url):
    return requests.get(url, auth=("api", os.getenv("MAILGUN_APIKEY")))


# Fetch and return all logs from Mailgun
def get_logs():
    json_data = {}
    page = 1
    response = request_logs()
    items = response.json()["items"]
    items_count = len(items)
    json_data[page] = response.json()
    next_page = response.json()["paging"]["next"]

    with open("data1.json", "w") as f:
        json.dump(response.json(), f)

    while len(items) == 300:
        response = request_page(next_page)
        items = response.json()["items"]
        items_count += len(items)
        page += 1
        json_data[page] = response.json()
        next_page = response.json()["paging"]["next"]

        with open("data2.json", "w") as f:
            json.dump(response.json(), f)

        # break;

    print(
        "Logs fetched. Total pages: " + str(len(json_data)) + ". Total items: ",
        items_count,
    )
    return json_data


# Save logs into file
def save_logs(data):
    log_date_folder = os.getenv("LOG_DIR") + "/" + log_date.format("Y-MM")
    if not os.path.exists(log_date_folder):
        os.mkdir(log_date_folder)

    with open(
        log_date_folder + "/" + pendulum.now().format("Y-MM-DD-HHmmss") + ".json", "w"
    ) as f:
        json.dump(data, f)


logs = get_logs()
save_logs(logs)
