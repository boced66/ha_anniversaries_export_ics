"""The ha_anniversaries_export_ics component."""

from homeassistant.core import HomeAssistant

from .api import AnniversaryExportAPI

DOMAIN = "anniversaries_export_ics"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the anniversaries_export_ics component."""
    hass.http.register_view(
        AnniversaryExportAPI(hass=hass, config=config, domain=DOMAIN)
    )

    return True
