import psutil
import time
from Email_Report import send_email

def Extract_running_apps():
    """
    Extracts the list of currently running user-installed applications/processes.

    This function iterates through all active processes using psutil,
    capturing the name of each process and filtering out duplicates and system processes.

    Returns:
        list: A list of strings, each representing the name of a user-installed running process.
    """
    running_apps = set()  # Use a set to avoid duplicates
    user_installed_paths = ["C:\\Program Files", "C:\\Program Files (x86)", "C:\\Users"]  # Example paths

    for process in psutil.process_iter(attrs=['name', 'exe']):
        try:
            exe_path = process.info['exe']
            if exe_path:  # Check if the executable path is available
                # Check if the executable path starts with user-installed paths
                if any(exe_path.startswith(path) for path in user_installed_paths):
                    running_apps.add(process.info['name'])  # Add to set to avoid duplicates
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return list(running_apps)  # Convert the set back to a list

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
        for item in content:
            f.write(f"{item}\n")

def Time_checker(start_time: float, duration: int) -> bool:
    """
    Checks if a specified duration has passed since the start time.

    Parameters:
    start_time (float): The start time in seconds (epoch time).
    duration (int): Duration in seconds to check against.

    Returns:
    bool: True if the duration has passed, False otherwise.
    """
    current_time = time.time()
    return (current_time - start_time) >= duration

def Running_App_Monitor():
    """
    Monitors the running applications and sends email notifications if needed.

    This function performs the following steps:
    1. Checks if the log file is empty.
    2. If not empty, sends an email with the log file content and clears the log file.
    3. Extracts the list of running applications.
    4. Logs the list of applications along with the current date and time.
    5. Waits for 30 seconds and checks if the log has been written for 30 minutes.
    6. Sends email if the time duration is met, then clears the log file.
    """
    log_file = "Log\\Running_app.log"

    while True:
        # Step 1: Check if log file is empty
        try:
            with open(log_file, "r") as f:
                content = f.read().strip()
                if content:
                    send_email("jitin.k.sengar@gmail.com", "Running Application Report", content)
                    Clear_file(log_file)
        except FileNotFoundError:
            pass

        # Step 2: Extract running application details
        running_apps = Extract_running_apps()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        Write_file(log_file, [f"{timestamp}"] + running_apps)

        # Step 3: Wait for 30 minutes or keep monitoring
        start_time = time.time()
        while not Time_checker(start_time, 1800):  # 1800 seconds = 30 minutes
            time.sleep(30)

        # Step 4: Send email and clear log file
        with open(log_file, "r") as f:
            content = f.read()
            send_email("raunitarya599@gmail.com", "Running Application Log Report", content)
        Clear_file(log_file)
