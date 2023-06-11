from MobSecco.colors import color as col
import os
from pyaxmlparser import APK
import subprocess
import shutil
import re


class MOBSECCO():
    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.package_name = None
        self.unzip_folder = None
        self.new_folder = None
        self.platform_version = None
        self.plugin_metadata = []


    def validate_apk_file(self):
        if not os.path.exists(self.apk_path):
            print(col.FAIL + "File Does Not Exist")
            exit(1)

        if not os.path.isfile(self.apk_path):
            print(col.FAIL + "Invalid Path Provided")
            exit(1)

        if not self.apk_path.endswith(".apk"):
            print(col.FAIL + "Invalid APK file format. Please provide a valid APK file.")
            exit(1)

        try:
            apk = APK(self.apk_path)
            self.package_name = apk.packagename
        except FileNotFoundError:
            print(col.FAIL + "APK file not found or is not a valid APK.")
            exit(1)


    def check_tool_installed(self, tool_name, command):
        if shutil.which(command) is not None:
            print(col.OKGREEN + f"Found {tool_name} is already installed")
        else:
            print(col.FAIL + f"{tool_name} is not installed")
            exit(1)

    def apkdetails(self):
        apk = APK(self.apk_path)
        self.package_name = apk.packagename
        self.appname = apk.application
        print(col.WARNING + f"Package: {self.package_name}")
        print(col.WARNING + f"App Name: {self.appname}")
        

    def unzip_apk(self):
        try:
            apk_name = os.path.basename(self.apk_path)
            apk_name = os.path.splitext(apk_name)[0]
            self.unzip_folder = apk_name + "-original"
            self.zipapk = apk_name + ".zip"
            
            print(col.ENDC + "Changing APK to ZIP")
            shutil.copy2(self.apk_path, self.zipapk)

            print(col.ENDC + "Unzipping APK File")
            

            if os.path.exists(self.unzip_folder):
                print(col.OKGREEN + f"{self.unzip_folder} folder already exists.")
                return 
            
            shutil.unpack_archive(self.zipapk, self.unzip_folder)
            print(col.OKGREEN + f"APK file successfully unzipped into {self.unzip_folder} folders")
            return 
        except FileNotFoundError:
            print("APK file not found.")
            print(col.FAIL + "APK file not found.")
            exit(1)


    def validate_cordova(self):
        cordova_plugins_path = os.path.join(self.unzip_folder, "assets", "www", "cordova_plugins.js")
        if not os.path.exists(cordova_plugins_path):
            print(col.FAIL + f"cordova_plugins.js file was not found in {self.unzip_folder}, Make sure provided apk is built with Cordova")
            exit(1)
        else:
            print(col.OKGREEN + f"Found Cordova Plugins in {cordova_plugins_path}")


    def create_cordova_project(self):
        try:
            self.new_folder = self.appname + "-new"
            print(col.WARNING + f"Creating a New Cordova Project")

            appname_arg = f'"{self.appname}"'
            foldername_arg =f'"{self.new_folder}"'


            command = f"cordova create {foldername_arg} {self.package_name} {appname_arg}"

            if os.path.exists(self.new_folder):
                print(col.OKGREEN + f"Found {self.new_folder} is already installed")
                return

            subprocess.run(command, shell=True, check=True)
            print(col.OKGREEN + f"New Cordova project created in {self.new_folder} folder")
            
        except subprocess.CalledProcessError as e:
            print(col.FAIL + f"Failed to create Cordova project. Error: {e}")
            exit(1)


    def get_platform_version(self):
        cordova_js_path = os.path.join(self.unzip_folder, "assets", "www", "cordova.js")
        try:
            with open(cordova_js_path, "r") as file:
                for line in file:
                    if "PLATFORM_VERSION_BUILD_LABEL" in line:
                        version_start_index = line.find("'") + 1
                        version_end_index = line.rfind("'")
                        self.platform_version = line[version_start_index:version_end_index]
                        break
                else:
                    self.platform_version = "latest"
            print(col.WARNING + f"Found Cordova Android Platform Version {self.platform_version}")
        except FileNotFoundError:
            print(col.FAIL + f"cordova.js file not found in the unzip folder: {self.unzip_folder}")
            exit(1)



    def add_android_platform(self):
        if self.new_folder is None:
            print(col.FAIL + "Cordova project folder not found. Cannot add Android platform.")
            exit(1)

        try:
            command = f"cordova platform add android@{self.platform_version}"
            subprocess.run(command, shell=True, check=True, cwd=self.new_folder)
            print(col.WARNING + f"Android platform version {self.platform_version} added to Cordova project in {self.new_folder} folder")
        except subprocess.CalledProcessError as e:
            print(col.FAIL + f"Failed to add Android platform to Cordova project. Error: {e}")
            exit(1)



    def get_plugin_metadata(self):
        print(col.WARNING + f"Trying to get all plugins")
        cordova_plugins_path = os.path.join(self.unzip_folder, "assets", "www", "cordova_plugins.js")
        try:
            with open(cordova_plugins_path, "r") as file:
                content = file.read()
                metadata_match = re.search(r"module.exports.metadata = ({.*?});", content, re.DOTALL)
                if metadata_match:
                    metadata_content = metadata_match.group(1)
                    metadata = eval(metadata_content)
                    for key, value in metadata.items():
                        plugin_info = f"{key}@{value}"
                        self.plugin_metadata.append(plugin_info)
                    
                    for allplugins in self.plugin_metadata:
                        print(col.OKBLUE + f"Plugin Found: {allplugins}")
                else:
                    print(col.WARNING + f"No plugin found in cordova_plugins.js file")
        except FileNotFoundError:
            print(col.FAIL + f"cordova_plugins.js file not found in the unzip folder: '{self.unzip_folder}'")
            exit(1)


    def install_plugins(self):
        print(col.WARNING + f"Installing Cordova plugins")
        for plugin_info in self.plugin_metadata:
            try:
                command = f"cordova plugin add {plugin_info}"
                subprocess.check_call(command, shell=True, cwd=self.new_folder)
                print(col.OKBLUE + f"Installed plugin: {plugin_info}")
            except subprocess.CalledProcessError as e:
                print(col.FAIL + f"Failed to install plugin: {plugin_info}")
                print(e)
        print(col.OKGREEN + f"Cordova plugin installation completed.")


    def audit_plugins(self):

        print(col.WARNING + f"Cordova plugins Audit")

        try:
            command = f"npm audit"
            subprocess.check_call(command, shell=True, cwd=self.new_folder)
        except subprocess.CalledProcessError as e:
            print(e)
        print(col.OKGREEN + f"Audit Completed")


    def copy_source_code(self):
        print(col.WARNING + f"Copying Source Code from APK to Cordova Project")
        src_folder = os.path.join(self.unzip_folder, "assets", "www")
        dest_folder = os.path.join(self.new_folder, "www")
        excluded_files = ["cordova_plugins.js", "cordova.js"]
        excluded_folders = ["plugins", "cordova-js-src"]

        for root, dirs, files in os.walk(src_folder):
            # Exclude specific folders
            dirs[:] = [d for d in dirs if d not in excluded_folders]

            # Exclude specific files
            files[:] = [f for f in files if f not in excluded_files]

            for file in files:
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_folder, os.path.relpath(src_path, src_folder))
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)
                print(col.WARNING + f"Copied: {os.path.relpath(dest_path, self.new_folder)}")

        print(col.OKGREEN + f"Copying files completed")



    def compile_apk(self):

        print(col.WARNING + f"Trying to compile new Cordova apk")

        try:
            command = f"cordova build android --packageType=apk"
            subprocess.check_call(command, shell=True, cwd=self.new_folder)
            print(col.OKGREEN + f"Compile Complete")
        except subprocess.CalledProcessError as e:
            print(e)

        



    
    def run(self):
        self.validate_apk_file()
        print(col.BOLD + "Checking required tools installed")
        self.check_tool_installed("Node.js", "node")
        self.check_tool_installed("ADB", "adb")
        self.check_tool_installed("npm", "npm")
        self.check_tool_installed("Gradle", "gradle")
        self.apkdetails()
        self.unzip_apk()
        self.validate_cordova()
        self.create_cordova_project()
        self.get_platform_version()
        self.get_plugin_metadata()
        self.copy_source_code()
        self.add_android_platform()
        self.install_plugins()
        self.audit_plugins()
        self.compile_apk()