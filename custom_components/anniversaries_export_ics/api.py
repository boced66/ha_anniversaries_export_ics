"""API for calendar export."""

from datetime import datetime, timedelta
from http import HTTPStatus

from aiohttp import web
from dateutil.relativedelta import relativedelta
from homeassistant.components import http
from homeassistant.core import HomeAssistant
from icalendar import Calendar, Event


class AnniversaryExportAPI(http.HomeAssistantView):
    """View to export anniversaries in ICS format."""

    url = "/api/anniversaries/export.ics"
    name = "api:anniversaries:ics"
    requires_auth = False
    show_last_year = False

    def __init__(self, hass: HomeAssistant, config: dict, domain: str) -> None:
        """Initialize the iCalendar view."""
        self.secret_api = ""
        self.agenda_name = "Anniversaries"
        self.summary_format = "{friendly_name} ({years_at_anniversary})"

        for name, value in config[domain].items():
            if name == "secret":
                self.secret_api = str(value)
            if name == "agenda_name":
                self.agenda_name = str(value)
            if name == "summary_format":
                self.summary_format = str(value)
            if name == "show_last_year":
                self.show_last_year = bool(value)
        self.hass = hass

    async def get(self, request: web.Request):  # noqa: ANN201
        """Handle GET requests to export anniversaries in ICS format."""
        secret_url = request.query.get("s")
        if secret_url is None:
            secret_url = ""

        # Le secret de la configuration ne correspond pas a celui du paramètre
        if secret_url != self.secret_api:
            return web.Response(body="403: Forbidden", status=HTTPStatus.FORBIDDEN)

        anniversaries = [
            state
            for state in self.hass.states.async_all()
            if state.entity_id.startswith("sensor.")
            and state.attributes.get("attribution")
            == "Sensor data calculated by Anniversaries Integration"
        ]

        if not anniversaries:
            return web.Response(
                body="No anniversaries found",
                status=HTTPStatus.NOT_FOUND,
            )
        # Generate ICS data
        cal = Calendar()
        cal["X-WR-CALNAME"] = self.agenda_name
        cal["PRODID"] = "-//Home Assistant//Calendar Export//EN"

        for a in anniversaries:
            start = a.attributes.get("next_date")
            if isinstance(start, datetime):  # on convertit en date pure
                start = start.date()

            e = Event()
            e.add("uid", a.entity_id)
            e.add(
                "summary",
                self.summary_format.format(
                    friendly_name=a.attributes.get("friendly_name"),
                    years_at_anniversary=a.attributes.get("years_at_anniversary"),
                    current_years=a.attributes.get("current_years"),
                    date=a.attributes.get("date"),
                    next_date=a.attributes.get("next_date"),
                    weeks_remaining=a.attributes.get("weeks_remaining"),
                    unit_of_measurement=a.attributes.get("unit_of_measurement"),
                    icon=a.attributes.get("icon"),
                ),
            )
            e.add("dtstart", start)
            e.add("dtend", start + timedelta(days=1))
            cal.add_component(e)

            if self.show_last_year:
                e = Event()
                e.add("uid", a.entity_id)
                e.add(
                    "summary",
                    self.summary_format.format(
                        friendly_name=a.attributes.get("friendly_name"),
                        years_at_anniversary=a.attributes.get("years_at_anniversary")
                        - 1,
                        current_years=a.attributes.get("current_years") - 1,
                        date=a.attributes.get("date") - relativedelta(years=1),
                        next_date=a.attributes.get("next_date")
                        - relativedelta(years=1),
                        weeks_remaining=a.attributes.get("weeks_remaining"),
                        unit_of_measurement=a.attributes.get("unit_of_measurement"),
                        icon=a.attributes.get("icon"),
                    ),
                )
                e.add("dtstart", start - relativedelta(years=1))
                e.add("dtend", start + timedelta(days=1) - relativedelta(years=1))
                cal.add_component(e)

        ics = cal.to_ical().decode("utf-8")

        # Return ICS data as response
        return web.Response(
            status=HTTPStatus.OK,
            body=ics,
            headers={"Content-Type": "text/calendar"},
        )
