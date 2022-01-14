import os
from ppadb.client import Client as AdbClient
from pyaxmlparser import APK
import sys

DEFAULT_CAMERA_IP = '10.163.11.78'
DEFAULT_PORT = 5555
DEFAULT_DIR = '/media/sf_tmp/CS'


def install_app(apk_n):
    try:
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

    print("Static analysis for: ", apk.packagename)
    os.chdir(DEFAULT_DIR)
    print("1.a) Applications shall not have com.securityandsafetythings namespace:"+"\033[93m")
    os.system("apkanalyzer manifest application-id "+"{}".format(apk_filename))
    print('\033[0m')
    print("1.b) Application should be release versions / Not debuggable:"+"\033[93m")
    os.system("apkanalyzer manifest debuggable "+"{}".format(apk_filename))
    print('\033[0m')
    print("1.c) Application has FGS permission declared:"+"\033[93m")
    os.system("apkanalyzer manifest print "+"{}".format(apk_filename)+"| grep -i android.permission.FOREGROUND_SERVICE")
    print('\033[0m')
    print('\r')
    print('------------------------------------------------')
    print('Application classification for: ', apk.packagename)
    print('Uses Native library:'+'\033[93m')
    os.system("apkanalyzer files list "+"{}".format(apk_filename)+"| grep -i .so$")
    print('\033[0m')
    print('a) Uses SNPE:'+'\033[93m')
    os.system("apkanalyzer files list "+"{}".format(apk_filename)+"| egrep -i 'lib.*skel.so$|hexa'")
    print('\033[0m')
    print('b) Uses SNPE:'+'\033[93m')
    os.system("apkanalyzer dex packages "+"{}".format(apk_filename)+"| egrep -w 'com.qualcomm.qti.snpe$'")
    print('\033[0m')
    print('a) Uses TFlite:'+'\033[93m')
    os.system("apkanalyzer files list "+"{}".format(apk_filename)+"| egrep -i 'tflite'")
    print('\033[0m')
    print('b) Uses TFlite:'+'\033[93m')
    os.system("apkanalyzer dex packages "+"{}".format(apk_filename)+"| egrep -w 'org.tensorflow$|GpuDelegate|NnApiDelegate|HexagonDelegate|dsp'")
    print('\033[0m')

    working = input("Please check if the app is working on the camera and then press any key.")
    device.uninstall(apk.packagename)
    choice = input("Please enter n to continue or q to exit:")
    if choice == 'n':
        pass
    elif choice == 'q':
        break

client.remote_disconnect()
