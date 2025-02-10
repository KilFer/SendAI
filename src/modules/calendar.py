import caldav
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

class Calendar:
    def __init__(self):
        self.client = caldav.DAVClient(
            url=os.getenv("CALENDAR_CALDAV_URL"),
            username=os.getenv("CALENDAR_CALDAV_USERNAME"),
            password=os.getenv("CALENDAR_CALDAV_PASSWORD")
        )

    @staticmethod
    def can_be_loaded():
        return bool(os.getenv("CALENDAR_CALDAV_URL")) and bool(os.getenv("CALENDAR_CALDAV_USERNAME")) and bool(
            os.getenv("CALENDAR_CALDAV_PASSWORD"))

    def get(self):
        """
        Fetches all events for today's date from the CalDAV server.
        """
        today = datetime.today()
        start = today.replace(hour=0, minute=0, second=0)
        end = today.replace(hour=23, minute=59, second=59)

        events = []

        try:
            # Get the first available calendar
            principal = self.client.principal()
            calendars = principal.calendars()

            if not calendars:
                return {"error": "No calendars found"}

            calendar = calendars[0]  # Using the first available calendar

            # Retrieve events occurring today
            results = calendar.date_search(start, end)

            for event in results:
                events.append({
                    "summary": event.instance.vevent.summary.value,
                    "start": event.instance.vevent.dtstart.value.isoformat(),
                    "end": event.instance.vevent.dtend.value.isoformat()
                })

        except Exception as e:
            return {"error": str(e)}

        return events

