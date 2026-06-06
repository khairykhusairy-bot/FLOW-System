"""
FLOW — Flood Level Observation Warning System
Database Module: SQLite logging for monitoring data
"""

import sqlite3
import csv
import os
from datetime import datetime
from typing import List, Dict, Optional

DB_PATH = "flow_monitoring.db"


def init_db():
    """Initialize the SQLite database and create tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            bottles INTEGER DEFAULT 0,
            plastic_waste INTEGER DEFAULT 0,
            logs_count INTEGER DEFAULT 0,
            branches INTEGER DEFAULT 0,
            trash INTEGER DEFAULT 0,
            total_roi_objects INTEGER DEFAULT 0,
            blockage_percentage REAL DEFAULT 0.0,
            rain_intensity TEXT DEFAULT 'No Rain',
            rain_intensity_value REAL DEFAULT 0.0,
            humidity REAL DEFAULT NULL,
            wind_speed REAL DEFAULT NULL,
            temperature REAL DEFAULT NULL,
            feels_like REAL DEFAULT NULL,
            flood_risk TEXT DEFAULT 'Low Risk',
            confidence REAL DEFAULT 0.0,
            alert_triggered INTEGER DEFAULT 0,
            alert_message TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)

    # ── Migration: add new columns to existing databases ──────────────────────
    existing_cols = {row[1] for row in cursor.execute("PRAGMA table_info(monitoring_logs)")}
    migrations = {
        "humidity":             "ALTER TABLE monitoring_logs ADD COLUMN humidity             REAL DEFAULT NULL",
        "wind_speed":           "ALTER TABLE monitoring_logs ADD COLUMN wind_speed           REAL DEFAULT NULL",
        "temperature":          "ALTER TABLE monitoring_logs ADD COLUMN temperature          REAL DEFAULT NULL",
        "feels_like":           "ALTER TABLE monitoring_logs ADD COLUMN feels_like           REAL DEFAULT NULL",
        "rain_intensity_value": "ALTER TABLE monitoring_logs ADD COLUMN rain_intensity_value REAL DEFAULT 0.0",
        # Water level columns (added by water_level module)
        "water_level_cm":       "ALTER TABLE monitoring_logs ADD COLUMN water_level_cm      REAL DEFAULT NULL",
        "water_level_trend":    "ALTER TABLE monitoring_logs ADD COLUMN water_level_trend   TEXT DEFAULT NULL",
        "water_level_status":   "ALTER TABLE monitoring_logs ADD COLUMN water_level_status  TEXT DEFAULT NULL",
        "water_rise_rate":      "ALTER TABLE monitoring_logs ADD COLUMN water_rise_rate     REAL DEFAULT NULL",
        "location":             "ALTER TABLE monitoring_logs ADD COLUMN location            TEXT DEFAULT ''",
    }
    for col, sql in migrations.items():
        if col not in existing_cols:
            cursor.execute(sql)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alert_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            message TEXT NOT NULL,
            severity TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def log_monitoring_data(data: Dict):
    """Insert a monitoring snapshot into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO monitoring_logs (
            timestamp, bottles, plastic_waste, logs_count, branches, trash,
            total_roi_objects, blockage_percentage, rain_intensity, rain_intensity_value,
            humidity, wind_speed, temperature, feels_like,
            flood_risk, confidence, alert_triggered, alert_message,
            water_level_cm, water_level_trend, water_level_status, water_rise_rate,
            location
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("timestamp", datetime.now().isoformat()),
        data.get("bottles", 0),
        data.get("plastic_waste", 0),
        data.get("logs_count", 0),
        data.get("branches", 0),
        data.get("trash", 0),
        data.get("total_roi_objects", 0),
        data.get("blockage_percentage", 0.0),
        data.get("rain_intensity", "No Rain"),
        data.get("rain_intensity_value", 0.0),
        data.get("humidity", None),
        data.get("wind_speed", None),
        data.get("temperature", None),
        data.get("feels_like", None),
        data.get("flood_risk", "Low Risk"),
        data.get("confidence", 0.0),
        int(data.get("alert_triggered", False)),
        data.get("alert_message", ""),
        data.get("water_level_cm", None),
        data.get("water_level_trend", None),
        data.get("water_level_status", None),
        data.get("water_rise_rate", None),
        data.get("location", ""),
    ))
    conn.commit()
    conn.close()


def log_alert(alert_type: str, message: str, severity: str):
    """Log an alert event."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alert_history (timestamp, alert_type, message, severity)
        VALUES (?, ?, ?, ?)
    """, (datetime.now().isoformat(), alert_type, message, severity))
    conn.commit()
    conn.close()


def get_recent_logs(limit: int = 50) -> List[Dict]:
    """Retrieve recent monitoring logs."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM monitoring_logs
        ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_recent_alerts(limit: int = 20) -> List[Dict]:
    """Retrieve recent alerts."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM alert_history
        ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def export_to_csv(filepath: str = "flow_export.csv"):
    """Export all monitoring logs to CSV."""
    logs = get_recent_logs(limit=10000)
    if not logs:
        return False
    fieldnames = list(logs[0].keys())
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(logs)
    return True


def get_stats_summary() -> Dict:
    """Get aggregate statistics from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            COUNT(*) as total_records,
            AVG(blockage_percentage) as avg_blockage,
            MAX(blockage_percentage) as max_blockage,
            AVG(rain_intensity_value) as avg_rain,
            SUM(alert_triggered) as total_alerts
        FROM monitoring_logs
    """)
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "total_records": row[0],
            "avg_blockage": round(row[1] or 0, 2),
            "max_blockage": round(row[2] or 0, 2),
            "avg_rain": round(row[3] or 0, 3),
            "total_alerts": row[4] or 0
        }
    return {}
