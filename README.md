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


## Quick Install

Copy and run:

First Time Setup

Grant storage access if you want to save log files:

```bash
termux-setup-storage
```
Tap Allow when Android asks for permission.

```bash
pkg update -y && pkg upgrade -y && \
pkg install git python traceroute inetutils -y && \
git clone https://github.com/pars1500/IR-NetScope-Termux.git && \
cd IR-NetScope-Termux && \
pip install -r requirements.txt && \
python main.py
```








## Step-by-Step Installation

### Step 1 - Update Termux

```bash
pkg update -y && pkg upgrade -y
```

### Step 2 - Grant Storage Permission

```bash
termux-setup-storage
```

Tap **Allow** when Android asks for storage permission.

### Step 3 - Install Required Packages

```bash
pkg install git python traceroute inetutils -y
```

### Step 4 - Clone Repository

```bash
git clone https://github.com/pars1500/IR-NetScope-Termux.git
```

### Step 5 - Enter Project Directory

```bash
cd IR-NetScope-Termux
```

### Step 6 - Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 7 - Run Application

```bash
python main.py
```

## Update

```bash
cd ~/IR-NetScope-Termux && git pull
```

## Remove

```bash
rm -rf ~/IR-NetScope-Termux
```

