"""
FLOW — Flood Level Observation Warning System
icons.py: Centralised SVG icon management system

All icons follow Lucide / Heroicons outline style:
  • 24×24 viewBox
  • 2px stroke-width
  • round stroke-linecap / linejoin
  • currentColor — inherits colour from CSS

Usage
-----
    from icons import icon, icon_html, ICONS

    # Inline HTML (use with st.markdown(..., unsafe_allow_html=True))
    html = icon_html("check-circle", size=18, color="#00e676")

    # As part of a label string
    label = f"{icon('camera')} Live Feed"
"""

from __future__ import annotations
from typing import Optional

# ── Raw SVG path data (24×24 viewBox) ─────────────────────────────────────────
# Each value is the inner SVG markup (paths/circles/polylines).
# All use stroke="currentColor" so colour is inherited.

_SVG_PATHS: dict[str, str] = {

    # ── Status ─────────────────────────────────────────────────────────────────
    "check-circle": (
        '<circle cx="12" cy="12" r="10"/>'
        '<polyline points="9 12 11 14 15 10"/>'
    ),
    "alert-circle": (
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="12" y1="8" x2="12" y2="12"/>'
        '<line x1="12" y1="16" x2="12.01" y2="16"/>'
    ),
    "alert-triangle": (
        '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 '
        '1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>'
        '<line x1="12" y1="9" x2="12" y2="13"/>'
        '<line x1="12" y1="17" x2="12.01" y2="17"/>'
    ),
    "info": (
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="12" y1="16" x2="12" y2="12"/>'
        '<line x1="12" y1="8" x2="12.01" y2="8"/>'
    ),
    "x-circle": (
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="15" y1="9" x2="9" y2="15"/>'
        '<line x1="9" y1="9" x2="15" y2="15"/>'
    ),
    "shield-alert": (
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'
        '<line x1="12" y1="8" x2="12" y2="12"/>'
        '<line x1="12" y1="16" x2="12.01" y2="16"/>'
    ),

    # ── Monitoring / Camera ───────────────────────────────────────────────────
    "camera": (
        '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4'
        'l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>'
        '<circle cx="12" cy="13" r="4"/>'
    ),
    "video": (
        '<polygon points="23 7 16 12 23 17 23 7"/>'
        '<rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>'
    ),
    "eye": (
        '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>'
        '<circle cx="12" cy="12" r="3"/>'
    ),
    "radio": (
        '<circle cx="12" cy="12" r="2"/>'
        '<path d="M16.24 7.76a6 6 0 0 1 0 8.49m-8.48-.01a6 6 0 0 1 0-8.49'
        'm11.31-2.82a10 10 0 0 1 0 14.14m-14.14 0a10 10 0 0 1 0-14.14"/>'
    ),

    # ── Weather / Rain ────────────────────────────────────────────────────────
    "cloud-rain": (
        '<line x1="16" y1="13" x2="16" y2="21"/>'
        '<line x1="8" y1="13" x2="8" y2="21"/>'
        '<line x1="12" y1="15" x2="12" y2="23"/>'
        '<path d="M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25"/>'
    ),
    "cloud-lightning": (
        '<path d="M19 16.9A5 5 0 0 0 18 7h-1.26a8 8 0 1 0-11.62 9"/>'
        '<polyline points="13 11 9 17 15 17 11 23"/>'
    ),
    "sun": (
        '<circle cx="12" cy="12" r="5"/>'
        '<line x1="12" y1="1" x2="12" y2="3"/>'
        '<line x1="12" y1="21" x2="12" y2="23"/>'
        '<line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>'
        '<line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>'
        '<line x1="1" y1="12" x2="3" y2="12"/>'
        '<line x1="21" y1="12" x2="23" y2="12"/>'
        '<line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>'
        '<line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>'
    ),
    "moon": (
        '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>'
    ),
    "cloud": (
        '<path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/>'
    ),
    "wind": (
        '<path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2'
        'm15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/>'
    ),
    "thermometer": (
        '<path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/>'
    ),
    "droplet": (
        '<path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>'
    ),
    "umbrella": (
        '<polyline points="23 12 22.01 12"/>'
        '<path d="M12 2a10 10 0 0 1 10 10c0-5.52-4.48-10-10-10S2 6.48 2 12'
        'a10 10 0 0 1 10-10z"/>'
        '<path d="M12 12v6a2 2 0 0 0 4 0"/>'
    ),

    # ── Water / Flood ─────────────────────────────────────────────────────────
    "waves": (
        '<path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 '
        '2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>'
        '<path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 '
        '2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>'
        '<path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 '
        '2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>'
    ),
    "gauge": (
        '<path d="M12 2a10 10 0 1 0 10 10"/>'
        '<path d="M12 6v6l4 2"/>'
    ),
    "trending-up": (
        '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>'
        '<polyline points="17 6 23 6 23 12"/>'
    ),
    "trending-down": (
        '<polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/>'
        '<polyline points="17 18 23 18 23 12"/>'
    ),
    "arrow-up": (
        '<line x1="12" y1="19" x2="12" y2="5"/>'
        '<polyline points="5 12 12 5 19 12"/>'
    ),
    "arrow-down": (
        '<line x1="12" y1="5" x2="12" y2="19"/>'
        '<polyline points="19 12 12 19 5 12"/>'
    ),
    "minus": '<line x1="5" y1="12" x2="19" y2="12"/>',

    # ── Alerts / Notifications ────────────────────────────────────────────────
    "bell": (
        '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>'
        '<path d="M13.73 21a2 2 0 0 1-3.46 0"/>'
    ),
    "bell-off": (
        '<path d="M13.73 21a2 2 0 0 1-3.46 0"/>'
        '<path d="M18.63 13A17.89 17.89 0 0 1 18 8"/>'
        '<path d="M6.26 6.26A5.86 5.86 0 0 0 6 8c0 7-3 9-3 9h14"/>'
        '<path d="M18 8a6 6 0 0 0-9.33-5"/>'
        '<line x1="1" y1="1" x2="23" y2="23"/>'
    ),
    "siren": (
        '<path d="M7 18H17"/>'
        '<path d="M7 22H17"/>'
        '<path d="M11 3L5.5 9"/>'
        '<path d="M13 3L18.5 9"/>'
        '<circle cx="12" cy="12" r="3"/>'
        '<path d="M4 18V12a8 8 0 0 1 16 0v6"/>'
    ),
    "zap": (
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>'
    ),
    "send": (
        '<line x1="22" y1="2" x2="11" y2="13"/>'
        '<polygon points="22 2 15 22 11 13 2 9 22 2"/>'
    ),
    "message-square": (
        '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'
    ),

    # ── Dashboard / Navigation ────────────────────────────────────────────────
    "layout-dashboard": (
        '<rect x="3" y="3" width="7" height="9"/>'
        '<rect x="14" y="3" width="7" height="5"/>'
        '<rect x="14" y="12" width="7" height="9"/>'
        '<rect x="3" y="16" width="7" height="5"/>'
    ),
    "bar-chart": (
        '<line x1="12" y1="20" x2="12" y2="10"/>'
        '<line x1="18" y1="20" x2="18" y2="4"/>'
        '<line x1="6" y1="20" x2="6" y2="16"/>'
    ),
    "bar-chart-2": (
        '<line x1="18" y1="20" x2="18" y2="10"/>'
        '<line x1="12" y1="20" x2="12" y2="4"/>'
        '<line x1="6" y1="20" x2="6" y2="14"/>'
    ),
    "activity": (
        '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>'
    ),
    "list": (
        '<line x1="8" y1="6" x2="21" y2="6"/>'
        '<line x1="8" y1="12" x2="21" y2="12"/>'
        '<line x1="8" y1="18" x2="21" y2="18"/>'
        '<line x1="3" y1="6" x2="3.01" y2="6"/>'
        '<line x1="3" y1="12" x2="3.01" y2="12"/>'
        '<line x1="3" y1="18" x2="3.01" y2="18"/>'
    ),

    # ── Settings / Controls ───────────────────────────────────────────────────
    "cog": (
        '<circle cx="12" cy="12" r="3"/>'
        '<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 '
        '2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 '
        '1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 '
        '1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A'
        '1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 '
        '0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 '
        '2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 '
        '1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 '
        '1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 '
        '2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 '
        '1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>'
    ),
    "sliders": (
        '<line x1="4" y1="21" x2="4" y2="14"/>'
        '<line x1="4" y1="10" x2="4" y2="3"/>'
        '<line x1="12" y1="21" x2="12" y2="12"/>'
        '<line x1="12" y1="8" x2="12" y2="3"/>'
        '<line x1="20" y1="21" x2="20" y2="16"/>'
        '<line x1="20" y1="12" x2="20" y2="3"/>'
        '<line x1="1" y1="14" x2="7" y2="14"/>'
        '<line x1="9" y1="8" x2="15" y2="8"/>'
        '<line x1="17" y1="16" x2="23" y2="16"/>'
    ),
    "target": (
        '<circle cx="12" cy="12" r="10"/>'
        '<circle cx="12" cy="12" r="6"/>'
        '<circle cx="12" cy="12" r="2"/>'
    ),
    "crosshair": (
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="22" y1="12" x2="18" y2="12"/>'
        '<line x1="6" y1="12" x2="2" y2="12"/>'
        '<line x1="12" y1="6" x2="12" y2="2"/>'
        '<line x1="12" y1="22" x2="12" y2="18"/>'
    ),
    "refresh-cw": (
        '<polyline points="23 4 23 10 17 10"/>'
        '<polyline points="1 20 1 14 7 14"/>'
        '<path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 '
        '0 0 20.49 15"/>'
    ),

    # ── Media / Playback ──────────────────────────────────────────────────────
    "play": '<polygon points="5 3 19 12 5 21 5 3"/>',
    "square": '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>',
    "pause": (
        '<rect x="6" y="4" width="4" height="16"/>'
        '<rect x="14" y="4" width="4" height="16"/>'
    ),
    "rotate-ccw": (
        '<polyline points="1 4 1 10 7 10"/>'
        '<path d="M3.51 15a9 9 0 1 0 .49-3.6"/>'
    ),

    # ── Objects / Debris ─────────────────────────────────────────────────────
    "package": (
        '<line x1="16.5" y1="9.4" x2="7.55" y2="4.24"/>'
        '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 '
        '0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>'
        '<polyline points="3.27 6.96 12 12.01 20.73 6.96"/>'
        '<line x1="12" y1="22.08" x2="12" y2="12"/>'
    ),
    "trash-2": (
        '<polyline points="3 6 5 6 21 6"/>'
        '<path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 '
        '1-1h4a1 1 0 0 1 1 1v2"/>'
        '<line x1="10" y1="11" x2="10" y2="17"/>'
        '<line x1="14" y1="11" x2="14" y2="17"/>'
    ),

    # ── Map / Location ────────────────────────────────────────────────────────
    "map-pin": (
        '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>'
        '<circle cx="12" cy="10" r="3"/>'
    ),
    "navigation": (
        '<polygon points="3 11 22 2 13 21 11 13 3 11"/>'
    ),

    # ── Data / Analytics ─────────────────────────────────────────────────────
    "database": (
        '<ellipse cx="12" cy="5" rx="9" ry="3"/>'
        '<path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>'
        '<path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>'
    ),
    "file-text": (
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
        '<line x1="16" y1="13" x2="8" y2="13"/>'
        '<line x1="16" y1="17" x2="8" y2="17"/>'
        '<polyline points="10 9 9 9 8 9"/>'
    ),
    "save": (
        '<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 '
        '0 1-2 2z"/>'
        '<polyline points="17 21 17 13 7 13 7 21"/>'
        '<polyline points="7 3 7 8 15 8"/>'
    ),
    "download": (
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        '<polyline points="7 10 12 15 17 10"/>'
        '<line x1="12" y1="15" x2="12" y2="3"/>'
    ),

    # ── Theme ─────────────────────────────────────────────────────────────────
    "sun-medium": (
        '<circle cx="12" cy="12" r="4"/>'
        '<path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41'
        'M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>'
    ),
    "moon-star": (
        '<path d="M12 3a6.364 6.364 0 0 0 9 9 9 9 0 1 1-9-9Z"/>'
        '<path d="M20 3v4M22 5h-4"/>'
    ),

    # ── Misc ──────────────────────────────────────────────────────────────────
    "users": (
        '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>'
        '<circle cx="9" cy="7" r="4"/>'
        '<path d="M23 21v-2a4 4 0 0 0-3-3.87"/>'
        '<path d="M16 3.13a4 4 0 0 1 0 7.75"/>'
    ),
    "link": (
        '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>'
        '<path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>'
    ),
    "wifi": (
        '<path d="M5 12.55a11 11 0 0 1 14.08 0"/>'
        '<path d="M1.42 9a16 16 0 0 1 21.16 0"/>'
        '<path d="M8.53 16.11a6 6 0 0 1 6.95 0"/>'
        '<line x1="12" y1="20" x2="12.01" y2="20"/>'
    ),
    "signal": (
        '<line x1="2" y1="20" x2="2" y2="14"/>'
        '<line x1="8" y1="20" x2="8" y2="8"/>'
        '<line x1="14" y1="20" x2="14" y2="4"/>'
        '<line x1="20" y1="20" x2="20" y2="2"/>'
    ),
    "edit-2": (
        '<path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>'
    ),
    "x": (
        '<line x1="18" y1="6" x2="6" y2="18"/>'
        '<line x1="6" y1="6" x2="18" y2="18"/>'
    ),
    "check": '<polyline points="20 6 9 12 4 16"/>',
    "chevron-right": '<polyline points="9 18 15 12 9 6"/>',
    "chevron-down": '<polyline points="6 9 12 15 18 9"/>',
    "polygon": (
        '<path d="M3 12 L8 4 L16 4 L21 12 L16 20 L8 20 Z"/>'
        '<circle cx="3" cy="12" r="1.5" fill="currentColor"/>'
        '<circle cx="8" cy="4" r="1.5" fill="currentColor"/>'
        '<circle cx="16" cy="4" r="1.5" fill="currentColor"/>'
        '<circle cx="21" cy="12" r="1.5" fill="currentColor"/>'
        '<circle cx="16" cy="20" r="1.5" fill="currentColor"/>'
        '<circle cx="8" cy="20" r="1.5" fill="currentColor"/>'
    ),
    "scan": (
        '<path d="M3 7V5a2 2 0 0 1 2-2h2"/>'
        '<path d="M17 3h2a2 2 0 0 1 2 2v2"/>'
        '<path d="M21 17v2a2 2 0 0 1-2 2h-2"/>'
        '<path d="M7 21H5a2 2 0 0 1-2-2v-2"/>'
        '<line x1="3" y1="12" x2="21" y2="12"/>'
    ),
    "film": (
        '<rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>'
        '<line x1="7" y1="2" x2="7" y2="22"/>'
        '<line x1="17" y1="2" x2="17" y2="22"/>'
        '<line x1="2" y1="12" x2="22" y2="12"/>'
        '<line x1="2" y1="7" x2="7" y2="7"/>'
        '<line x1="2" y1="17" x2="7" y2="17"/>'
        '<line x1="17" y1="17" x2="22" y2="17"/>'
        '<line x1="17" y1="7" x2="22" y2="7"/>'
    ),
}

