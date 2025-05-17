# wifi-scanner

# 📶 Wi-Fi Network Scanner (Python)

This is a simple cross-platform Wi-Fi network scanner built using Python. It can scan nearby Wi-Fi networks (SSID, BSSID, Signal Strength) and also display the host's IP and MAC address.

---

## 🚀 Features

- Scans nearby **Wi-Fi networks**:
  - Shows **SSID (Wi-Fi name)**
  - Shows **BSSID (MAC address of router)**
  - Shows **Signal strength** (in % or dBm)
- Works on both **Windows** and **Linux**
- Detects your local **IP address**
- Detects your device’s **MAC address**
- CLI-based with clean, readable output

---

## 🖥️ Platforms Supported

- ✅ Windows (with `netsh`)
- ✅ Linux (with `iwconfig` + `iwlist` — may require `sudo`)

---

## ⚙️ Requirements

- Python 3.6+
- Admin/root privileges (for full scan results)
- For Linux: `wireless-tools` must be installed:
  ```bash
  sudo apt install wireless-tools



## Sample Output

📶 Scanning ALL nearby WiFi networks on Windows...

✅ Found 3 unique WiFi networks:

1. SSID : Global_5GHz
   BSSID: b4:3d:08:9b:f0:01
   Signal: 61%

2. SSID : Home_WiFi
   BSSID: a0:ab:1b:5d:77:1a
   Signal: 75%

3. SSID : Mobile_Hotspot
   BSSID: 92:34:a1:45:ff:bb
   Signal: 40%

💻 Your IP address  : 192.168.1.46
🔐 Your MAC address : 50:E0:85:96:D7:B5


## Internals Used

netsh wlan show networks mode=bssid (Windows)

iwlist scan (Linux)

socket module for IP

uuid module for MAC


