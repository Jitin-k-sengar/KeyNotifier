import winreg
import time
from Email_Report import send_email
import filecmp

def Extract_installed_apps():
    """
    Retrieves a list of installed applications on a Windows system.

    This function scans the Windows registry for installed applications,
    checking both 64-bit and 32-bit registry paths, as well as user-specific
    installations.

    Returns:
        list: A list of strings, where each string is the display name of an
              installed application. The list may contain duplicates if an
              application is registered in multiple locations.

    Note:
        This function is specific to Windows operating systems and relies on
        the winreg module to access the Windows registry.
    """
    apps = []

    # Registry paths for 64-bit and 32-bit apps on Windows
    paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    ]

    for root, path in paths:
        try:
            with winreg.OpenKey(root, path) as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            app_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            apps.append(app_name)
                    except (FileNotFoundError, OSError, IndexError):
                        # Skip entries that are incomplete or not accessible
                        continue
        except FileNotFoundError:
            # Skip paths that do not exist
            pass

    return apps

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
        file1 = "Log\\Installed_app.log"
        file2 = "Temp\\Installed_app_temp.log"
        # Compare the two files using filecmp
        if filecmp.cmp(file1, file2, shallow=False):
            return "Same"
        else:
            return "Different"
    except FileNotFoundError as e:
        print(f"Error: {e}")

def Clear_file(file_path: str):
    """
    Clears the content of a file by opening it in write mode and writing an empty string.

    This function attempts to open the specified file in write mode and clear its contents.
    If the file doesn't exist, it prints an error message.

    Parameters:
    file_path (str): The path to the file that needs to be cleared.

    Returns:
    None

    Raises:
    FileNotFoundError: If the specified file is not found, an error message is printed.
    """
    try:
        with open(file_path, "w") as f:
            f.write("")
    except FileNotFoundError as e:
        print(f"Error: {e}")

def Write_file(file_path: str, content: list):
    """
    Writes a list of content to a file, appending each item on a new line.

    This function opens the specified file in append mode and writes each item
    from the content list to the file, adding a newline character after each item.

    Parameters:
    file_path (str): The path to the file where the content will be written.
    content (list): A list of strings to be written to the file.

    Returns:
    None

    Note:
    The function does not handle file-related exceptions. It's recommended to
    implement error handling when using this function in production code.
    """
    f = open(file_path, "a")
    for con in content:
        f.write(f"{con}\n")
    f.close()
    
def Installed_App_Monitor():
    """
    Monitors changes in installed applications and sends email notifications.

    This function runs in an infinite loop, periodically checking for changes
    in the list of installed applications. If changes are detected, it sends
    an email report and updates the log files.

    The function performs the following steps:
    1. Extracts the current list of installed applications.
    2. Writes this list to a temporary file.
    3. Compares the temporary file with the existing log file.
    4. If changes are detected:
       - Reads the content of the temporary file.
       - Sends an email with the updated list of applications.
       - Updates the main log file.
       - Clears the temporary file.
    5. Waits for 3 minutes before the next check.

    Note:
    - This function does not take any parameters.
    - It does not return any value as it runs indefinitely.
    - The function relies on several helper functions: Extract_installed_apps(),
      Write_file(), Compare_content(), send_email(), and Clear_file().
    - The email recipient is hardcoded as "Jitin.k.sengar@gmail.com".
    """
    while True:
        installed_apps = Extract_installed_apps()

        Write_file("Temp\\Installed_app_temp.log", installed_apps)

        if Compare_content() == "Same":
            Clear_file("Temp\\Installed_app_temp.log")
        else:
            f = open("Temp\\Installed_app_temp.log", "r")
            content = f.read()
            send_email("Jitin.k.sengar@gmail.com", "Installed Application Report", f"{content}")
            print("Email sent")
            Clear_file("Log\\Installed_app.log")
            Write_file("Log\\Installed_app.log", installed_apps)
            Clear_file("Temp\\Installed_app_temp.log")

        time.sleep(180)