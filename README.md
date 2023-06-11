# MobSecco

<img src="https://i.ibb.co/Ldc788L/carbon.png" alt="MobSecco">


This Python script enables the cloning of Cordova-based mobile applications to create a new debug APK using the source code, purely for recreational purposes and to bypass security checks. Additionally, the script verifies the presence of outdated versions of Cordova libraries.

## Reference

[Recreating Cordova Mobile Apps to Bypass Security Implementations](https://medium.com/@Ano_F_/recreating-cordova-mobile-apps-to-bypass-security-implementations-8845ff7bdc58 "Recreating Cordova Mobile Apps to Bypass Security Implementations")

## Prerequisites

- Python 3
- NodeJS with NPM
- Java JDK
- Android SDK + Android Studio
- Gradle
- Cordova 

> **Note**:
> The system environment should contain the necessary requirements. The build process relies heavily on specific versions of Cordova and Gradle. It is not possible to determine the exact version used in the original application. To ensure a successful build process, it is important to use compatible or closely related versions.



## Installation
Manual Installation

```bash
  git clone https://github.com/Anof-cyber/MobSecco
  cd MobSecco
  pip install -r requirements.txt
```

Install with PIP
```
pip install mobsecco
```


## Usage

```bash
mobsecco -f ~/path/to/file.apk
```
