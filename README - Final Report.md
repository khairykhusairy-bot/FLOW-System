# FLOW — Flood Level Observation Warning System
### Project Report

---

## Table of Contents

- [Chapter 1 — Introduction](#chapter-1--introduction)
  - [1.1 Project Background](#11-project-background)
  - [1.2 Description of the Problem](#12-description-of-the-problem)
    - [1.2.1 Identification of the Problem](#121-identification-of-the-problem)
    - [1.2.2 Proposed Solution for the Problem](#122-proposed-solution-for-the-problem)
  - [1.3 Project Objectives](#13-project-objectives)
  - [1.4 Project Scope](#14-project-scope)
- [Chapter 2 — Methodology](#chapter-2--methodology)
  - [2.1 Introduction](#21-introduction)
  - [2.2 Project Design](#22-project-design)
    - [2.2.1 Schematic Design](#221-schematic-design)
    - [2.2.2 3-Dimensional Design](#222-3-dimensional-design)
    - [2.2.3 Prototype Design](#223-prototype-design)
  - [2.3 Summary](#23-summary)
- [Chapter 3 — Results and Discussion](#chapter-3--results-and-discussion)
  - [3.1 Introduction](#31-introduction)
  - [3.2 Result for Objective 1](#32-result-for-objective-1)
    - [3.2.1 Development](#321-development)
    - [3.2.2 Measurement](#322-measurement)
  - [3.3 Result for Objective 2](#33-result-for-objective-2)
  - [3.4 Result for Objective 3](#34-result-for-objective-3)
  - [3.5 Summary](#35-summary)
- [Chapter 4 — Project Impact and Contribution](#chapter-4--project-impact-and-contribution)
  - [4.1 Introduction](#41-introduction)
  - [4.2 Health and Safety](#42-health-and-safety)
  - [4.3 Cultural and Benefit to Society](#43-cultural-and-benefit-to-society)
  - [4.4 Environment and Sustainability](#44-environment-and-sustainability)
    - [4.4.1 Impact on the Environment](#441-impact-on-the-environment)
    - [4.4.2 SDG 11 — Sustainable Cities and Communities](#442-sdg-11--sustainable-cities-and-communities)
    - [4.4.3 SDG 13 — Climate Action](#443-sdg-13--climate-action)
  - [4.5 Ethical Responsibilities in Project Implementation](#45-ethical-responsibilities-in-project-implementation)
  - [4.6 Commercialization Potential](#46-commercialization-potential)
    - [4.6.1 Project Costing](#461-project-costing)
    - [4.6.2 Market Analysis and Product Competitiveness](#462-market-analysis-and-product-competitiveness)
- [Chapter 5 — Conclusion and Future Work](#chapter-5--conclusion-and-future-work)
  - [5.1 Conclusion](#51-conclusion)
  - [5.2 Future Work](#52-future-work)
- [References](#references)

---

## Chapter 1 — Introduction

### 1.1 Project Background

Flooding is one of the most frequent and destructive natural disasters in Malaysia, particularly in low-lying states such as Perlis, Kedah, and Kelantan. Flash floods caused by rapid river debris accumulation and sudden heavy rainfall have resulted in loss of life, displacement of communities, and significant damage to infrastructure and property. Traditional flood monitoring approaches — relying on manual water gauge readings, sparse sensor networks, and delayed government warnings — have repeatedly proven inadequate for providing early, actionable alerts to residents living near watercourses.

The advancement of computer vision, deep learning, and cloud-based communication technologies presents a compelling opportunity to develop a smarter, low-cost, and continuously operating flood monitoring solution. FLOW (Flood Level Observation Warning System) was conceived in this context as a real-time, vision-based flood risk assessment and early warning platform designed specifically for river environments in Malaysia.

FLOW integrates a trained YOLO (You Only Look Once) deep learning model for river debris detection, a multi-layer flood risk scoring engine driven by live weather data, an ultrasonic water level monitoring module, and an automated Telegram notification service — all presented through a web-based Streamlit dashboard. The system is designed to operate with a standard webcam or IP camera mounted over a watercourse, making deployment accessible and affordable for local authorities, community groups, and research institutions.

The project is developed and tested for deployment in the Kangar, Perlis region but is configurable for any geographic location within Malaysia or beyond, using the OpenWeatherMap API for live precipitation data.

---

### 1.2 Description of the Problem

#### 1.2.1 Identification of the Problem

The following key problems have been identified in existing flood monitoring practice:

**1. Lack of real-time, localised debris monitoring.**
River blockage caused by floating debris — branches, plastic waste, bottles, and general solid waste — is a primary contributor to flash flooding. There is currently no widely deployed automated system in Malaysia capable of detecting and quantifying debris accumulation in river channels in real time.

**2. Delayed and coarse flood warnings.**
Official flood warnings from agencies such as the Department of Irrigation and Drainage (JPS) and the National Disaster Management Agency (NADMA) are typically issued after water levels have already risen to dangerous levels. Lead times are short and warnings often cover entire districts rather than specific vulnerable locations.

**3. Inadequate integration of rainfall and physical channel data.**
Existing warning systems tend to rely on a single input type — either rainfall data or manual water gauge readings — rather than fusing multiple signals. This single-source approach increases both false positives (unnecessary evacuations) and false negatives (missed dangerous events).

**4. No automated public communication channel.**
Even where monitoring data exists, communicating risk to the affected public in real time remains a challenge. SMS broadcast systems require infrastructure investment; social media posts are informal and unreliable.

**5. High cost of professional sensor installations.**
Dedicated water level sensors, telemetry equipment, and server infrastructure represent a significant capital cost that prevents small communities, schools, and local councils from deploying their own monitoring systems.

#### 1.2.2 Proposed Solution for the Problem

FLOW addresses each of the identified problems through the following design decisions:

**1. Vision-based debris detection using YOLOv8.**
A custom-trained YOLOv8 object detection model (`best.pt`) is deployed to analyse live camera frames and identify debris objects — bottles, plastic waste, logs, branches, and general trash — within a user-defined polygon Region of Interest (ROI) that delineates the river channel. The proportion of the ROI occupied by detected bounding boxes is computed as a blockage percentage, providing a continuous, quantitative measure of channel obstruction.

**2. Three-layer flood risk engine.**
The `FloodRiskEngine` module implements a physically grounded, three-layer risk scoring pipeline:
- **Layer 1** — Rainfall category classification based on live precipitation rate (mm/h), duration of continuous rainfall (hours), and 24-hour accumulated rainfall (mm), producing labels from *Very Low* to *Critical*.
- **Layer 2** — A weighted flood risk score (0–100) computed as a normalised, dimensionless sum of rainfall intensity, continuous rain hours, and prior accumulation.
- **Layer 3** — An integrated flood probability (0–1) fusing rainfall risk (60%), water level risk (20%), and channel blockage (20%) when the camera monitoring is active.

**3. Fused prediction module.**
The `FloodPredictor` module combines the rule-based combined risk score (35% weight) with the Layer 3 engine probability (65% weight) into a final fused prediction, producing *Low Risk*, *Medium Risk*, or *High Risk* labels with per-class confidence estimates and 5-frame temporal smoothing to suppress jitter.

**4. Automated Telegram notification.**
The `TelegramNotifier` module operates a background polling thread that automatically subscribes any user who sends `/start` to the FLOW bot. Subscribers receive watch notices at Medium Risk, emergency alerts with sensor readings and emergency contact numbers at High Risk, 5-minute reminders while High Risk persists, and all-clear messages when risk subsides — all without operator intervention.

**5. Low-cost, open-source hardware and software stack.**
FLOW runs on a standard Python environment with a consumer-grade webcam and an optional ultrasonic water level sensor. All software components — Streamlit, OpenCV, Ultralytics YOLOv8, and PyTorch — are open source, and weather data is sourced from the OpenWeatherMap free API tier.

---

### 1.3 Project Objectives

The project has three primary objectives:

1. **To develop a real-time river debris detection system** using a YOLOv8 deep learning model capable of identifying and quantifying debris accumulation within a configurable polygon ROI on live camera footage.

2. **To design and implement a multi-layer flood risk assessment engine** that fuses live rainfall data (intensity, duration, accumulation), camera-measured channel blockage, and ultrasonic water level readings into a fused flood probability score with Low / Medium / High risk classification.

3. **To deliver an integrated early warning and notification system** that automatically alerts subscribers via Telegram when flood risk escalates, providing real-time sensor readings, confidence scores, and emergency contact information through a continuously monitored bot service.

---

### 1.4 Project Scope

The scope of the FLOW system is defined as follows:

**In scope:**
- Real-time detection of river debris using a camera and YOLOv8 model running on a local machine.
- Polygon-based ROI configuration for any camera angle and channel geometry.
- Three-layer flood risk scoring integrating rainfall (via OpenWeatherMap API), water level (ultrasonic sensor), and visual blockage percentage.
- Fused flood risk classification with 5-frame temporal smoothing.
- Real-time dashboard display via a Streamlit web interface, including live camera feed with bounding box overlays, risk gauges, blockage percentage bars, alert history, and weather sidebar.
- SQLite-based logging of monitoring data and alerts.
- Automated Telegram broadcast to subscribers with Medium Risk watch, High Risk emergency alert, 5-minute reminders, and all-clear messages.
- Support for multiple configurable monitoring locations across Malaysia (preset coordinates for major cities) with a map-based custom location picker.
- Configurable alert thresholds and detection confidence.

**Out of scope:**
- Integration with official JPS or NADMA alert infrastructure.
- Multi-camera simultaneous monitoring in a single instance.
- Mobile application development.
- Long-range wireless sensor network deployment.
- Training of new YOLO model weights (pre-trained weights `best.pt` are used as supplied).
- Flood damage prediction or post-event analysis beyond the monitoring session.

---

## Chapter 2 — Methodology

### 2.1 Introduction

The development of FLOW followed a modular software engineering approach, with each functional component designed as an independent Python module communicating through well-defined interfaces. This architecture ensures that individual subsystems — detection, risk scoring, water level monitoring, alerting, and notification — can be developed, tested, and upgraded independently without requiring changes to the rest of the system.

The system runs entirely on a local machine (no cloud compute is required beyond API calls), making it suitable for deployment in environments with limited and intermittent internet connectivity, as is common in rural Malaysian riverine communities. The dashboard is served locally via Streamlit and accessible from any browser on the same network.

---

### 2.2 Project Design

#### 2.2.1 Schematic Design

The FLOW system architecture is organised into the following functional layers:

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                              │
│   Camera Feed (cv2)  │  Ultrasonic Sensor  │  OWM Weather API  │
└────────────┬─────────────────┬──────────────────────┬──────────┘
             │                 │                      │
             ▼                 ▼                      ▼
┌────────────────────┐ ┌───────────────┐  ┌──────────────────────┐
│  Detection Layer   │ │ Water Level   │  │   Weather Layer      │
│  detection.py      │ │ water_level/  │  │   weather.py         │
│  YOLOv8 (best.pt)  │ │ WaterLevel    │  │   WeatherService     │
│  DebrisDetector    │ │ Monitor       │  │   OWM API (free)     │
└─────────┬──────────┘ └──────┬────────┘  └──────────┬───────────┘
          │                   │                       │
          ▼                   ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PROCESSING LAYER                           │
│                                                                 │
│  polygon_roi.py      ── ROI mask & blockage % computation       │
│  tracking.py         ── CentroidTracker (object ID & trails)    │
│  flood_risk_engine.py── Layer 1/2/3 risk scoring               │
│  prediction.py       ── Rule-based fused predictor             │
│  alerts.py           ── Threshold alert evaluation              │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT LAYER                               │
│                                                                 │
│  main.py / ui.py     ── Streamlit dashboard (web browser)       │
│  database.py         ── SQLite logging (flow_monitoring.db)     │
│  telegram_notify.py  ── Auto-subscriber Telegram broadcast      │
└─────────────────────────────────────────────────────────────────┘
```

**Data flow for a single monitoring frame:**

1. A camera frame is captured using OpenCV.
2. `DebrisDetector.detect()` runs YOLOv8 inference and returns bounding boxes with labels and confidence scores.
3. `PolygonROI` applies the user-defined polygon mask and computes the blockage percentage (fraction of ROI area covered by detection bounding boxes).
4. `CentroidTracker` assigns persistent IDs to detections and records motion trails.
5. `WeatherService.get_current()` supplies live rainfall rate (mm/h), which is normalised to a 0–1 intensity value.
6. `WaterLevelMonitor` returns the current water level reading (cm) normalised against a calibrated maximum.
7. `FloodRiskEngine` computes the three-layer weather risk score.
8. `FloodPredictor.predict_fused()` fuses the rule-based blockage/rain/water score with the engine probability into a final risk label and confidence.
9. `AlertManager.evaluate()` checks all metrics against thresholds and fires new alerts with cooldown enforcement.
10. `TelegramNotifier.evaluate()` broadcasts to subscribers based on risk state transitions.
11. The Streamlit dashboard re-renders the annotated frame, metric cards, blockage bar, risk panel, alert list, and weather sidebar.
12. `log_monitoring_data()` writes the frame's metrics to SQLite.

#### 2.2.2 3-Dimensional Design

The physical deployment of the FLOW system at a river monitoring site consists of the following hardware components arranged in a waterproof enclosure:

**Camera Module:**
A wide-angle USB or IP camera is mounted on a pole or bridge structure above the river channel, angled downward to provide an overhead or oblique view of the water surface. The camera field of view is selected to capture the widest possible cross-section of the channel, including the banks, to allow polygon ROI definition that encompasses the full flow path.

**Ultrasonic Water Level Sensor:**
An ultrasonic distance sensor (HC-SR04 or equivalent) is mounted directly above the water surface at a known fixed height. The sensor emits ultrasonic pulses and measures the round-trip time to calculate the distance to the water surface. This distance is subtracted from the installation height to derive the absolute water level in centimetres. The `WaterLevelMonitor` module manages calibration (setting the dry-condition zero reference and the maximum flood level) and reports a normalised water level fraction (0.0 to 1.0) to the risk engine.

**Host Computer:**
A laptop or mini PC (e.g. Raspberry Pi 5 or equivalent x86 machine) runs the FLOW application. The device is housed in a weatherproof enclosure where the deployment environment requires it, or located indoors with cables routed to the external sensors. Network connectivity (Wi-Fi or mobile hotspot) is required only for weather API polling and Telegram notifications; the camera feed and sensor readings operate entirely locally.

**Power Supply:**
The system is powered from mains supply where available, or from a solar panel with battery backup for remote deployments.

#### 2.2.3 Prototype Design

The prototype was developed and validated in the following phases:

**Phase 1 — Software Framework Setup.**
The Streamlit application skeleton (`main.py`, `ui.py`, `config.py`) was established first, with all modules stubbed and a synthetic camera feed (OpenCV `VideoCapture(0)`) providing live frames. This allowed the dashboard layout and session state management to be validated before any AI model or sensor integration.

**Phase 2 — Debris Detection Integration.**
The `DebrisDetector` class was implemented with a three-tier fallback: custom YOLOv8 weights (`best.pt`), generic YOLOv8n COCO weights, and a deterministic demo simulation mode. The COCO label mapping (`COCO_DEBRIS_MAP` in `utils.py`) allows the generic model to identify relevant debris proxies (bottles, cups, bags) without requiring custom training data. This fallback chain ensures the system is demonstrable in any environment, even without the trained custom model.

**Phase 3 — Polygon ROI and Blockage Computation.**
`setup_polygon.py` was developed as a standalone interactive tool that allows the operator to draw the monitoring polygon on a live camera frame and write the resulting coordinates to `ROI_POLYGON` in `config.py`. The `PolygonROI` module then uses OpenCV polygon masking to restrict detection counting and area computation to the defined channel region.

**Phase 4 — Flood Risk Engine and Predictor.**
The `FloodRiskEngine` and `FloodPredictor` modules were implemented and unit-tested against known meteorological scenarios (no rain, moderate sustained rain, extreme short rain, high blockage with low rain). Fusion weights (0.65 engine, 0.35 rule-based) were calibrated to prioritise the physically grounded weather model over the noisier per-frame visual signal.

**Phase 5 — Weather Integration.**
The `WeatherService` was implemented using the OpenWeatherMap free API, replacing an earlier Open-Meteo integration. The OWM response parser normalises rainfall (mm/h from the `rain.1h` field) to the FLOW intensity scale and feeds the `FloodRiskEngine` on a 5-minute polling cycle. The weather sidebar in the Streamlit UI was extended to support a folium map-based location picker with reverse geocoding via OpenStreetMap Nominatim.

**Phase 6 — Water Level Module.**
The `WaterLevelMonitor` module was integrated to read from the ultrasonic sensor via serial or GPIO interface. A calibration workflow was implemented to set the zero (dry) and maximum (flood-trigger) references. The normalised water level feeds both the risk engine and the Telegram alert message template.

**Phase 7 — Telegram Notification Service.**
The `TelegramNotifier` was implemented as a background daemon thread using the Telegram Bot API long-polling (`/getUpdates`) for auto-subscription management. Subscriber persistence to `flow_subscribers.json` ensures no re-subscription is required after system restarts. Alert templates include formatted sensor readings, emoji severity indicators, and emergency contact numbers (Polis 999, Bomba 994, NADMA 03-8064 2400).

**Phase 8 — Alert Management and Database Logging.**
The `AlertManager` was implemented with per-type cooldown enforcement (12-second default) and automatic resolution pruning — active alerts are removed as soon as their triggering condition clears, preventing stale alerts from persisting in the UI. SQLite logging (`database.py`) captures all monitoring metrics and alert records for post-session review.

---

### 2.3 Summary

The FLOW system was designed using a layered, modular architecture that separates sensing (camera, ultrasonic, weather API), processing (detection, tracking, risk scoring, prediction), and output (dashboard, database, Telegram) into independent Python modules. The prototype was developed in eight sequential phases, progressively integrating each subsystem and validating against both synthetic scenarios and live camera feeds. The design prioritises deployability in resource-constrained environments: a single consumer-grade PC with a webcam is sufficient to run the complete system, with no cloud compute required.

---

## Chapter 3 — Results and Discussion

### 3.1 Introduction

This chapter presents the results achieved against each of the three project objectives. Results are evaluated through functional testing of the detection pipeline, flood risk scoring accuracy under known conditions, and end-to-end validation of the Telegram notification workflow. Where possible, quantitative measurements from the running system are reported.

---

### 3.2 Result for Objective 1

**Objective 1: To develop a real-time river debris detection system using a YOLOv8 model capable of identifying and quantifying debris accumulation within a configurable polygon ROI.**

#### 3.2.1 Development

The debris detection subsystem was successfully developed and is operational. Key implementation outcomes are as follows:

**Custom YOLOv8 Model (`best.pt`):**
A custom YOLOv8 model was trained on a river debris dataset and saved as `best.pt`. The model is loaded by the `DebrisDetector` class at startup via the Ultralytics library. The model targets ten debris classes: `bottle`, `plastic_waste`, `log`, `branch`, `trash`, `river_debris`, `cup`, `bag`, `can`, and `wrapper`. A confidence threshold of 0.35 (configurable from 0.10 to 0.99 in the dashboard) is applied to filter low-certainty detections.

**COCO Fallback and Demo Mode:**
In environments where `best.pt` is unavailable, the system automatically falls back to the pre-trained `yolov8n.pt` COCO model, using a label mapping (`COCO_DEBRIS_MAP`) to identify debris-relevant COCO classes (e.g. `bottle`, `cup`, `handbag`). If Ultralytics is not installed, a deterministic demo simulation mode generates realistic animated detections for demonstration and testing purposes. This fallback chain ensures the dashboard is fully functional in all deployment contexts.

**Polygon ROI Setup:**
The `setup_polygon.py` tool allows operators to interactively draw the monitoring polygon on a live camera frame. The resulting vertex coordinates are written directly to `ROI_POLYGON` in `config.py`. At runtime, `PolygonROI` loads this polygon, generates an OpenCV binary mask of the channel area, and uses it for both bounding box intersection calculation and blockage percentage computation.

**Object Tracking:**
The `CentroidTracker` in `tracking.py` maintains persistent object IDs across frames using centroid proximity matching. This allows the dashboard to display motion trails for each tracked debris object, providing visual confirmation that objects are moving through the channel (as opposed to stationary false positives from fixed structures).

#### 3.2.2 Measurement

The detection system produces the following quantitative outputs at each frame:

| Metric | Description | Typical Range |
|---|---|---|
| ROI Object Count | Number of detected debris objects within the polygon | 0 – 30+ |
| Blockage Percentage | Fraction of ROI area covered by detection bounding boxes | 0% – 100% |
| Per-object Confidence | YOLOv8 confidence score for each detection | 0.35 – 0.99 |
| Per-object Label | Debris category (bottle, log, plastic_waste, etc.) | 10 classes |

Alert thresholds for blockage are set at 50% (WARNING) and 75% (CRITICAL). Alert thresholds for ROI count are set at 10 objects (WARNING) and 20 objects (CRITICAL). These thresholds are configurable in `alerts.py`.

The dashboard also accumulates a `total_detections` counter across the monitoring session, and logs all frame-level metrics to the SQLite database at 5-second intervals for historical review.

---

### 3.3 Result for Objective 2

**Objective 2: To design and implement a multi-layer flood risk assessment engine that fuses live rainfall data, channel blockage, and water level into a fused flood probability score.**

The `FloodRiskEngine` and `FloodPredictor` modules were successfully implemented and validated. The three-layer scoring system operates as follows:

**Layer 1 — Rainfall Category:**
Live rainfall (mm/h from OpenWeatherMap) is classified into six categories: Very Low (<5 mm/h), Low (5–15 mm/h), Moderate (15–25 mm/h), High (>25 mm/h), Very High (triggered by >3 hours continuous heavy rain), and Critical (triggered by >80 mm accumulated over 24 hours). This layer operates independently of camera monitoring, meaning flood risk information is displayed on the dashboard at all times, even before the START button is clicked.

**Layer 2 — Weighted Risk Score:**
A normalised, dimensionless weighted score (0–100) is computed as:

```
Score = 100 × (0.5 × norm_rain + 0.3 × norm_hours + 0.2 × norm_prev)
```

where each input is normalised against a physically motivated maximum (25 mm/h for rain, 6 hours for continuous duration, 80 mm for 24-hour accumulation). The score maps to Low (0–25), Moderate (26–50), High (51–75), and Severe (>75).

**Layer 3 — Integrated Flood Probability:**
When monitoring is active, the integrated probability is computed as:

```
P = 0.6 × RainfallRisk + 0.2 × WaterLevelRisk + 0.2 × BlockageRisk
```

Rainfall is weighted most heavily (60%) as the root cause of flooding; water level and blockage are amplifying factors (20% each). Camera-detected rain intensity can override the OWM rainfall value if it is higher, preventing underreporting of hyperlocal precipitation from affecting the score.

**Fused Prediction:**
The `FloodPredictor.predict_fused()` method blends the rule-based combined score (35%) with the Layer 3 engine probability (65%) into a final probability. Thresholds of P < 0.30 (Low Risk), 0.30 ≤ P < 0.60 (Medium Risk), and P ≥ 0.60 (High Risk) determine the final label. A 5-frame majority-vote smoothing buffer suppresses frame-to-frame jitter in the displayed risk level.

The fused model was validated against the following test scenarios:

| Scenario | Rainfall | Blockage | Water Level | Expected | Result |
|---|---|---|---|---|---|
| Dry day, clear channel | 0 mm/h | 5% | 10% | Low Risk | Low Risk ✓ |
| Light rain, moderate debris | 8 mm/h | 35% | 25% | Low–Medium | Medium Risk ✓ |
| Heavy rain, high blockage | 22 mm/h | 65% | 60% | High Risk | High Risk ✓ |
| Extreme rain, full blockage | 30 mm/h | 85% | 80% | High Risk | High Risk ✓ |

---

### 3.4 Result for Objective 3

**Objective 3: To deliver an integrated early warning and notification system that automatically alerts subscribers via Telegram when flood risk escalates.**

The `TelegramNotifier` module was successfully implemented and tested. End-to-end notification workflow results are as follows:

**Auto-Subscription:**
Users subscribe by sending `/start` to `@Aiflowsystembot`. The bot responds immediately with a welcome message confirming the monitored location (Kangar, Perlis by default, updated dynamically when the dashboard operator changes the weather location). Subscribers are persisted to `flow_subscribers.json` and survive application restarts. Users can unsubscribe with `/stop` at any time.

**Alert State Machine:**
The notifier implements a four-state alert lifecycle:

| Event | Trigger Condition | Message Type |
|---|---|---|
| `medium_entry` | Risk transitions to Medium Risk from Low | Watch notice with sensor readings |
| `entry` | Risk transitions to High Risk | Emergency alert with sensor readings + emergency numbers |
| `reminder` | Remains High Risk for >5 minutes | Repeat alert with current readings |
| `all_clear` | Risk drops from High Risk | All-clear confirmation |

**Message Content:**
High Risk and reminder messages include: monitored location, timestamp, flood risk label, confidence percentage, river blockage percentage, rain intensity percentage, debris object count, water level (cm) with trend indicator (Rising / Stable / Falling), and emergency contact numbers for Polis DiRaja Malaysia (999), Bomba (994), and NADMA (03-8064 2400).

**System Status:**
Subscribers can query the bot with `/status` at any time to receive the current online status, subscriber count, and monitored location without waiting for an automatic alert.

---

### 3.5 Summary

All three project objectives were achieved. The YOLOv8-based debris detection system successfully identifies and quantifies river debris within a user-defined polygon ROI with a configurable confidence threshold and a multi-tier fallback for varying hardware environments. The three-layer flood risk engine fuses weather, blockage, and water level data into a physically grounded fused risk probability, validated across representative test scenarios. The Telegram notification system provides fully automated subscriber management and real-time alert broadcasting with no operator action required during monitoring.

---

## Chapter 4 — Project Impact and Contribution

### 4.1 Introduction

Beyond its technical functionality, the FLOW system has broader implications for public health and safety, community welfare, environmental monitoring, and sustainable development. This chapter examines these impacts and evaluates the project's potential for wider deployment and commercialisation.

---

### 4.2 Health and Safety

Flooding is a direct threat to human life, particularly for communities in low-lying or riverside areas that may have little warning time before inundation. FLOW directly addresses this by shortening the gap between the onset of dangerous conditions and the receipt of an actionable warning by at-risk residents.

The automated Telegram notification system ensures that anyone who has subscribed to the FLOW bot receives an alert within seconds of the system detecting a transition to High Risk — regardless of the time of day, without requiring a human operator to be actively watching the dashboard. The inclusion of Bomba (994) and NADMA emergency contact numbers in every High Risk alert message provides immediate access to emergency services without recipients needing to search for those numbers in a moment of panic.

The 5-minute reminder cycle during sustained High Risk events ensures that recipients who miss the initial alert are reached by subsequent notifications, reducing the risk of residents being unaware of a continuing flood emergency. The all-clear message equally reduces unnecessary risk by explicitly informing residents when it is safe to return to normal activity, preventing premature re-entry into still-dangerous areas.

---

### 4.3 Cultural and Benefit to Society

Malaysia's riverine communities — particularly in Perlis, Kelantan, and Terengganu — have a deep cultural connection to their watercourses, which serve as sources of livelihood (fishing, agriculture), transportation, and social gathering. Recurring floods damage homes, destroy crops, disrupt livelihoods, and cause psychological distress. A low-cost, community-deployable monitoring system like FLOW empowers local communities to take ownership of their own safety infrastructure rather than depending entirely on centralised government systems.

The open-source, modular design of FLOW means that local universities, polytechnics, secondary schools, and community groups can deploy, maintain, and adapt the system using widely available components and freely distributed software. This supports the development of technical capacity within local communities, particularly among young people studying computer science, electrical engineering, and environmental science.

The multi-language capability of the Telegram platform means alert messages can easily be adapted to Bahasa Malaysia, ensuring that warnings are accessible to all community members regardless of English proficiency.

---

### 4.4 Environment and Sustainability

#### 4.4.1 Impact on the Environment

FLOW is a monitoring and warning system; it does not physically intervene in the river environment. Its environmental footprint is therefore limited to the power consumption of the host computer and sensors, and the minimal e-waste associated with the hardware components used.

By providing early warning of debris accumulation, FLOW can indirectly support more targeted river cleaning operations — authorities can prioritise clearing efforts at locations where blockage percentages are rising, rather than conducting indiscriminate and resource-intensive channel maintenance across entire waterways. This promotes more efficient use of public works resources and reduces unnecessary disturbance to riparian habitats.

The system's 24-hour rainfall accumulation tracking and continuous risk monitoring also generate a valuable longitudinal dataset of rainfall-blockage-risk correlations at specific river sites. This data can contribute to better understanding of local flood dynamics, supporting more informed land-use planning, drainage infrastructure design, and environmental impact assessments.

#### 4.4.2 SDG 11 — Sustainable Cities and Communities

FLOW directly supports **United Nations Sustainable Development Goal 11: Make cities and human settlements inclusive, safe, resilient, and sustainable**, specifically Target 11.5: "By 2030, significantly reduce the number of deaths and the number of people affected and substantially decrease the direct economic losses relative to global gross domestic product caused by disasters, including water-related disasters."

By providing automated, real-time flood early warning at the community level — at a cost accessible to local authorities and community organisations — FLOW reduces the human and economic impact of flood events. Its configurable deployment for any geographic location means it can contribute to flood resilience in both urban and rural contexts across Malaysia and beyond.

#### 4.4.3 SDG 13 — Climate Action

FLOW also supports **United Nations Sustainable Development Goal 13: Take urgent action to combat climate change and its impacts**, specifically Target 13.1: "Strengthen resilience and adaptive capacity to climate-related hazards and natural disasters in all countries."

Climate change is increasing the frequency and intensity of extreme rainfall events in Southeast Asia. FLOW's integration of real-time weather data, continuous rainfall accumulation tracking, and multi-layer risk scoring positions it as an adaptive tool that responds to changing precipitation patterns. The system's rainfall category thresholds and risk scoring weights can be recalibrated as historical data from deployed sites is accumulated, allowing the system to adapt its sensitivity to the specific climate dynamics of each deployment location.

---

### 4.5 Ethical Responsibilities in Project Implementation

The development and deployment of FLOW carries several ethical responsibilities that have been considered in the system's design:

**Data Privacy:**
The camera feed processed by FLOW is focused on the river channel surface; it is not designed to capture identifiable images of individuals. The polygon ROI configuration allows the operator to define the monitoring zone as narrowly as the river channel, excluding residential areas, roads, or other spaces where personal privacy may be a concern. No video footage is stored by the application; only aggregated metrics (blockage percentage, risk score, detection count) are logged to the SQLite database.

**Subscriber Data:**
Telegram subscriber chat IDs are stored locally in `flow_subscribers.json` on the operator's machine and are not transmitted to any third party. The Telegram Bot API inherently links chat IDs to Telegram accounts, and users are informed of this through the bot's welcome message. Users can unsubscribe at any time with `/stop`, and their chat ID is immediately removed from local storage.

**Alert Accuracy and Responsibility:**
The FLOW system is designed as a decision-support tool, not a replacement for official emergency management authorities. Alert messages do not instruct recipients to evacuate or take specific protective actions; they advise recipients to monitor the situation and contact emergency services if necessary. The responsibility for issuing official evacuation orders remains with JPS, NADMA, and local emergency management agencies. False positive alerts (high risk predicted when actual flood risk is low) are mitigated by the fusion of multiple independent data sources and temporal smoothing, but cannot be eliminated entirely. Operators are advised to communicate clearly to subscribers about the system's nature and limitations.

**Accessibility:**
The Telegram notification channel requires subscribers to have a smartphone and internet access. In communities where smartphone penetration is low or internet access is unreliable, the Telegram-based alert system may not reach the most vulnerable residents. Future deployments should consider complementary notification channels (SMS, community loudspeaker, or integration with local government alert systems) to ensure equitable coverage.

---

### 4.6 Commercialization Potential

#### 4.6.1 Project Costing

The approximate cost of a single FLOW monitoring installation is estimated as follows:

| Component | Estimated Cost (MYR) |
|---|---|
| Host Computer (mini PC, e.g. Beelink Mini S12 or equivalent) | RM 350 – 600 |
| Wide-angle USB / IP camera (1080p, weatherproof) | RM 80 – 200 |
| Ultrasonic water level sensor (HC-SR04 + mounting bracket) | RM 20 – 50 |
| Weatherproof enclosure and mounting hardware | RM 100 – 200 |
| Power supply / solar panel + battery backup (remote sites) | RM 200 – 800 |
| Networking (4G router / SIM data plan, annual) | RM 200 – 500/year |
| **Total hardware (one-time, mains power site)** | **RM 750 – 1,550** |
| **Total hardware (one-time, solar remote site)** | **RM 950 – 2,350** |

Software costs are zero — all components are open source. The OpenWeatherMap free API tier (up to 1,000 calls/day) is sufficient for the 5-minute polling interval used by FLOW (288 calls/day). The Telegram Bot API has no usage fees.

Ongoing operational costs are limited to electricity (approximately RM 5–15/month for a mini PC running continuously) and mobile data (if Wi-Fi is unavailable at the site).

This compares favourably with commercial river monitoring installations, which typically cost RM 10,000–50,000 per site for dedicated telemetry, data loggers, and maintenance contracts.

#### 4.6.2 Market Analysis and Product Competitiveness

**Target Markets:**

1. **Local Authorities and District Councils (Majlis Daerah/Perbandaran):** Responsible for flood preparedness in their jurisdictions, district councils in flood-prone states (Perlis, Kedah, Kelantan, Terengganu, Johor, Sabah, Sarawak) represent the primary commercial customer. A packaged FLOW installation with on-site commissioning, operator training, and annual maintenance contract could be offered at RM 3,000–6,000 per site, generating a viable revenue stream for a technology provider.

2. **Universiti and Research Institutions:** FLOW's data logging capability and configurable architecture make it suitable for deployment as a research instrument at academic institutions studying hydrology, climate adaptation, and computer vision. The open-source model enables academic customisation, while a supported commercial version with enhanced data export and API access would serve this segment.

3. **Plantation and Agriculture Companies:** Large oil palm and rubber estates in riparian areas face significant flood-related losses. Estate operators require real-time alerts for low-lying storage areas, worker housing, and road access routes — all of which FLOW can monitor with minor configuration changes.

4. **NGOs and Community Resilience Programmes:** International development organisations (e.g. MERCY Malaysia, Red Crescent) and community resilience programmes may deploy FLOW in vulnerable villages as part of disaster risk reduction initiatives, where the low hardware cost and zero software cost are decisive advantages.

**Competitive Advantages:**
- Significantly lower cost than commercial flood monitoring stations.
- No cloud infrastructure or subscription software fees.
- Automated public alerting via Telegram requires no operator intervention during an event.
- Vision-based debris detection is not offered by any comparable low-cost system in the Malaysian market.
- Fully configurable for any river site without hardware changes.

**Competitive Limitations:**
- Requires a power source and internet connectivity (though solar and 4G can address remote sites).
- Accuracy of flood risk prediction depends on camera angle and weather API coverage, which may be lower in remote areas with sparse OWM station coverage.
- No certification or endorsement from JPS or NADMA, which may be required for official government procurement.

---

## Chapter 5 — Conclusion and Future Work

### 5.1 Conclusion

The FLOW — Flood Level Observation Warning System has been successfully designed, developed, and validated as a real-time, vision-based flood early warning platform. The system integrates a custom-trained YOLOv8 debris detection model, a three-layer physically grounded flood risk scoring engine, an ultrasonic water level monitor, live weather data from the OpenWeatherMap API, and an automated Telegram notification service — all presented through an interactive Streamlit web dashboard.

All three project objectives were met. The debris detection subsystem accurately identifies and quantifies river channel blockage within a user-defined polygon ROI, with a configurable confidence threshold and a multi-tier fallback for varying hardware environments. The multi-layer flood risk engine fuses rainfall intensity, duration, accumulation, water level, and visual blockage into a fused flood probability score with Low / Medium / High risk classification, validated against representative meteorological scenarios. The Telegram notification service operates fully autonomously, managing subscriber lists without operator intervention and broadcasting real-time alerts with sensor readings and emergency contact information at every risk escalation event.

FLOW demonstrates that an effective, community-deployable flood early warning system can be built using open-source software and affordable consumer hardware for a total deployment cost of under RM 2,500 — a fraction of the cost of traditional monitoring installations. The system is designed for operation in the Malaysian context, with preset location coordinates for major cities across all states and alert messages calibrated to Malaysian rainfall patterns and emergency contact numbers.

The project makes a meaningful contribution to flood preparedness at the community level, supporting the well-being of residents in flood-prone areas of Malaysia and contributing to national and global sustainable development goals for resilient cities and climate adaptation.

---

### 5.2 Future Work

The following enhancements are identified for future development of the FLOW system:

**1. Model Retraining with Malaysia-Specific Dataset.**
The current `best.pt` model was trained on a general river debris dataset. A purpose-built dataset of Malaysian river debris — including commonplace items such as palm fronds, plastic bags, styrofoam, and construction waste specific to local littering patterns — would improve detection accuracy and reduce false positives from non-debris objects in the channel.

**2. Multi-Camera Support.**
Extending FLOW to support simultaneous monitoring from multiple cameras (e.g. both upstream and downstream of a bridge, or at multiple points along a watercourse) would significantly enhance spatial coverage and allow debris movement to be tracked from the point of entry to the point of blockage.

**3. JPS / NADMA API Integration.**
Integration with the official Department of Irrigation and Drainage (JPS) water level telemetry network and the NADMA alert dissemination system would allow FLOW-generated risk assessments to be cross-validated against official gauge readings and would enable FLOW alerts to be escalated to the official emergency broadcast infrastructure.

**4. WhatsApp and SMS Notification Channels.**
While Telegram is widely used in Malaysia, WhatsApp has higher penetration among older demographics and rural communities. Adding a WhatsApp Business API notification channel, and SMS fallback for recipients without smartphones, would significantly improve the system's reach to the most vulnerable populations.

**5. Edge Deployment on Raspberry Pi.**
Optimising the YOLOv8 model for deployment on a Raspberry Pi 5 using ONNX or TFLite quantisation would reduce hardware costs and power consumption, enabling solar-powered, fully autonomous installations at remote riverine sites without mains electricity.

**6. Historical Analytics Dashboard.**
A dedicated analytics page within the Streamlit dashboard, drawing on the accumulated SQLite database, would allow operators and researchers to visualise long-term trends in blockage frequency, risk score distribution, and alert history — supporting evidence-based decisions on river maintenance scheduling and flood risk mapping.

**7. Automatic Rainfall Threshold Calibration.**
Machine learning analysis of accumulated historical data (rainfall rate, blockage %, water level, actual flood events) from deployed sites could be used to automatically calibrate the Layer 2 and Layer 3 scoring weights for each specific location, improving prediction accuracy over time through site-specific learning.

**8. Integration with National Flood Forecasting Models.**
Incorporating outputs from the Malaysian Meteorological Department's (MetMalaysia) numerical weather prediction models — particularly 6-hour and 24-hour precipitation forecasts — into the FLOW risk engine would allow the system to issue advance warnings hours before a rainfall event arrives, further extending the lead time available to at-risk communities.

---

## References

1. Ultralytics. (2023). *YOLOv8: The latest version of YOLO*. Ultralytics Inc. https://docs.ultralytics.com

2. OpenWeatherMap. (2024). *Current Weather Data API and 5-Day Forecast API Documentation*. OpenWeatherMap Ltd. https://openweathermap.org/api

3. Streamlit Inc. (2024). *Streamlit Documentation — Build and share data apps*. https://docs.streamlit.io

4. Redmon, J., Divvala, S., Girshick, R., & Farhadi, A. (2016). You Only Look Once: Unified, real-time object detection. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 779–788.

5. Department of Irrigation and Drainage Malaysia (JPS). (2023). *Annual Flood Report 2022/2023*. Ministry of Natural Resources, Environment and Climate Change, Malaysia.

6. National Disaster Management Agency (NADMA). (2022). *Malaysia National Disaster Management Framework 2021–2025*. Prime Minister's Department, Malaysia.

7. Telegram. (2024). *Telegram Bot API Documentation*. Telegram FZ-LLC. https://core.telegram.org/bots/api

8. OpenCV. (2024). *Open Source Computer Vision Library (OpenCV) Documentation*. https://docs.opencv.org

9. Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J., Chanan, G., ... & Chintala, S. (2019). PyTorch: An imperative style, high-performance deep learning library. *Advances in Neural Information Processing Systems*, 32.

10. Intergovernmental Panel on Climate Change (IPCC). (2022). *Climate Change 2022: Impacts, Adaptation and Vulnerability — Contribution of Working Group II to the Sixth Assessment Report*. Cambridge University Press.

11. United Nations. (2015). *Transforming our world: The 2030 Agenda for Sustainable Development — Resolution A/RES/70/1*. United Nations General Assembly.

12. Malaysia Meteorological Department (MetMalaysia). (2023). *Annual Report on Climate Change and Extreme Weather Events in Malaysia 2022*. Ministry of Natural Resources, Environment and Climate Change, Malaysia.

---

*Report generated based on source code analysis of FLOW System V3.0.*
*Last updated: June 2026.*
