import subprocess
import platform
import re
import socket
import uuid

def get_mac_address():
    """
    Get the MAC address of the primary network interface.
    """
    mac_num = hex(uuid.getnode()).replace('0x', '').zfill(12)
    mac_address = ':'.join(mac_num[i:i+2] for i in range(0, 12, 2)).upper()
    return mac_address

def get_ip_address():
    """
    Get the local IP address of the machine.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"Unable to determine IP address: {e}"

def scan_windows():
    try:
        output = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
            encoding='utf-8', errors='ignore'
        )
    except subprocess.CalledProcessError:
        print("❌ Failed to scan WiFi networks. Please run this script as Administrator.")
        return []

    networks = []
    lines = output.split('\n')
    ssid = None
    bssid = None
    signal = None

    for line in lines:
        line = line.strip()
        if line.startswith("SSID "):
            parts = line.split(" : ")
            ssid = parts[1].strip() if len(parts) == 2 else None
            bssid = None
            signal = None
        elif line.startswith("BSSID "):
            parts = line.split(" : ")
            bssid = parts[1].strip() if len(parts) == 2 else None
        elif line.startswith("Signal"):
            parts = line.split(" : ")
            signal = parts[1].strip() if len(parts) == 2 else None
            if ssid:
                networks.append({'SSID': ssid, 'BSSID': bssid, 'Signal': signal})
                bssid = None
                signal = None
    return networks

def scan_linux():
    try:
        interfaces_output = subprocess.check_output(['iwconfig'], encoding='utf-8', errors='ignore')
        interfaces = re.findall(r'^(\w+)\s+IEEE', interfaces_output, re.MULTILINE)
        if not interfaces:
            print("❌ No wireless interfaces found.")
            return []

        iface = interfaces[0]

        output = subprocess.check_output(['sudo', 'iwlist', iface, 'scan'], encoding='utf-8', errors='ignore')
    except subprocess.CalledProcessError:
        print("❌ Failed to scan WiFi networks. Please run this script with sudo/root.")
        return []

    networks = []
    cells = output.split("Cell ")
    for cell in cells[1:]:
        ssid_search = re.search(r'ESSID:"([^"]+)"', cell)
        ssid = ssid_search.group(1) if ssid_search else None

        signal_search = re.search(r'Signal level=(-?\d+)\s*dBm', cell)
        if not signal_search:
            signal_search = re.search(r'Signal level=(\d+)/100', cell)
        signal = signal_search.group(1) if signal_search else None

        address_search = re.search(r'Address: ([0-9A-Fa-f:]{17})', cell)
        bssid = address_search.group(1) if address_search else None

        if ssid:
            networks.append({'SSID': ssid, 'BSSID': bssid, 'Signal': signal})
    return networks

def main():
    system = platform.system()
    print(f"\n📶 Scanning WiFi networks on {system}...\n")

    if system == "Windows":
        networks = scan_windows()
    elif system == "Linux":
        networks = scan_linux()
    else:
        print(f"❌ Unsupported OS: {system}")
        return

    if not networks:
        print("⚠️ No WiFi networks found.")
    else:
        print(f"✅ Found {len(networks)} network(s):\n")
        for i, net in enumerate(networks, 1):
            print(f"{i}. SSID: {net['SSID']}")
            print(f"   BSSID: {net['BSSID']}")
            if net['Signal']:
                print(f"   Signal: {net['Signal']}")
            print()

    print("💻 Your IP address  :", get_ip_address())
    print("🔐 Your MAC address :", get_mac_address())

if __name__ == "__main__":
    main()
