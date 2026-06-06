"""
FLOW — Flood Level Observation Warning System
Weather Module: Real-time weather data via Google Maps Platform Weather API

Usage:
    from weather import WeatherService
    ws = WeatherService(latitude=6.1248, longitude=100.3673, location_name="Kangar, Perlis")
    data = ws.get_current()      # dict with all live metrics
    forecast = ws.get_forecast() # list of next 24 h hourly entries (true hourly from Google)

Google Maps Platform Weather API endpoints used:
    Current : https://weather.googleapis.com/v1/currentConditions:lookup
    Forecast: https://weather.googleapis.com/v1/forecast/hours:lookup
"""

import urllib.request
import urllib.parse
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional
from config import WEATHER_LOCATIONS, GOOGLE_WEATHER_API_KEY

try:
    import folium
    from streamlit_folium import st_folium
    _FOLIUM_AVAILABLE = True
except ImportError:
    _FOLIUM_AVAILABLE = False


# ─── Custom Location Persistence ──────────────────────────────────────────────
# Saved alongside config.py so they survive app restarts.
_CUSTOM_LOC_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "flow_custom_locations.json"
)


def _load_custom_locations() -> Dict[str, tuple]:
    """Return saved custom locations as {name: (lat, lon)}."""
    try:
        if os.path.exists(_CUSTOM_LOC_FILE):
            with open(_CUSTOM_LOC_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
            # Stored as list-of-2 for JSON; convert back to tuple
            return {k: tuple(v) for k, v in raw.items() if len(v) == 2}
    except Exception:
        pass
    return {}


def _save_custom_locations(locs: Dict[str, tuple]) -> None:
    """Persist custom locations dict to disk."""
    try:
        with open(_CUSTOM_LOC_FILE, "w", encoding="utf-8") as f:
            # Store tuples as lists (JSON-safe)
            json.dump({k: list(v) for k, v in locs.items()}, f, indent=2)
    except Exception as exc:
        print(f"[FLOW Weather] Could not save custom locations: {exc}")


def _delete_custom_location(name: str) -> None:
    """Remove a single entry from the persisted custom locations."""
    locs = _load_custom_locations()
    locs.pop(name, None)
    _save_custom_locations(locs)


def _reverse_geocode(lat: float, lon: float) -> str:
    """Return a human-readable name for coordinates using Nominatim (OSM, no key required)."""
    try:
        url = (
            "https://nominatim.openstreetmap.org/reverse"
            f"?lat={lat}&lon={lon}&format=json&zoom=14&accept-language=en"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "FLOW-FloodMonitor/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        addr = data.get("address", {})
        parts: List[str] = []
        for key in ("suburb", "city_district", "quarter", "town", "city", "county", "state"):
            val = addr.get(key, "")
            if val and val not in parts:
                parts.append(val)
                if len(parts) == 2:
                    break
        return ", ".join(parts) if parts else data.get("display_name", "")[:60]
    except Exception:
        return ""


# ─── Google Weather condition type → FLOW label + icon ───────────────────────
# Google returns a string "type" field (e.g. "CLEAR", "RAIN", "THUNDERSTORM").
# We map these to the same label/icon vocabulary the rest of FLOW already uses.

_GOOGLE_CONDITION_MAP: Dict[str, Dict] = {
    # Clear / sunny
    "CLEAR":                              {"label": "Clear Sky",              "day": "☀️",  "night": "🌙"},
    "MOSTLY_CLEAR":                       {"label": "Mainly Clear",           "day": "🌤️", "night": "🌙"},
    # Cloudy
    "PARTLY_CLOUDY":                      {"label": "Partly Cloudy",          "day": "⛅",  "night": "🌤️"},
    "MOSTLY_CLOUDY":                      {"label": "Mostly Cloudy",          "day": "☁️",  "night": "☁️"},
    "CLOUDY":                             {"label": "Overcast",               "day": "☁️",  "night": "☁️"},
    # Fog / haze
    "FOG":                                {"label": "Fog",                    "day": "🌫️", "night": "🌫️"},
    "LIGHT_FOG":                          {"label": "Light Fog",              "day": "🌫️", "night": "🌫️"},
    # Drizzle
    "DRIZZLE":                            {"label": "Light Drizzle",          "day": "🌦️", "night": "🌦️"},
    "LIGHT_RAIN_AND_WIND":                {"label": "Light Rain",             "day": "🌧️", "night": "🌧️"},
    # Rain
    "RAIN":                               {"label": "Slight Rain",            "day": "🌧️", "night": "🌧️"},
    "LIGHT_RAIN":                         {"label": "Slight Rain",            "day": "🌧️", "night": "🌧️"},
    "MODERATE_RAIN":                      {"label": "Moderate Rain",          "day": "🌧️", "night": "🌧️"},
    "HEAVY_RAIN":                         {"label": "Heavy Rain",             "day": "🌧️", "night": "🌧️"},
    "RAIN_AND_WIND":                      {"label": "Heavy Rain",             "day": "🌧️", "night": "🌧️"},
    "HEAVY_RAIN_AND_WIND":                {"label": "Heavy Rain",             "day": "🌧️", "night": "🌧️"},
    # Showers
    "SHOWERS":                            {"label": "Slight Rain",            "day": "🌦️", "night": "🌦️"},
    "HEAVY_SHOWERS":                      {"label": "Heavy Rain",             "day": "🌧️", "night": "🌧️"},
    # Freezing
    "FREEZING_DRIZZLE_FREEZING_RAIN":     {"label": "Freezing Rain",          "day": "🌨️", "night": "🌨️"},
    # Snow
    "SNOW":                               {"label": "Moderate Snow",          "day": "❄️",  "night": "❄️"},
    "LIGHT_SNOW":                         {"label": "Slight Snow",            "day": "🌨️", "night": "🌨️"},
    "HEAVY_SNOW":                         {"label": "Heavy Snow",             "day": "❄️",  "night": "❄️"},
    "SNOW_AND_WIND":                      {"label": "Heavy Snow",             "day": "❄️",  "night": "❄️"},
    "BLIZZARD":                           {"label": "Blizzard",               "day": "❄️",  "night": "❄️"},
    # Thunder — all variants mapped to ⛈️
    "THUNDERSTORM":                       {"label": "Thunderstorm",           "day": "⛈️", "night": "⛈️"},
    "THUNDERSTORM_AND_RAIN":              {"label": "Thunderstorm",           "day": "⛈️", "night": "⛈️"},
    "HEAVY_THUNDERSTORM_AND_RAIN":        {"label": "Heavy Thunderstorm",     "day": "⛈️", "night": "⛈️"},
    "LIGHT_THUNDERSTORM":                 {"label": "Light Thunderstorm",     "day": "⛈️", "night": "⛈️"},
    "LIGHT_THUNDERSTORM_RAIN":            {"label": "Light Thunderstorm Rain","day": "⛈️", "night": "⛈️"},
    "THUNDERSTORM_RAIN":                  {"label": "Thunderstorm Rain",      "day": "⛈️", "night": "⛈️"},
    "SCATTERED_THUNDERSTORMS":            {"label": "Scattered Thunderstorms","day": "⛈️", "night": "⛈️"},
    "ISOLATED_THUNDERSTORMS":             {"label": "Isolated Thunderstorms", "day": "⛈️", "night": "⛈️"},
    "THUNDERSHOWERS":                     {"label": "Thundershowers",         "day": "⛈️", "night": "⛈️"},
    "HEAVY_THUNDERSHOWERS":               {"label": "Heavy Thundershowers",   "day": "⛈️", "night": "⛈️"},
}


def _smart_condition_fallback(condition_type: str, is_day: bool) -> Dict:
    """
    Derive a sensible icon from an unmapped condition type string by scanning
    for known keywords in order of priority (most specific first).
    Returns a dict with 'label' and 'icon'.
    """
    t = condition_type.upper()

    # Thunder takes priority over everything else
    if "THUNDER" in t or "LIGHTNING" in t or "STORM" in t:
        icon = "⛈️"
        label = condition_type.replace("_", " ").title()
        return {"label": label, "icon": icon}
    if "BLIZZARD" in t or "SNOW" in t or "SLEET" in t or "HAIL" in t or "ICE" in t or "FREEZE" in t or "FREEZ" in t:
        return {"label": condition_type.replace("_", " ").title(), "icon": "❄️"}
    if "SHOWER" in t or "HEAVY_RAIN" in t or "DOWNPOUR" in t:
        return {"label": condition_type.replace("_", " ").title(), "icon": "🌧️"}
    if "RAIN" in t or "DRIZZLE" in t or "PRECIP" in t:
        return {"label": condition_type.replace("_", " ").title(), "icon": "🌧️"}
    if "FOG" in t or "MIST" in t or "HAZE" in t or "SMOKE" in t or "DUST" in t or "SAND" in t:
        return {"label": condition_type.replace("_", " ").title(), "icon": "🌫️"}
    if "CLOUD" in t or "OVERCAST" in t:
        return {"label": condition_type.replace("_", " ").title(), "icon": "☁️"}
    if "WIND" in t or "GUST" in t or "BREEZY" in t or "SQUALL" in t or "TORNADO" in t or "HURRICANE" in t:
        return {"label": condition_type.replace("_", " ").title(), "icon": "💨"}
    if "CLEAR" in t or "SUNNY" in t or "FAIR" in t:
        day_icon = "☀️" if is_day else "🌙"
        return {"label": condition_type.replace("_", " ").title(), "icon": day_icon}
    # Generic cloudy fallback if nothing matched
    return {"label": condition_type.replace("_", " ").title(), "icon": "🌤️" if is_day else "🌙"}


def _google_condition(condition_type: str, is_day: bool) -> Dict:
    """Map a Google Weather condition type string to a label + icon dict."""
    entry = _GOOGLE_CONDITION_MAP.get(condition_type.upper())
    if entry:
        return {"label": entry["label"], "icon": entry["day"] if is_day else entry["night"]}
    # Smart keyword-based fallback — never returns the thermometer 🌡️
    return _smart_condition_fallback(condition_type, is_day)


def rain_intensity_to_category(intensity: float) -> str:
    """
    Map a normalised rain intensity (0-1) to a human-readable category name
    that matches the WMO-style labels used by the live weather sidebar.

    0.00              → "No Rain"
    0.001 – 0.199     → "Light Drizzle"
    0.200 – 0.399     → "Slight Rain"
    0.400 – 0.599     → "Moderate Rain"
    0.600 – 0.799     → "Heavy Rain"
    0.800 – 1.000     → "Violent Showers"
    """
    if intensity <= 0.0:
        return "No Rain"
    elif intensity < 0.2:
        return "Light Drizzle"
    elif intensity < 0.4:
        return "Slight Rain"
    elif intensity < 0.6:
        return "Moderate Rain"
    elif intensity < 0.8:
        return "Heavy Rain"
    else:
        return "Violent Showers"


def _rain_to_intensity(mm_per_hour: float) -> float:
    """
    Convert rainfall (mm/h) to a 0-1 normalised intensity value
    compatible with FLOW's FloodPredictor and AlertManager.

    Scale (typical tropical reference):
        0       mm/h  → 0.00  (dry)
        2.5     mm/h  → 0.25  (light rain)
        7.5     mm/h  → 0.50  (moderate)
        15      mm/h  → 0.75  (heavy)
        25+     mm/h  → 1.00  (extreme / flash-flood territory)
    """
    return round(min(1.0, mm_per_hour / 25.0), 4)


class WeatherService:
    """
    Fetches current conditions and hourly forecast from the Google Maps Platform
    Weather API.  Results are cached for `cache_ttl` seconds to avoid hammering
    the API on every Streamlit rerender.

    Google Weather API endpoints used:
        Current  : https://weather.googleapis.com/v1/currentConditions:lookup
        Forecast : https://weather.googleapis.com/v1/forecast/hours:lookup

    The public interface (get_current, get_forecast, rain_intensity,
    update_location, force_refresh, last_error, is_stale) is identical to the
    previous OpenWeatherMap implementation so the rest of FLOW needs no changes.

    Parameters
    ----------
    latitude, longitude : Monitoring site coordinates.
    location_name       : Human-readable name shown in the UI.
    cache_ttl           : Seconds to cache results (default: 300 = 5 min).
    api_key             : Google Maps API key (defaults to GOOGLE_WEATHER_API_KEY).
    """

    CURRENT_URL  = "https://weather.googleapis.com/v1/currentConditions:lookup"
    FORECAST_URL = "https://weather.googleapis.com/v1/forecast/hours:lookup"

    def __init__(
        self,
        latitude: float = 6.1248,
        longitude: float = 100.3673,
        location_name: str = "Monitoring Site",
        cache_ttl: int = 300,
        api_key: str = GOOGLE_WEATHER_API_KEY,
    ):
        self.latitude      = latitude
        self.longitude     = longitude
        self.location_name = location_name
        self.cache_ttl     = cache_ttl
        self._api_key      = api_key

        self._current_cache:  Optional[Dict]       = None
        self._forecast_cache: Optional[List[Dict]] = None
        self._last_fetch:     float                = 0.0
        self._fetch_error:    Optional[str]        = None

    # ─── Public API ───────────────────────────────────────────────────────────

    def get_current(self) -> Dict:
        """
        Return current weather conditions as a flat dict:
            temperature      float   °C
            feels_like       float   °C
            humidity         float   %
            wind_speed       float   km/h
            wind_direction   int     °
            rain_mm          float   mm/h  (last-1h value from OWM, treated as mm/h)
            rain_intensity   float   0-1   (normalised, ready for FloodPredictor)
            condition_label  str
            condition_icon   str
            weather_code     int     (OWM condition ID)
            is_day           bool
            timestamp        str     ISO-8601
            location         str
            error            str | None
        """
        self._maybe_refresh()
        if self._current_cache:
            return self._current_cache
        return self._error_payload()

    def get_forecast(self, hours: int = 24) -> List[Dict]:
        """
        Return a list of forecast dicts for approximately the next `hours` hours.
        Google Weather API returns true hourly data; each dict has:
            time, temperature, rain_mm, rain_intensity,
            condition_label, condition_icon, wind_speed, humidity.
        """
        self._maybe_refresh()
        if self._forecast_cache:
            return self._forecast_cache[:hours]
        return []

    def rain_intensity(self) -> float:
        """Shortcut: just the normalised rain intensity (0-1), safe to call often."""
        return self.get_current().get("rain_intensity", 0.0)

    @property
    def last_error(self) -> Optional[str]:
        return self._fetch_error

    @property
    def is_stale(self) -> bool:
        return (time.time() - self._last_fetch) > self.cache_ttl * 2

    def force_refresh(self):
        """Bypass cache and fetch fresh data immediately."""
        self._last_fetch = 0.0
        self._maybe_refresh()

    def update_location(self, latitude: float, longitude: float, location_name: str):
        """
        Switch to a new monitoring location and immediately invalidate the cache
        so the next call to get_current() / get_forecast() fetches fresh data.
        """
        if (
            self.latitude      != latitude
            or self.longitude  != longitude
            or self.location_name != location_name
        ):
            self.latitude      = latitude
            self.longitude     = longitude
            self.location_name = location_name
            self._current_cache  = None
            self._forecast_cache = None
            self._last_fetch     = 0.0
            self._fetch_error    = None

    # ─── Internal ─────────────────────────────────────────────────────────────

    def _maybe_refresh(self):
        """Fetch from API only when cache has expired."""
        if (time.time() - self._last_fetch) < self.cache_ttl:
            return
        try:
            self._fetch()
            self._fetch_error = None
        except Exception as exc:
            self._fetch_error = str(exc)
            print(f"[FLOW Weather] Fetch failed: {exc}")

    def _build_url(self, base: str, extra: dict = None) -> str:
        """Build a Google Weather API URL with location and key parameters."""
        params = {
            "location.latitude":  self.latitude,
            "location.longitude": self.longitude,
            "key":                self._api_key,
            "unitsSystem":        "METRIC",
            "languageCode":       "en",
        }
        if extra:
            params.update(extra)
        return f"{base}?{urllib.parse.urlencode(params)}"

    def _fetch_json(self, url: str) -> Dict:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "FLOW-FloodMonitor/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())

    def _fetch(self):
        """Fetch current + forecast from Google Weather API and populate both caches."""
        current_url  = self._build_url(self.CURRENT_URL)
        forecast_url = self._build_url(self.FORECAST_URL, {"hours": 24})  # true hourly, 24 h

        current_raw  = self._fetch_json(current_url)
        forecast_raw = self._fetch_json(forecast_url)

        self._parse_current(current_raw)
        self._parse_forecast(forecast_raw)
        self._last_fetch = time.time()

    def _parse_current(self, raw: Dict):
        """Parse Google Weather API /currentConditions:lookup response."""
        is_day = bool(raw.get("isDaytime", True))

        # Condition
        weather_cond = raw.get("weatherCondition", {})
        cond_type    = weather_cond.get("type", "CLEAR")
        cond         = _google_condition(cond_type, is_day)

        # Temperature (Google returns nested {degrees, unit})
        temp_obj       = raw.get("temperature",        {"degrees": 0})
        feels_obj      = raw.get("feelsLikeTemperature", {"degrees": 0})
        humidity       = float(raw.get("relativeHumidity", 0) or 0)

        # Wind (Google: windSpeed in km/h when unitsSystem=METRIC)
        wind_obj  = raw.get("wind", {})
        wind_kmh  = round(float(wind_obj.get("speed", {}).get("value", 0) or 0), 1)
        wind_deg  = int(wind_obj.get("direction", {}).get("degrees", 0) or 0)

        # Precipitation (Google: precipitation.qpf.quantity = mm accumulated over past hour)
        precip    = raw.get("precipitation", {})
        qpf_obj   = precip.get("qpf", {"quantity": 0})
        rain_mm   = float(qpf_obj.get("quantity", 0) or 0)

        # Timestamp (ISO-8601 string from Google)
        ts_raw = raw.get("currentTime", datetime.utcnow().isoformat() + "Z")
        try:
            ts_iso = datetime.fromisoformat(ts_raw.rstrip("Z")).isoformat()
        except Exception:
            ts_iso = datetime.now().isoformat()

        self._current_cache = {
            "temperature":     round(float(temp_obj.get("degrees",  0)), 1),
            "feels_like":      round(float(feels_obj.get("degrees", 0)), 1),
            "humidity":        round(humidity, 1),
            "wind_speed":      wind_kmh,
            "wind_direction":  wind_deg,
            "rain_mm":         round(rain_mm, 2),
            "rain_intensity":  _rain_to_intensity(rain_mm),
            "condition_label": cond["label"],
            "condition_icon":  cond["icon"],
            "weather_code":    0,          # Google doesn't use numeric codes; kept for compat
            "is_day":          is_day,
            "timestamp":       ts_iso,
            "location":        self.location_name,
            "error":           None,
        }

    def _parse_forecast(self, raw: Dict):
        """Parse Google Weather API /forecast/hours:lookup response (true hourly)."""
        entries = []

        for item in raw.get("forecastHours", []):
            # Google timestamp is an ISO-8601 string
            ts_raw = item.get("interval", {}).get("startTime", "")
            try:
                dt_obj = datetime.fromisoformat(ts_raw.rstrip("Z"))
            except Exception:
                continue

            is_day_f = 6 <= dt_obj.hour < 20
            weather_cond = item.get("weatherCondition", {})
            cond_type    = weather_cond.get("type", "CLEAR")
            cond         = _google_condition(cond_type, is_day_f)

            temp_obj  = item.get("temperature",     {"degrees": 0})
            hum       = float(item.get("relativeHumidity", 0) or 0)
            wind_obj  = item.get("wind", {})
            wind_kmh  = round(float(wind_obj.get("speed", {}).get("value", 0) or 0), 1)

            precip    = item.get("precipitation", {})
            qpf_obj   = precip.get("qpf", {"quantity": 0})
            rain_mm   = float(qpf_obj.get("quantity", 0) or 0)

            entries.append({
                "time":            dt_obj.strftime("%Y-%m-%dT%H:%M"),
                "temperature":     round(float(temp_obj.get("degrees", 0)), 1),
                "humidity":        round(hum, 1),
                "rain_mm":         round(rain_mm, 2),
                "rain_intensity":  _rain_to_intensity(rain_mm),
                "condition_label": cond["label"],
                "condition_icon":  cond["icon"],
                "wind_speed":      wind_kmh,
            })

        self._forecast_cache = entries

    @staticmethod
    def _error_payload() -> Dict:
        return {
            "temperature": 0, "feels_like": 0, "humidity": 0,
            "wind_speed": 0, "wind_direction": 0,
            "rain_mm": 0.0, "rain_intensity": 0.0,
            "condition_label": "Unavailable", "condition_icon": "⚠️",
            "weather_code": -1, "is_day": True,
            "timestamp": datetime.now().isoformat(),
            "location": "Unknown", "error": "Weather data unavailable",
        }


# ─── Streamlit UI helpers ──────────────────────────────────────────────────────

def render_weather_sidebar(ws: WeatherService):
    """
    Call inside a `with st.sidebar:` block to render the compact weather widget.
    Requires `import streamlit as st` in the calling module.
    """
    import streamlit as st

    st.markdown('<div class="sidebar-label">🌤️ LIVE WEATHER</div>', unsafe_allow_html=True)

    # ── Build merged location list ─────────────────────────────────────────────
    # Order: "📍 Custom Location" first, then user-saved customs, then presets.
    custom_locs  = _load_custom_locations()           # {name: (lat, lon)}
    preset_locs  = {k: v for k, v in WEATHER_LOCATIONS.items() if k != "📍 Custom Location"}

    # Full ordered dict for the selectbox
    all_locations: Dict[str, tuple] = {"📍 Custom Location": None}
    all_locations.update(custom_locs)
    all_locations.update(preset_locs)

    location_names = list(all_locations.keys())

    # Work out which index to pre-select
    current_name = ws.location_name
    default_idx  = 0
    for i, name in enumerate(location_names):
        if name == current_name:
            default_idx = i
            break

    # ── Location selectbox + delete button for saved custom entries ────────────
    # Show a delete (✕) button next to the selectbox only when the active
    # selection is a user-saved custom location (not a built-in preset).
    selected_is_custom_saved = (
        current_name in custom_locs and current_name in location_names
    )

    if selected_is_custom_saved:
        sel_col, del_col = st.columns([5, 1])
        with sel_col:
            chosen_name = st.selectbox(
                "📌 Location",
                location_names,
                index=default_idx,
                key="weather_location_select",
                help="Choose a preset, a saved custom location, or '📍 Custom Location' to add a new one.",
            )
        with del_col:
            st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
            if st.button("✕", key="weather_delete_btn", help=f"Remove '{current_name}' from saved locations"):
                _delete_custom_location(current_name)
                # Fall back to first preset after deletion
                first_preset = next(iter(preset_locs), None)
                if first_preset:
                    lat, lon = preset_locs[first_preset]
                    ws.update_location(lat, lon, first_preset)
                st.rerun()
    else:
        chosen_name = st.selectbox(
            "📌 Location",
            location_names,
            index=default_idx,
            key="weather_location_select",
            help="Choose a preset, a saved custom location, or '📍 Custom Location' to add a new one.",
        )

    coords = all_locations[chosen_name]

    if coords is None:
        # ── Map-based location picker ──────────────────────────────────────────
        if "flow_map_lat" not in st.session_state:
            st.session_state.flow_map_lat = ws.latitude
        if "flow_map_lon" not in st.session_state:
            st.session_state.flow_map_lon = ws.longitude
        if "flow_map_geocoded_for" not in st.session_state:
            st.session_state.flow_map_geocoded_for = None

        _mlat = st.session_state.flow_map_lat
        _mlon = st.session_state.flow_map_lon

        if _FOLIUM_AVAILABLE:
            st.caption("🗺️ Click anywhere on the map to select a location")
            _m = folium.Map(location=[_mlat, _mlon], zoom_start=7, tiles="OpenStreetMap")
            folium.Marker(
                location=[_mlat, _mlon],
                tooltip=f"📍 {_mlat:.4f}°, {_mlon:.4f}°",
                icon=folium.Icon(color="red", icon="info-sign"),
            ).add_to(_m)
            _map_data = st_folium(
                _m,
                key="flow_location_map",
                height=310,
                returned_objects=["last_clicked"],
            )
            if _map_data and _map_data.get("last_clicked"):
                _click = _map_data["last_clicked"]
                _new_lat = round(float(_click["lat"]), 6)
                _new_lon = round(float(_click["lng"]), 6)
                if abs(_new_lat - _mlat) > 1e-5 or abs(_new_lon - _mlon) > 1e-5:
                    st.session_state.flow_map_lat = _new_lat
                    st.session_state.flow_map_lon = _new_lon
                    st.session_state.flow_map_geocoded_for = None
                    st.rerun()
        else:
            st.info("Install `folium` & `streamlit-folium` to enable map selection.")
            _c1, _c2 = st.columns(2)
            with _c1:
                _new_lat = st.number_input(
                    "Latitude", value=_mlat,
                    min_value=-90.0, max_value=90.0,
                    format="%.6f", key="weather_custom_lat",
                )
            with _c2:
                _new_lon = st.number_input(
                    "Longitude", value=_mlon,
                    min_value=-180.0, max_value=180.0,
                    format="%.6f", key="weather_custom_lon",
                )
            if abs(_new_lat - _mlat) > 1e-6 or abs(_new_lon - _mlon) > 1e-6:
                st.session_state.flow_map_lat = _new_lat
                st.session_state.flow_map_lon = _new_lon
                st.session_state.flow_map_geocoded_for = None
                st.rerun()

        # Reverse-geocode when coordinates change (only runs once per new location)
        _geo_key = (st.session_state.flow_map_lat, st.session_state.flow_map_lon)
        if st.session_state.flow_map_geocoded_for != _geo_key:
            _geocoded = _reverse_geocode(
                st.session_state.flow_map_lat,
                st.session_state.flow_map_lon,
            )
            st.session_state.flow_map_geocoded_for = _geo_key
            st.session_state["weather_custom_name"] = _geocoded

        # Confirmation panel
        st.markdown(f"""
<div style="background:rgba(0,180,255,0.07);border:1px solid rgba(0,180,255,0.18);
     border-radius:8px;padding:8px 10px;margin:6px 0 4px;">
  <div style="font-size:10px;color:var(--text-muted);letter-spacing:1px;margin-bottom:6px;">
    📍 SELECTED COORDINATES
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;font-size:12px;">
    <div>
      <div style="font-size:10px;color:var(--text-muted);">Latitude</div>
      <div style="font-weight:700;color:var(--accent-cyan);">
        {st.session_state.flow_map_lat:.6f}°
      </div>
    </div>
    <div>
      <div style="font-size:10px;color:var(--text-muted);">Longitude</div>
      <div style="font-weight:700;color:var(--accent-cyan);">
        {st.session_state.flow_map_lon:.6f}°
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

        custom_label = st.text_input(
            "Location Name",
            key="weather_custom_name",
            placeholder="e.g. My River Site",
        )

        _btn_apply, _btn_save = st.columns(2)
        with _btn_apply:
            if st.button("🔄 Apply", use_container_width=True, key="weather_apply_btn",
                         help="Use this location now without saving"):
                ws.update_location(
                    st.session_state.flow_map_lat,
                    st.session_state.flow_map_lon,
                    custom_label.strip() or "Custom Location",
                )
                st.rerun()
        with _btn_save:
            if st.button("💾 Save", use_container_width=True, key="weather_save_btn",
                         help="Save permanently to the location list"):
                label = custom_label.strip() or "Custom Location"
                locs  = _load_custom_locations()
                locs[label] = (
                    st.session_state.flow_map_lat,
                    st.session_state.flow_map_lon,
                )
                _save_custom_locations(locs)
                ws.update_location(
                    st.session_state.flow_map_lat,
                    st.session_state.flow_map_lon,
                    label,
                )
                st.rerun()
    else:
        lat, lon = coords
        ws.update_location(lat, lon, chosen_name)

    w   = ws.get_current()
    err = w.get("error") or ws.last_error

    if err and w["weather_code"] == -1:
        st.warning(f"Weather unavailable: {err}")
        return

    # ── Main condition card ────────────────────────────────────────────────────
    rain_color = "#e74c3c" if w["rain_intensity"] >= 0.75 else \
                 "#f39c12" if w["rain_intensity"] >= 0.40 else "#2ecc71"

    st.markdown(f"""
<div style="background:rgba(0,180,255,0.07);border:1px solid rgba(0,180,255,0.18);
     border-radius:10px;padding:12px 14px;margin-bottom:10px;">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
    <span style="font-size:28px;line-height:1;">{w['condition_icon']}</span>
    <div>
      <div style="font-size:13px;font-weight:700;color:var(--text-primary);">
        {w['condition_label']}
      </div>
      <div style="font-size:10px;color:var(--text-muted);">{w['location']}</div>
    </div>
    <div style="margin-left:auto;text-align:right;">
      <div style="font-size:22px;font-weight:800;color:var(--accent-cyan);">
        {w['temperature']}°C
      </div>
      <div style="font-size:10px;color:var(--text-muted);">
        Feels {w['feels_like']}°C
      </div>
    </div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:11px;color:var(--text-secondary);">
    <div>💧 Humidity: <strong>{w['humidity']}%</strong></div>
    <div>💨 Wind: <strong>{w['wind_speed']} km/h</strong></div>
    <div>🌧️ Rain: <strong>{w['rain_mm']} mm/h</strong></div>
    <div style="color:{rain_color};">
      ⚡ Intensity: <strong>{w['rain_intensity']:.2f}</strong>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── 24-HOUR FORECAST — horizontal scrollable with NOW marker ───────────────
    forecast = ws.get_forecast(hours=24)
    if forecast:
        st.markdown(
            '<div style="font-size:10px;color:var(--text-muted);'
            'letter-spacing:1px;margin:8px 0 4px;">24-HOUR FORECAST</div>',
            unsafe_allow_html=True,
        )

        # Determine current hour string "HH:MM" to match against forecast slots
        now_label = datetime.now().strftime("%H:%M")
        # Find the closest forecast slot to now
        now_hour  = datetime.now().hour
        now_idx   = 0
        for _i, _h in enumerate(forecast):
            try:
                _slot_hour = int(_h["time"][-5:].split(":")[0])
                if _slot_hour == now_hour:
                    now_idx = _i
                    break
            except Exception:
                pass

        # Build one vertical card per hour for horizontal layout
        cards_html = ""
        for idx, h in enumerate(forecast):
            hour_label = h["time"][-5:]   # "HH:MM"
            is_now     = (idx == now_idx)
            rain_col   = (
                "#e74c3c" if h["rain_intensity"] >= 0.75 else
                "#f39c12" if h["rain_intensity"] >= 0.40 else
                "#3498db" if h["rain_mm"] > 0 else
                "var(--text-muted)"
            )

            if is_now:
                # Highlighted NOW card
                now_marker = '<div style="font-size:9px;font-weight:800;color:#fff;background:#00b4ff;border-radius:4px;padding:1px 5px;text-align:center;letter-spacing:1px;margin-bottom:4px;">NOW</div>'
                card_border = "border:1.5px solid #00b4ff;background:rgba(0,180,255,0.18);"
                time_color  = "#00d4ff"
                temp_color  = "#00d4ff"
            else:
                now_marker  = ""
                card_border = "border:1px solid rgba(0,180,255,0.12);background:rgba(0,180,255,0.04);"
                time_color  = "var(--text-primary)"
                temp_color  = "var(--accent-cyan)"

            cards_html += f"""
<div style="display:inline-flex;flex-direction:column;align-items:center;
            min-width:62px;max-width:62px;
            padding:8px 4px 6px;
            border-radius:8px;
            {card_border}
            margin-right:5px;flex-shrink:0;vertical-align:top;">
  {now_marker}
  <div style="font-size:11px;font-weight:600;color:{time_color};
              margin-bottom:5px;white-space:nowrap;">{hour_label}</div>
  <div style="font-size:20px;line-height:1;margin-bottom:4px;">{h['condition_icon']}</div>
  <div style="font-size:10px;color:var(--text-secondary);text-align:center;
              white-space:normal;line-height:1.2;margin-bottom:5px;
              min-height:28px;">{h['condition_label']}</div>
  <div style="font-size:12px;font-weight:700;color:{temp_color};
              margin-bottom:3px;">{h['temperature']}°C</div>
  <div style="font-size:10px;color:{rain_col};">{h['rain_mm']}mm</div>
</div>"""

        st.markdown(f"""
<div style="background:rgba(0,180,255,0.04);
            border:1px solid rgba(0,180,255,0.15);
            border-radius:8px;
            overflow-x:auto;
            overflow-y:hidden;
            padding:10px 8px 8px;
            white-space:nowrap;
            scrollbar-width:thin;
            scrollbar-color:rgba(0,180,255,0.3) transparent;">
  {cards_html}
</div>
""", unsafe_allow_html=True)

    # ── Stale data warning ─────────────────────────────────────────────────────
    if ws.is_stale:
        st.warning("⚠ Weather data is stale — check internet connection.")
    else:
        fetched_at = datetime.fromtimestamp(ws._last_fetch).strftime("%H:%M")
        st.caption(f"Updated {fetched_at} · Refreshes every 5 min · Google Weather API")


def render_weather_main_panel(ws: WeatherService):
    """
    Render an expanded weather card for the main dashboard area.
    Call inside any st.container() or column.
    """
    import streamlit as st

    w        = ws.get_current()
    forecast = ws.get_forecast(hours=24)

    st.markdown("#### 🌤️ Real-Time Weather & Forecast")

    col_a, col_b, col_c, col_d = st.columns(4)
    metrics = [
        (col_a, "🌡️ Temperature",  f"{w['temperature']}°C",  f"Feels {w['feels_like']}°C"),
        (col_b, "💧 Humidity",      f"{w['humidity']}%",       "Relative"),
        (col_c, "💨 Wind Speed",    f"{w['wind_speed']} km/h", f"{w['wind_direction']}° bearing"),
        (col_d, "🌧️ Rain Rate",    f"{w['rain_mm']} mm/h",    f"Intensity {w['rain_intensity']:.2f}"),
    ]
    for col, label, val, delta in metrics:
        with col:
            st.metric(label, val, delta)

    if forecast:
        import pandas as pd
        df = pd.DataFrame(forecast[:24])
        df["hour"] = df["time"].str[-5:]
        df = df.set_index("hour")
        st.line_chart(
            df[["temperature", "rain_mm"]].rename(
                columns={"temperature": "Temp (°C)", "rain_mm": "Rain (mm/h)"}
            ),
            use_container_width=True,
            height=180,
        )
