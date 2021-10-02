# Mailgun Event Logs
[Mailgun](https://www.mailgun.com/) has a limited number of days for log retention depending on the plan. Free & Flex plan has 5 days, while the highiest plan has 30 days.
This Python script lets you archive the logs for whichever reason. It fetches [events](https://documentation.mailgun.com/en/latest/api-events.html#events) from the previous day until present, and stores them as JSON files.

## Installation
- Python 3.6+ is required. Actually I haven't tried 2.7.
- `git clone` this repo.
- Install required Python packages:
  ```
  pip3 install -r requirements.txt
  ```
- Create a folder to store the logs.
- Copy `.env.sample` to `.env` and enter your Mailgun details and log folder path.

## Usage
```
python3 get_events.py
```

## Related:
-  [medeopolis/mailgun_events_store](https://github.com/medeopolis/mailgun_events_store) - Download mailgun events and store them in Django
-  [darron/mailgun_datadog](https://github.com/darron/mailgun_datadog) - Send your Mailgun events to Datadog with this one weird trick
-  [AdrianHL/mailgun-events](https://github.com/AdrianHL/mailgun-events) - Mailgun Events Laravel Package
-  [simmatrix/golang-mailgun-statistics](https://github.com/simmatrix/golang-mailgun-statistics) - GoLang Mailgun Statistics (Events API)
-  [adig/mailgun-events-slack](https://github.com/adig/mailgun-events-slack) - Simple nodejs app that reads events(logs) from mailgun and sends them to Slack
-  [jbox-web/mailgun-rails](https://github.com/jbox-web/mailgun-rails) - Mailgun Rails provides webhook processing and event decoration to make using Mailgun with Rails much easier
-  [M-R-K-Development/Mailgun-CSV-event-export-laravel](https://github.com/M-R-K-Development/Mailgun-CSV-event-export-laravel) - A Mailgun API connector that exports events to a CSV file.
-  [Joni-Lover/mailgun_events](https://github.com/Joni-Lover/mailgun_events)
