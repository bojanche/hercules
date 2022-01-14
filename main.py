import os
from ppadb.client import Client as AdbClient
import time
from pyaxmlparser import APK
import sys


DEFAULT_150_APPLIST = ['com.securityandsafetythings.datetimecontrol',
                    'com.securityandsafetythings.messagebroker',
                    'com.securityandsafetythings.appmanager.app',
                    'com.securityandsafetythings.firmware',
                    'com.securityandsafetythings.ids',
                    'com.securityandsafetythings.io',
                    'com.securityandsafetythings.videopipeline',
                    'com.securityandsafetythings.networkcontrol',
                    'com.android.defcontainer',
                    'com.securityandsafetythings.idswebui',
                    'android',
                    'com.securityandsafetythings.adbauthorization',
                    'com.securityandsafetythings.gateway',
                    'com.securityandsafetythings',
                    'com.android.providers.settings',
                    'com.securityandsafetythings.devicemanagement',
                    'com.securityandsafetythings.appresourceproxy',
                    'com.securityandsafetythings.deviceid',
                    'android.ext.shared',
                    'com.securityandsafetythings.cloudconnector.app',
                    'android.ext.services',
                    'com.android.packageinstaller',
                    'com.securityandsafetythings.crashreporter.app',
                    'com.securityandsafetythings.health',
                    'com.securityandsafetythings.webserver',
                    'com.android.shell',
                    'com.securityandsafetythings.userdb',
                    'com.securityandsafetythings.event',
                    'com.securityandsafetythings.wificonnect',
                    'com.securityandsafetythings.media',
                    'com.securityandsafetythings.onvif',
                    'com.securityandsafetythings.webui']

DEFAULT_151_APPLIST = ['com.securityandsafetythings.datetimecontrol',
                    'com.securityandsafetythings.messagebroker',
                    'com.securityandsafetythings.appmanager.app',
                    'com.securityandsafetythings.firmware',
                    'com.securityandsafetythings.ids',
                    'com.securityandsafetythings.io',
                    'com.securityandsafetythings.videopipeline',
                    'com.securityandsafetythings.networkcontrol',
                    'com.securityandsafetythings.resourcemanager',
                    'com.android.defcontainer',
                    'com.securityandsafetythings.idswebui',
                    'android',
                    'com.securityandsafetythings.adbauthorization',
                    'com.securityandsafetythings.gateway',
                    'com.securityandsafetythings',
                    'com.android.providers.settings',
                    'com.securityandsafetythings.devicemanagement',
                    'com.securityandsafetythings.appresourceproxy',
                    'com.securityandsafetythings.deviceid',
                    'android.ext.shared',
                    'com.securityandsafetythings.cloudconnector.app',
                    'android.ext.services',
                    'com.android.packageinstaller',
                    'com.securityandsafetythings.crashreporter.app',
                    'com.securityandsafetythings.health',
                    'com.securityandsafetythings.webserver',
                    'com.android.shell',
                    'com.securityandsafetythings.userdb',
                    'com.securityandsafetythings.event',
                    'com.securityandsafetythings.wificonnect',
                    'com.securityandsafetythings.media',
                    'com.securityandsafetythings.onvif',
                    'com.securityandsafetythings.webui']
DEFAULT_200_APPLIST = ['com.securityandsafetythings.datetimecontrol',
                    'com.securityandsafetythings.messagebroker',
                    'com.securityandsafetythings.appmanager.app',
                    'com.securityandsafetythings.firmware',
                    'com.securityandsafetythings.ids',
                    'com.securityandsafetythings.io',
                    'com.securityandsafetythings.videopipeline',
                    'com.securityandsafetythings.networkcontrol',
                    'com.android.defcontainer',
                    'com.securityandsafetythings.idswebui',
                    'android',
                    'com.securityandsafetythings.adbauthorization',
                    'com.securityandsafetythings.gateway',
                    'com.securityandsafetythings',
                    'com.android.providers.settings',
                    'com.securityandsafetythings.devicemanagement',
                    'com.securityandsafetythings.appresourceproxy',
                    'com.securityandsafetythings.deviceid',
                    'android.ext.shared',
                    'com.securityandsafetythings.cloudconnector.app',
                    'android.ext.services',
                    'com.android.packageinstaller',
                    'com.securityandsafetythings.crashreporter.app',
                    'com.securityandsafetythings.health',
                    'com.securityandsafetythings.webserver',
                    'com.android.shell',
                    'com.securityandsafetythings.userdb',
                    'com.securityandsafetythings.event',
                    'com.securityandsafetythings.wificonnect',
                    'com.securityandsafetythings.media',
                    'com.securityandsafetythings.onvif',
                    'com.securityandsafetythings.webui',
                    'com.securityandsafetythings.calibration',
                    'com.securityandsafetythings.streamprovider']