# ── Public alias for the path registry ────────────────────────────────────────
ICONS = _SVG_PATHS


# ── Core renderer ─────────────────────────────────────────────────────────────
def icon_html(
    name: str,
    *,
    size: int = 16,
    color: str = "currentColor",
    stroke_width: float = 2.0,
    extra_style: str = "",
    class_: str = "",
    aria_label: Optional[str] = None,
) -> str:
    """
    Return a self-contained ``<svg>`` string for the named icon.

    Parameters
    ----------
    name         : Icon key from ICONS / _SVG_PATHS.
    size         : Square pixel size (width = height).
    color        : CSS colour string, e.g. ``"#00e676"`` or ``"var(--accent-cyan)"``.
                   Pass ``"currentColor"`` (default) to inherit from parent.
    stroke_width : SVG stroke-width attribute.
    extra_style  : Additional inline CSS appended to the ``style`` attribute.
    class_       : Optional CSS class(es) added to the ``<svg>`` element.
    aria_label   : If provided, adds ``aria-label`` and removes ``aria-hidden``.

    Returns
    -------
    str
        Raw HTML string — embed directly in f-strings passed to
        ``st.markdown(..., unsafe_allow_html=True)``.

    Example
    -------
    >>> html = icon_html("check-circle", size=18, color="#00e676")
    >>> st.markdown(f"<div>{html} Success</div>", unsafe_allow_html=True)
    """
    inner = _SVG_PATHS.get(name)
    if inner is None:
        # Graceful fallback: render a small filled circle
        inner = '<circle cx="12" cy="12" r="5" fill="currentColor"/>'

    aria = f'aria-label="{aria_label}"' if aria_label else 'aria-hidden="true"'
    cls = f'class="{class_}"' if class_ else ""
    style = (
        f"display:inline-block;vertical-align:middle;flex-shrink:0;"
        f"width:{size}px;height:{size}px;{extra_style}"
    )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
        f'width="{size}" height="{size}" '
        f'fill="none" stroke="{color}" '
        f'stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'{aria} {cls} style="{style}">'
        f"{inner}"
        f"</svg>"
    )


