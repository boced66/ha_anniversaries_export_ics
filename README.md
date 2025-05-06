# Anniversaries Export ICS / Export des anniversaires au format ICS

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/boced66/ha_anniversaries_export_ics)](https://github.com/boced66/ha_anniversaries_export_ics/releases)
![GitHub Release Date](https://img.shields.io/github/release-date/boced66/ha_anniversaries_export_ics)
[![GitHub](https://img.shields.io/github/license/boced66/ha_anniversaries_export_ics)](LICENSE)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-brightgreen.svg)](https://github.com/boced66/ha_anniversaries_export_ics/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/boced66/ha_anniversaries_export_ics)](https://github.com/boced66/ha_anniversaries_export_ics/issues)

[![Buy me a coffee](https://img.shields.io/static/v1.svg?label=Buy%20me%20a%20coffee&logo=buy%20me%20a%20coffee&logoColor=white&labelColor=ff69b4&message=donate&color=Black)](buymeacoffee.com/boced66k)


📅 This Home Assistant integration exports anniversaries created with the [Anniversaries integration](https://github.com/pinkywafer/Anniversaries) into an iCalendar (`.ics`) file accessible via a URL.  
🇫🇷 Cette intégration Home Assistant permet d’exporter les anniversaires créés avec l’intégration [Anniversaries](https://github.com/pinkywafer/Anniversaries) vers un fichier iCalendar (`.ics`) accessible via une URL.

---

## 🔧 Installation
### HACS
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=boced66&repository=ha_anniversaries_export_ics&category=Integration)

### Manual
1. Open your Home Assistant `config` directory (where your `configuration.yaml` is).
2. If not present, create a folder named `custom_components`.
3. Inside it, create a folder named `anniversaries_export_ics`.
4. Download and copy all files from this repository's `custom_components/anniversaries_export_ics/` folder into the one you just created.
5. Restart Home Assistant.
6. Configure via YAML (see below).

---

## ⚙️ YAML Configuration

Add to your `configuration.yaml`:

```yaml
anniversaries_export_ics:
  secret: my_secret_key
  agenda_name: "Anniversaires"
  summary_format: "{friendly_name} fête ses {current_years} ans 🎉"
```

### 🔐 Parameters

| Parameter        | Required | Description |
|------------------|----------|-------------|
| `secret`         | ✅        | Secret key required in the export URL. |
| `agenda_name`    | ❌        | The calendar name shown in the ICS file. |
| `summary_format` | ❌        | Format string used for each event. You can use the placeholders listed below. |

#### Available placeholders for `summary_format`:

- `{friendly_name}`
- `{years_at_anniversary}`
- `{current_years}`
- `{date}`
- `{next_date}`
- `{weeks_remaining}`
- `{unit_of_measurement}`
- `{icon}`

## 📥 ICS URL
Once configured, your calendar will be available at:
```
https://<your-home-assistant-url>/api/anniversaries/export.ics?s=<your_secret>
```

---

## 🧭 Original Repository

This project is a **fork** of [`JosephAbbey/ha_calendar_export`](https://github.com/JosephAbbey/ha_calendar_export).

While the original project exported events from any Home Assistant calendar entity, this fork focuses specifically on the [`Anniversaries`](https://github.com/pinkywafer/Anniversaries) integration and adapts the logic to work with its sensor entities.

Many changes have been made to better support this use case.

---

## 🧭 Dépôt d'origine

Ce projet est un **fork** de [`JosephAbbey/ha_calendar_export`](https://github.com/JosephAbbey/ha_calendar_export).

Alors que le projet original permettait d’exporter les événements depuis n’importe quelle entité de type "calendar", ce fork se concentre exclusivement sur l’intégration [`Anniversaries`](https://github.com/pinkywafer/Anniversaries) et adapte la logique pour fonctionner avec les capteurs créés par celle-ci.

De nombreuses modifications ont été apportées pour mieux répondre à ce cas d’usage.


## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***


