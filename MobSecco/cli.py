import argparse
from MobSecco.colors import color as col
import sys
from MobSecco.MobSecco import MOBSECCO



def header():
	VERSION = __import__('MobSecco').__version__
	print(col.WARNING + "  __  __         _      _____                        \n |  \/  |       | |    / ____|                       \n | \  / |  ___  | |__ | (___    ___   ___  ___  ___  \n | |\/| | / _ \ | '_ \ \___ \  / _ \ / __|/ __|/ _ \ \n | |  | || (_) || |_) |____) ||  __/| (__| (__| (_) |\n |_|  |_| \___/ |_.__/|_____/  \___| \___|\___|\___/ \n {}\n --\n Clonning Cordova Mobile Application\n (c) Sourav Kalal (AnoF-Cyber)\n".format(VERSION) + col.ENDC, file=sys.stderr)



def argument():
    parser = argparse.ArgumentParser(description="Extract the source code and create a clone apk of Cordova Mobile Application")
    parser.add_argument("-f", "--file", help="Path to the APK file", type=str, required=True)
    args = parser.parse_args()
    return args



def main():
	header()
	args = argument()
	apk_tool = MOBSECCO(args.file)
	apk_tool.run()
