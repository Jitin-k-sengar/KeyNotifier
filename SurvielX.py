from Installed_App_Monitor import Installed_App_Monitor
from Running_App_Monitor import Running_App_Monitor
from Wifi_Monitor import Wifi_Monitor
from threading import Thread

Thread(target=Installed_App_Monitor).start()
Thread(target=Running_App_Monitor).start()
Thread(target=Wifi_Monitor).start()