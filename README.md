# DeepIsles Gui

## Overview
Gui on top of the DeepIsles docker container, allows interatictive processing of files in single and batch mode

## Prerequisites
Before installing and running this project, ensure the following software is installed on your system:

1. **Python** (version 3.12 or higher)
2. **Docker**
3. **NVIDIA Docker Toolkit** (if using GPU acceleration with NVIDIA GPUs)

---

## Installation Guide

### 1. Python Installation

#### Step 1.1: Install Required Python Packages
Run the following command to install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Docker Installation

#### Step 2.1: Install Docker
Follow the instructions on the [official Docker website](https://www.docker.com/products/docker-desktop) to install Docker on your system.

#### Step 2.2: Verify Installation
Ensure Docker is installed correctly:
```bash
docker --version
```

### 3. NVIDIA Docker Toolkit Installation (Optional for GPU Acceleration)

#### Linux
#### Step 3.1: Install NVIDIA Drivers
Install the correct NVIDIA drivers for your GPU. You can download them from the [NVIDIA Drivers page](https://www.nvidia.com/Download/index.aspx).

#### Step 3.2: Install NVIDIA Docker Toolkit
Follow these steps to set up NVIDIA Docker Toolkit:
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html
[official Nvidia website]([https://www.docker.com/products/docker-desktop](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html))

#### Step 3.3: Verify NVIDIA Docker Toolkit Installation
Test the setup using:
```bash
docker run --rm --gpus all ubuntu nvidia-smi
```

#### Windows
#### Step 3.1: Settings
Start docker application as administrator.\
Select the settings option from the tray icon.\
In General tab, enable the option "Use the WSL 2 based engine".\
Apply and restart docker.\


---

## Usage
Run main.py to start the gui, use the appended test cases in the code repo to get familiar with the workflows.

---

#### Installers
## Link Windows:
## Link Ubuntu (Version > 20.04):
Optional way to install the deb file sudo dpkg -i <Path-of-the-Deb-Package

