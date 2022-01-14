import os
from ppadb.client import Client as AdbClient
from pyaxmlparser import APK
import sys

DEFAULT_CAMERA_IP = '192.168.1.227'
DEFAULT_PORT = 5555
DEFAULT_DIR = '/media/sf_tmp/CS'


def install_app(apk_n):
    try:
        device.shell("logcat -c")
        device.install(apk_n, grand_all_permissions=True)
    except Exception as e:
        print(e)
        sys.exit()


# Checking if adb server is running
try:
    os.system('adb start-server')
except:
    pass

# creating client connection to the server
client = AdbClient(host="127.0.0.1", port=5037)

# connecting to the camera
device_IP = DEFAULT_CAMERA_IP

client.remote_connect(device_IP, DEFAULT_PORT)

device = client.device(device_IP+':'+str(DEFAULT_PORT))

while True:
    dir_list = []
    dir_list = os.listdir(DEFAULT_DIR)
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
    ###########################################

    client.remote_connect(device_IP, DEFAULT_PORT)
    install_app(os.path.join(DEFAULT_DIR, apk_filename))

    # Preparing apk to be installed
    apk = APK(os.path.join(DEFAULT_DIR, apk_filename))


    working = input("Would you like to dump the logcat(y/n)? ")
    if working == 'y':
        logcat_command = "logcat -v year -d"
        log_entries = device.shell(logcat_command)
        with open(os.path.join('.', apk.packagename+".MTK.txt"), "w") as fajl:
            fajl.write(log_entries)
    elif working == 'n':
        continue
    device.uninstall(apk.packagename)
    choice = input("Please enter n to continue or q to exit:")
    if choice == 'n':
        pass
    elif choice == 'q':
        break

client.remote_disconnect()