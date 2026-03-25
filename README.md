# 🔐 File Integrity Monitoring (FIM) with Wazuh SIEM

## 📌 Overview

This project implements a **real-time File Integrity Monitoring (FIM)** system using Python and integrates it with the **Wazuh SIEM platform** for log analysis, alert generation, and visualization.

The system continuously monitors a specified directory, detects file changes using **SHA256 hashing**, and generates structured logs that are ingested by Wazuh to produce security alerts.

---

## 🚀 Key Features

* 🔍 **Real-time Monitoring** using watchdog
* 🔐 **SHA256 Hashing** for integrity verification
* ⚡ Detection of:

  * File Creation
  * File Modification
  * File Deletion
* 📄 **Structured Logging** compatible with SIEM ingestion
* 🧠 **Custom Wazuh Rules** for alert generation
* 📊 **Dashboard Visualization** of alerts in Wazuh
* 🛠️ Lightweight and efficient implementation

---

## 🏗️ Architecture

```text
FIM Script (Python)
        ↓
Log File (fim.log)
        ↓
Wazuh Log Collector
        ↓
Wazuh Rules Engine
        ↓
Security Alerts (Dashboard)
```

---

## 🛠️ Technologies Used

| Technology   | Purpose                     |
| ------------ | --------------------------- |
| Python       | Core scripting              |
| Watchdog     | Real-time file monitoring   |
| Wazuh SIEM   | Log analysis and alerting   |
| SHA256       | File integrity verification |
| Linux (Kali) | Testing environment         |

---

## ⚙️ How It Works

1. The script creates a **baseline** of file hashes for the monitored directory.
2. It continuously watches for file system events using watchdog.
3. When a change occurs:

   * A new hash is generated
   * Compared with the baseline
4. If a difference is detected:

   * A log entry is created in `fim.log`
5. Wazuh reads the log file and:

   * Matches it against custom rules
   * Generates alerts in the dashboard

---

## 📂 Project Structure

```text
fim_realtime.py     # Main FIM script
README.md           # Project documentation
requirements.txt    # Dependencies
.gitignore          # Ignored files
```

---

## ▶️ Installation & Usage

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/fim-wazuh-siem.git
cd fim-wazuh-siem
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Run the script

```bash
python3 fim_realtime.py
```

Enter the directory you want to monitor when prompted.

---

### 4️⃣ Trigger events

```bash
echo "test" >> test_folder/file1.txt
touch test_folder/newfile.txt
rm test_folder/newfile.txt
```

---

## 📊 Sample Log Output

```text
MODIFIED file=test_folder/file1.txt
CREATED file=test_folder/newfile.txt
DELETED file=test_folder/newfile.txt
```

---

## 🔥 Wazuh Integration

* Configured Wazuh to monitor `fim.log` using `<localfile>`
* Implemented custom rules to detect:

  * `MODIFIED`
  * `CREATED`
  * `DELETED`
* Alerts are generated with severity levels and displayed in the dashboard

---

## 📸 Dashboard Output

*(Add your screenshot here)*

```text
Custom FIM: File modified → Level 10 alert
```

---

## 🎯 Learning Outcomes

This project helped in understanding:

* File Integrity Monitoring concepts
* Hash-based change detection
* Real-time system monitoring
* SIEM log ingestion and processing
* Detection engineering using Wazuh rules
* Alert visualization in security dashboards

---

## 💼 Real-World Use Case

This system can be used in:

* SOC environments for monitoring critical files
* Detecting unauthorized file modifications
* Identifying potential ransomware activity
* Compliance monitoring (PCI-DSS, HIPAA)

---

## ⚠️ Limitations

* Runs locally (no distributed agents)
* Does not yet include alert correlation
* No automated response (can be extended)

---

## 🚀 Future Improvements

* Add email/Slack alerting
* Integrate with SOAR platforms
* Monitor critical system directories (/etc, /var)
* Add anomaly detection using ML
* Implement centralized multi-agent architecture

---

## 👨‍💻 Author

**Bais Sabu**
Cybersecurity Enthusiast | SOC Analyst Aspirant

---
