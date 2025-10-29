# 🛡️ Sitewarden

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

**Sitewarden** is a lightweight Python-based tool for monitoring the availability, response time, and health of websites or APIs.  
It helps developers, sysadmins, and businesses keep track of uptime, detect outages early, and gain insights into performance trends.

![Sitewarden Screenshot](screenshots/sitewarden_snap_0.jpg)


---

## 🚀 Features

- 🔍 **URL Monitoring:** Check one or multiple URLs at defined intervals  
- ⏱️ **Response Time Tracking:** Measure and log latency  
- ⚠️ **Alerting System:** Notify via email, Slack, or console when sites go down  
- 📊 **Logging & Reports:** Export results to CSV, JSON, or databases  
- 🧠 **Smart Retries:** Recheck failed endpoints to avoid false alarms  
- 🧩 **Extensible:** Easily integrate new alerting or logging backends  

---

## 🧰 Installation

```bash
# Clone the repository
git clone https://github.com/almusavvir/sitewarden.git
cd sitewarden

# Install dependencies
pip install -r requirements.txt

# Run Sitewarden
python3 sitewarden.py