def icon(
    name: str,
    *,
    size: int = 16,
    color: str = "currentColor",
    stroke_width: float = 2.0,
) -> str:
    """
    Shorthand wrapper around :func:`icon_html` for use inside f-strings.

    Identical to ``icon_html`` but with fewer parameters for inline use.
    """
    return icon_html(name, size=size, color=color, stroke_width=stroke_width)


# ── Composite helpers ──────────────────────────────────────────────────────────
def status_icon(severity: str, size: int = 16) -> str:
    """
    Return the appropriate status icon HTML for a given alert severity string.

    Severity values recognised (case-insensitive):
        ``"critical"`` / ``"error"``  → alert-circle  (red)
        ``"warning"``                 → alert-triangle (orange)
        ``"info"``                    → info           (blue)
        ``"success"`` / ``"ok"``      → check-circle   (green)
    """
    s = severity.lower()
    if s in ("critical", "error", "high"):
        return icon_html("alert-circle",   size=size, color="#e74c3c")
    if s in ("warning", "medium", "moderate"):
        return icon_html("alert-triangle", size=size, color="#f39c12")
    if s in ("info", "information"):
        return icon_html("info",           size=size, color="#3498db")
    return icon_html("check-circle", size=size, color="#2ecc71")


def rain_icon(intensity: float, is_day: bool = True, size: int = 20) -> str:
    """
    Return a weather icon based on rain intensity (0.0 – 1.0).

    0.0        → sun / moon
    0.0 – 0.4  → cloud-rain (light/moderate)
    0.4 – 0.7  → cloud-rain (heavier, orange)
    0.7+       → cloud-lightning (storm, red)
    """
    if intensity <= 0.0:
        if is_day:
            return icon_html("sun",  size=size, color="#f39c12")
        return icon_html("moon", size=size, color="#7ba3cc")
    if intensity < 0.4:
        return icon_html("cloud-rain",      size=size, color="#2ecc71")
    if intensity < 0.7:
        return icon_html("cloud-rain",      size=size, color="#f39c12")
    return icon_html("cloud-lightning",     size=size, color="#e74c3c")