DEFAULT_REPORT_NAME = 'report.txt'
DEFAULT_TEST_TIME = 300
DEFAULT_LOGCAT_NAME = 'camera.log'
DEFAULT_CAMERA_IP = '192.168.1.236'


# Sleeper function with time countdown
def sleeper(remaining):
    for rest in range(remaining, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(rest))
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\rComplete!            \n")


# Clear apps from the camera for a fresh new start
def clear_camera():
    apk_list_on_camera = []
    try:
        apk_on_camera = device.shell("pm list packages").split('package:')
    except (AttributeError, RuntimeError) as e:
        print("Camera not accessible. Killing the tests...Error: ", e)
        sys.exit()

    for aplist in apk_on_camera:
        apk_list_on_camera.append(aplist.rstrip())
    apk_list_on_camera = apk_list_on_camera[1:]
    apk_difference = list(set(apk_list_on_camera) - set(DEFAULT_200_APPLIST))
    if apk_difference != ['']:
        for i in apk_difference:
            device.uninstall(i)
    device.shell("logcat -c")
    device.shell("reboot")
    print("--- Preparing camera for application testing...")
    print("--- Wait until camera reboots (80 seconds)...")
    sleeper(80)
    device.shell("wait-for-device")


def install_app(apk):
    try:
        device.install(apk, grand_all_permissions=True)
    except:
        print("--- Camera still offline, please try again.")
        sys.exit()
    print("---- Installing apk. Time delay set to 10 seconds for the app to install/settle...")
    sleeper(10)


# Checking if adb server is running
try:
    os.system('adb start-server')
except:
    pass

# creating client connection to the server
client = AdbClient(host="127.0.0.1", port=5037)

# connecting to the camera
device_IP = input('Please enter camera IP: ')
if device_IP == '':
    print("--- No IP entered. Using default camera ip: {}...".format(DEFAULT_CAMERA_IP))
    device_IP = DEFAULT_CAMERA_IP
else:
    print('--- Device ip:', device_IP)

client.remote_connect(device_IP, 5555)
device = client.device(device_IP+":5555")
dir_path = input("Please enter the folder in which app to-be-tested resides (if not entered, current folder will be used): ")
dir_list = []
if dir_path == '':
    dir_path = '.'
    dir_list = os.listdir(dir_path)
else:
    try:
        dir_list = os.listdir(dir_path)
    except:
        print("Wrong folder format. Shutting down testing.")
        sys.exit()

apk_list = []
for file in dir_list:
    if file.endswith(".apk"):
        apk_list.append(file)
for n, t in enumerate(apk_list):
    print(str(n)+'. '+t)
if len(apk_list) <=0:
    print("No apks found in this folder. Exiting...")
    sys.exit()
select_app = input("Pls enter number of app to test: ")
apk_filename = apk_list[int(select_app)]

# removes ALL non-OS apps and resets the camera, clears logcat
clear_camera()
client.remote_connect(device_IP, 5555)
install_app(os.path.join(dir_path, apk_filename))


apk = APK(os.path.join(dir_path, apk_filename))
print("Checking certs for: ", apk.packagename)
print('--- Writing cert info into file')
os.chdir(dir_path)
os.system("apksigner verify -v --print-certs "+"{} >> {}".format(apk_filename, DEFAULT_REPORT_NAME))
report_file = open(os.path.join(dir_path, DEFAULT_REPORT_NAME), "a")
# tabulating the cert info
report_file.write("\nPackage name: "+apk.packagename+'\n')
report_file.write("\n- Initial CPU usage: "+str(device.cpu_percent())+' %'+'\n')
report_file.write("- Initial memory usage: "+str(round(device.get_meminfo(apk.packagename).pss / 1024, 2))+' MB'+'\n')
test_time = input("Please enter time to test in seconds (if not entered, default of {} seconds is used): ".format(DEFAULT_TEST_TIME))
if test_time == '':
    test_time = DEFAULT_TEST_TIME
    sleeper(test_time)
else:
    sleeper(int(test_time))




report_file.close()
print("--- Dumping logcat...")
logcat_command = "logcat -v year -d"
log_entries = device.shell(logcat_command)
with open(os.path.join(dir_path, DEFAULT_LOGCAT_NAME), "w") as fajl:
    fajl.write(log_entries)
client.remote_disconnect()
