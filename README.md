# Mailgun Logs
Simple Python script to save and archive your Mailgun logs. It will fetch the logs from previous day until present, and store the responses in .json  in a folder created for the month. It's best to run this via Cron at midnight.

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
python3 getlogs.py
```
