import caldav
from datetime import datetime
from src.config import CONFIG

class Calendar:
    def __init__(self):
        self.client = caldav.DAVClient(
            url=CONFIG["calendar"]["caldav_url"],
            # url=os.getenv("CALENDAR_CALDAV_URL"),
            # username=os.getenv("CALENDAR_CALDAV_USERNAME"),
            username=CONFIG["calendar"]["caldav_username"],
            # password=os.getenv("CALENDAR_CALDAV_PASSWORD")
            password = CONFIG["calendar"]["caldav_password"]
        )

    @staticmethod
    def can_be_loaded():
        return (bool(CONFIG["calendar"])
                and bool(CONFIG["calendar"]["caldav_url"])
                and bool(CONFIG["calendar"]["caldav_username"])
                and bool(CONFIG["calendar"]["caldav_password"]))

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

            results = calendars[0].date_search(start, end)

            for event in results:
                events.append({
                    "summary": event.instance.vevent.summary.value,
                    "start": event.instance.vevent.dtstart.value.isoformat(),
                    "end": event.instance.vevent.dtend.value.isoformat()
                })

        except Exception as e:
            return {"error": str(e)}

        return events

