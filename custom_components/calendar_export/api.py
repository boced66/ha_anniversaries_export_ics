"""API for calendar export."""

from datetime import timedelta
from http import HTTPStatus
from homeassistant.core import HomeAssistant
from dateutil.parser import isoparse

import pytz
from aiohttp import web
from homeassistant.components import http

from icalendar import Calendar, Event

class AnniversaryExportAPI(http.HomeAssistantView):
    """View to export anniversaries in ICS format."""

    url = "/api/anniversaries/export.ics"
    name = "api:anniversaries:ics"
    requires_auth = False

    def __init__(self, secret: str, hass: HomeAssistant) -> None:
        """Initialize the iCalendar view."""
        self.secret_api = secret
        self.hass = hass
        

    async def get(self, request: web.Request):  # noqa: ANN201
        """Handle GET requests to export anniversaries in ICS format."""
        

        secret_url = request.query.get("s")
        if secret_url is None:
          secret_url = ""

        #Le secret de la configuration ne correspond pas a celui du paramètre
        if secret_url != self.secret_api:
          return web.Response(body="403: Forbidden", status=HTTPStatus.FORBIDDEN)

        #TODO : récupérer la liste des anniversaires
        anniversaries = [
            state
            for state in self.hass.states.async_all()
            if state.entity_id.startswith("sensor.")
            and state.attributes.get("attribution") == "Sensor data calculated by Anniversaries Integration"
        ]

        if not anniversaries:
            return web.Response(
                body="No anniversaries found",
                status=HTTPStatus.NOT_FOUND,
            )
        # Generate ICS data
        cal = Calendar()
        cal["X-WR-CALNAME"] = "Anniversaries"
        cal["PRODID"] = "-//Home Assistant//Calendar Export//EN"

        tz = pytz.timezone(self.hass.config.time_zone)

        for a in anniversaries:
            start = isoparse(a.attributes.get("next_date"))
            e = Event()
            e.add("uid", a.entity_id)
            e.add("summary", a.attributes.get("friendly_name"))
            e.add("dtstart", start)
            e.add("dtend", start + timedelta(days=1))
            cal.add_component(e)

        ics = cal.to_ical().decode("utf-8")

        # Return ICS data as response
        return web.Response(
            status=HTTPStatus.OK,
            body=ics,
            headers={"Content-Type": "text/calendar"},
        )

        
        
