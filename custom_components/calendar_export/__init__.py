"""The calendar_export component."""

from homeassistant.core import HomeAssistant

from .api import AnniversaryExportAPI

DOMAIN = "anniversaries_export_ics"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the anniversaries_export_ics component."""
    secret_api = ""
    
    for name, value in config[DOMAIN].items():
      if name == "secret":
        secret_api = str(value)

    hass.http.register_view(AnniversaryExportAPI(hass=hass, config = config, DOMAIN=DOMAIN))

    return True
