# File Integrity Monitoring with Wazuh SIEM

## About This Project

I built this project to understand how File Integrity Monitoring (FIM) works in a real SOC environment and how it integrates with a SIEM like Wazuh.

The goal was to create a simple system that monitors files in real time, detects changes, and sends those events to Wazuh so they appear as security alerts in the dashboard.

---

## What This Project Does

* Monitors a directory in real time
* Detects:

  * File creation
  * File modification
  * File deletion
* Uses SHA256 hashing to verify file integrity
* Logs events in a format suitable for SIEM ingestion
* Sends logs to Wazuh
* Generates alerts using custom Wazuh rules

---

## How It Works

1. When the script runs, it creates a baseline of file hashes
2. It continuously monitors the folder using the watchdog library
3. When a file changes:

   * A new hash is generated
   * Compared with the stored baseline
4. If a change is detected:

   * An event is logged in `fim.log`
5. Wazuh reads this log file and:

   * Matches it with custom rules
   * Generates alerts in the dashboard

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/fim-wazuh-siem.git
cd fim-wazuh-siem
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run the script

```bash
python3 fim_realtime.py
```

Enter the directory you want to monitor when prompted.

---

## Testing the Project

Create a test folder:

```bash
mkdir test_folder
echo "hello" > test_folder/file1.txt
```

---

### Trigger file modification

```bash
echo "modified" >> test_folder/file1.txt
```

---

### Create a new file

```bash
touch test_folder/newfile.txt
```

---

### Delete a file

```bash
rm test_folder/newfile.txt
```

---

## Sample Log Output

```text
MODIFIED file=test_folder/file1.txt
CREATED file=test_folder/newfile.txt
DELETED file=test_folder/newfile.txt
```

---

## Wazuh Integration

To integrate with Wazuh, I configured the following in `ossec.conf`:

```xml
<localfile>
  <log_format>syslog</log_format>
  <location>/home/your-user/fim-wazuh-siem/fim.log</location>
</localfile>
```

Then restarted Wazuh:

```bash
sudo systemctl restart wazuh-manager
```

---

## Custom Detection Rules

Added custom rules in:

```text
/var/ossec/etc/rules/local_rules.xml
```

Example:

```xml
<group name="fim_custom,">

  <rule id="100100" level="10">
    <match>MODIFIED</match>
    <description>Custom FIM: File modified</description>
  </rule>

</group>
```

---

## Viewing Alerts

In the Wazuh dashboard:

1. Go to **Security Events**
2. Or **Threat Hunting → Discover**
3. Search:

```text
MODIFIED
```

---

## What I Learned

* How real-time file monitoring works
* How hashing helps detect file changes
* How SIEM tools ingest and process logs
* Writing custom detection rules in Wazuh
* Troubleshooting log ingestion issues

---

## Challenges I Faced

* Getting Wazuh to read custom logs
* Fixing log format issues for rule matching
* Handling duplicate file modification events
* Debugging SIEM ingestion pipeline

---

## Future Improvements

* Add email/Slack alerting
* Monitor critical system directories
* Improve event deduplication
* Add basic anomaly detection

---

## Author

Bais Sabu
Cybersecurity enthusiast focused on SOC and detection engineering
