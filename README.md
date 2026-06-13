# IR-NetScope-Termux

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Platform](https://img.shields.io/badge/Platform-Termux-green)
![License](https://img.shields.io/badge/License-MIT-orange)
![Status](https://img.shields.io/badge/Status-Active-success)
![Network](https://img.shields.io/badge/Network-Diagnostics-red)

Professional Network Assessment Tool for Android Termux

## Screenshots

### Auto Detection

![Auto Detection](screenshots/auto-detection.jpg)

### Core Network Report

![Core Network Report](screenshots/report-core.jpg)

### VPN & Protocol Readiness

![VPN Protocol Report](screenshots/report-vpn.jpg)




## Installation Guide (Android Termux)

###Step 1 - Update Packages

```bash
pkg update -y && pkg upgrade -y
```

###Step 2 - Grant Storage Permission
```bash
termux-setup-storage
```

###Step 3 - Install Requirements
```bash
pkg install git python traceroute inetutils -y
```

###Step 4 - Clone Repository
```bash
git clone https://github.com/pars1500/IR-NetScope-Termux.git
```
###Step 5 - Enter Project Directory
```bash
cd IR-NetScope-Termux
```
###Step 6 - Install Python Dependencies

```bash
pip install -r requirements.txt
```
###Step 7 - Run Application

```bash
python main.py
```
###Updateh
```bash
cd IR-NetScope-Termux && git pull
```
###Remove
```bash
rm -rf ~/IR-NetScope-Termux
```
