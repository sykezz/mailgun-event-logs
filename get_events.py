import argparse
import pendulum
from mailgun_events import MailgunEvents


parser = argparse.ArgumentParser(
    description="Fetch Mailgun Events since last hour or from the previous day until present, then stores them as JSON files",
    epilog="Eg: get_events.py daily"
)
parser.add_argument(
    "type",
    help="Get event logs by daily or hourly",
    choices=["daily", "hourly"]
)
args = parser.parse_args()

if args.type == "daily":
    start_time = pendulum.yesterday()
else:  # hourly
    # Previous hour :00:00:00
    start_time = (
        pendulum.now().subtract(hours=1).replace(microsecond=0, second=0, minute=0)
    )

mgl = MailgunEvents(start_time)
mgl.get_events()
