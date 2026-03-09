# 🌡️ Temperature Sensor Monitor — ROS 2

A ROS 2-based temperature monitoring system that simulates a real-world sensor pipeline using a **three-node architecture**. The system publishes live temperature readings, evaluates them against a configurable threshold, triggers alerts, and logs all anomalies — with full support for **runtime parameter tuning**, **custom service calls**, and **multiple launch configurations**.

---

## 📌 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Nodes](#nodes)
- [Custom Interface](#custom-interface)
- [Launch Configurations](#launch-configurations)
- [Prerequisites](#prerequisites)
- [Installation & Build](#installation--build)
- [Usage](#usage)
- [Runtime Configuration](#runtime-configuration)
- [Project Structure](#project-structure)
- [Key Concepts Demonstrated](#key-concepts-demonstrated)

---

## Overview

This project models a production-style IoT temperature monitoring pipeline entirely within ROS 2. Three decoupled nodes communicate via topics and services:

1. A **sensor node** generates temperature readings with configurable base values and variance.
2. A **monitor node** evaluates readings against a threshold and publishes alerts — threshold can be adjusted live via a ROS 2 service.
3. A **logger node** subscribes to alerts and maintains a timestamped in-memory log of all anomalies.

---

## System Architecture

```
                        ROS 2 Temperature Monitor — Node Graph
  
  ┌──────────────────────────────┐
  │      TemperatureSensor       │
  │   [ temperature_sensor.py ]  │
  │                              │
  │  params:                     │
  │   • publish_rate  (2.0 Hz)   │
  │   • base_temp     (25.0 °C)  │
  │   • temp_variation (5.0 °C)  │
  └──────────────┬───────────────┘
                 │
                 │  TOPIC: /temperature
                 │  type:  std_msgs/Float32
                 │
                 ▼
  ┌──────────────────────────────┐          ┌─────────────────────────────┐
  │         MonitorNode          │          │       ROS 2 Client          │
  │      [ monitor_node.py ]     │◄─────────│  (CLI / external node)      │
  │                              │  SERVICE │                             │
  │  param:                      │ /set_threshold                        │
  │   • temp_threshold (28.0 °C) │  Setbool │  data=true  → threshold+5  │
  │                              │  srv     │  data=false → threshold-5  │
  └──────────────┬───────────────┘          └─────────────────────────────┘
                 │
                 │  TOPIC: /alerts
                 │  type:  std_msgs/String
                 │  (published only when temp > threshold)
                 │
                 ▼
  ┌──────────────────────────────┐
  │         AlertLogger          │
  │     [ alert_logger.py ]      │
  │                              │
  │  • timestamps each alert     │
  │  • tracks cumulative count   │
  │  • logs to ROS 2 console     │
  └──────────────────────────────┘
```

---

## Nodes

### `temperature_sensor.py` — Sensor Node
Simulates a hardware temperature sensor. Publishes randomized temperature readings to the `/temperature` topic at a configurable rate.

| Parameter | Default | Description |
|---|---|---|
| `publish_rate` | `2.0` | Publishing frequency in Hz |
| `base_temp` | `25.0` | Baseline temperature in °C |
| `temp_variation` | `5.0` | ± random variation applied each reading |

- **Publishes:** `/temperature` (`std_msgs/Float32`)

---

### `monitor_node.py` — Monitor Node
The core decision-making node. Evaluates each incoming temperature reading against a threshold. Publishes an alert message if the threshold is exceeded. Also exposes a **ROS 2 service** to raise or lower the threshold at runtime without restarting the system.

| Parameter | Default | Description |
|---|---|---|
| `temp_threshold` | `28.0` | Alert trigger temperature in °C |

- **Subscribes:** `/temperature` (`std_msgs/Float32`)
- **Publishes:** `/alerts` (`std_msgs/String`)
- **Service:** `/set_threshold` (`my_robot_interfaces/srv/Setbool`)
  - `request.data = True` → threshold **+5°C**
  - `request.data = False` → threshold **−5°C**

---

### `alert_logger.py` — Alert Logger Node
Listens to the `/alerts` topic and maintains a timestamped in-memory log of every alert received. Logs alert count in real time.

- **Subscribes:** `/alerts` (`std_msgs/String`)
- Timestamps each alert using `datetime.now()`
- Tracks cumulative alert count across the session

---

## Custom Interface

The `my_robot_interfaces` package defines a custom service used by the Monitor Node:

```
# Setbool.srv
bool data        # True = increase threshold, False = decrease threshold
---
bool success     # Whether the operation succeeded
string message   # Human-readable confirmation with new threshold value
```

> This custom service (rather than `std_srvs/SetBool`) demonstrates how to design domain-specific interfaces that carry semantically meaningful responses.

---

## Launch Configurations

Four launch files are provided under `temp_monitor_system/launch/`, each demonstrating a different ROS 2 launch pattern:

| Launch File | Description |
|---|---|
| `system.launch.py` | Basic launch — starts all three nodes |
| `system_advanced.launch.py` | Advanced launch with argument passing and logging config |
| `system_namespaced.launch.py` | Launches nodes under a ROS 2 namespace for multi-robot or isolated testing |
| `system_with_yaml.launch.py` | Loads parameters from a YAML config file (production-style configuration) |

---

## Prerequisites

| Requirement | Version |
|---|---|
| Ubuntu | 22.04 LTS (Jammy) |
| ROS 2 | Humble Hawksbill (or newer) |
| Python | 3.10+ |
| `colcon` | Latest |

---

## Installation & Build

**1. Clone into your ROS 2 workspace:**

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/Gowtham13042007/Temperature_sensor.git .
```

**2. Install dependencies:**

```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
```

**3. Build the workspace:**

```bash
colcon build
```

**4. Source the workspace:**

```bash
source install/setup.bash
```

---

## Usage

### Option A — Launch all nodes at once (recommended)

```bash
ros2 launch temp_monitor_system system.launch.py
```

### Option B — Run nodes individually (3 terminals)

```bash
# Terminal 1 — Temperature Sensor
ros2 run temp_monitor_system temperature_sensor

# Terminal 2 — Monitor Node
ros2 run temp_monitor_system monitor_node

# Terminal 3 — Alert Logger
ros2 run temp_monitor_system alert_logger
```

### Inspect live data

```bash
# View temperature stream
ros2 topic echo /temperature

# View alert stream
ros2 topic echo /alerts

# Check topic frequency
ros2 topic hz /temperature
```

---

## Runtime Configuration

### Adjust parameters at launch

```bash
ros2 run temp_monitor_system temperature_sensor \
  --ros-args -p base_temp:=30.0 -p publish_rate:=5.0 -p temp_variation:=8.0
```

### Change threshold live via service call

```bash
# Increase threshold by 5°C
ros2 service call /set_threshold my_robot_interfaces/srv/Setbool "{data: true}"

# Decrease threshold by 5°C
ros2 service call /set_threshold my_robot_interfaces/srv/Setbool "{data: false}"
```

---

## Project Structure

```
Temperature_sensor/
│
├── my_robot_interfaces/              # Custom ROS 2 service definition
│   ├── srv/
│   │   └── Setbool.srv               # Custom service: bool → success + message
│   ├── CMakeLists.txt
│   └── package.xml
│
└── temp_monitor_system/              # Core application package
    ├── config/                       # YAML parameter files
    ├── launch/
    │   ├── system.launch.py          # Basic launch
    │   ├── system_advanced.launch.py # Launch with args & logging
    │   ├── system_namespaced.launch.py # Namespaced launch
    │   └── system_with_yaml.launch.py  # YAML-driven config launch
    ├── resource/
    ├── temp_monitor_system/
    │   ├── __init__.py
    │   ├── temperature_sensor.py     # Publisher node (sensor simulation)
    │   ├── monitor_node.py           # Threshold monitor + service server
    │   └── alert_logger.py           # Alert subscriber + timestamped log
    ├── test/
    ├── package.xml
    ├── setup.cfg
    └── setup.py
```

---

## Key Concepts Demonstrated

| Concept | Implementation |
|---|---|
| **Publisher / Subscriber** | `/temperature` and `/alerts` topics using `Float32` and `String` |
| **ROS 2 Services** | `/set_threshold` with a custom `Setbool` service — runtime threshold control |
| **Custom Interfaces** | `my_robot_interfaces` package with a domain-specific `.srv` definition |
| **Parameterized Nodes** | `declare_parameter()` with defaults, overridable at launch |
| **Multiple Launch Patterns** | Basic, advanced, namespaced, and YAML-driven launch files |
| **Multi-Node Architecture** | Three fully decoupled nodes communicating over DDS |
| **Alert Logging** | Timestamped in-memory log with cumulative alert tracking |
| **Multi-Package Workspace** | Interface package separated from application logic |

---

*Built with ROS 2 · Python · rclpy · CMake · colcon*