def water_level_icon(level_cm: Optional[float], size: int = 16) -> str:
    """
    Return a trend icon for water level.

    ``None`` or 0  → waves (neutral)
    positive rate  → trending-up
    negative rate  → trending-down
    """
    if level_cm is None:
        return icon_html("waves",        size=size, color="var(--accent-cyan)")
    if level_cm > 0:
        return icon_html("trending-up",  size=size, color="#e74c3c")
    if level_cm < 0:
        return icon_html("trending-down", size=size, color="#2ecc71")
    return icon_html("minus",            size=size, color="#7ba3cc")


def debris_icon(class_name: str, size: int = 14) -> str:
    """
    Map a YOLOv8 debris class label to an SVG icon.

    Unknown classes fall back to a generic ``package`` icon.
    """
    mapping: dict[str, str] = {
        "bottle":         "droplet",
        "plastic_waste":  "trash-2",
        "plastic":        "trash-2",
        "bag":            "package",
        "log":            "activity",
        "branch":         "activity",
        "wood":           "activity",
        "trash":          "trash-2",
        "river_debris":   "waves",
        "tire":           "rotate-ccw",
        "tyre":           "rotate-ccw",
        "can":            "package",
        "foam":           "package",
        "cloth":          "package",
        "paper":          "file-text",
        "metal":          "package",
        "glass":          "package",
        "carton":         "package",
        "styrofoam":      "package",
        "polystyrene":    "package",
        "tin":            "package",
        "aluminium":      "package",
        "aluminum":       "package",
        "food_container": "package",
        "food container": "package",
    }
    icon_name = mapping.get(class_name.lower(), "package")
    return icon_html(icon_name, size=size, color="var(--accent-cyan)")


# ── Labelled icon helper ───────────────────────────────────────────────────────
def icon_label(
    icon_name: str,
    label: str,
    *,
    size: int = 14,
    color: str = "currentColor",
    gap: int = 6,
    font_size: int = 11,
    font_weight: int = 600,
    letter_spacing: float = 1.5,
    text_transform: str = "uppercase",
    text_color: str = "var(--text-muted)",
) -> str:
    """
    Return a flex row: ``[icon] [label text]``.

    Intended for sidebar section headers and similar elements that currently
    use emoji + text patterns like ``'📷 MONITORING'``.

    Example
    -------
    >>> st.markdown(icon_label("camera", "MONITORING"), unsafe_allow_html=True)
    """
    svg = icon_html(icon_name, size=size, color=color)
    return (
        f'<div style="display:flex;align-items:center;gap:{gap}px;'
        f'font-size:{font_size}px;font-weight:{font_weight};'
        f'letter-spacing:{letter_spacing}px;text-transform:{text_transform};'
        f'color:{text_color};margin-bottom:10px;">'
        f"{svg}"
        f"<span>{label}</span>"
        f"</div>"
    )
