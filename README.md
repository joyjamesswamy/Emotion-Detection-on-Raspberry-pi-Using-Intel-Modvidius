### 1. Flash Ubuntu 20.04 LTS Server to an SD Card

1. Download the **Ubuntu 20.04 LTS Server** image for Raspberry Pi from the [official Ubuntu downloads](https://ubuntu.com/download).
2. Flash the image to an SD card using tools like **Etcher** or **Raspberry Pi Imager**.
3. Insert the SD card into the Raspberry Pi and boot it up.

---

### 

```bash
bash
Copy code
sudo nano /etc/netplan/01-netcfg.yaml

```

```yaml
yaml
Copy code
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: true

```

### **2. Configuring the Wi-Fi Network**

### **Step 1: Create a `wpa_supplicant` Configuration File**

1. Open the terminal and create the configuration file:
    
    ```bash
    bash
    Copy code
    sudo nano /etc/wpa_supplicant.conf
    ```
    
2. Add the following content to the file:
    
    ```
    country=US
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=wheel
    update_config=1
    network={
        ssid="Your Wi-Fi SSID"
        scan_ssid=1
        psk="Your Wi-Fi Password"
        key_mgmt=WPA-PSK
    }
    ```
    
    - Replace `Your Wi-Fi SSID` and `Your Wi-Fi Password` with your network credentials.
    - Replace `US` with your 2-character country code from the [ISO Alpha-2 Code list on Wikipedia](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes).
3. Save and exit:
    - Press `CTRL + X`, then `Y`, and `Enter`.

---

### **Step 2: Connect to the Wi-Fi Network**

1. Use the following command to connect:
    
    ```bash
    sudo wpa_supplicant -B -iwlan0 -c /etc/wpa_supplicant.conf
    ```
    
2. Obtain an IP address via DHCP:
    
    ```bash
    sudo dhclient -v wlan0
    ```
    
3. Verify the connection:
    - Run the `ping` command:
        
        ```bash
        ping -c 5 google.com
        ```
        
    - If successful, the Raspberry Pi is connected to the internet.

---

### **2. Upgrading Ubuntu 20.04 LTS Packages**

### **Step 1: Update the APT Package Cache**

Run the following command to update the package repository cache:

```bash
sudo apt update
```

### **Step 2: Upgrade Existing Packages**

Upgrade all installed packages to the latest versions:

```bash
sudo apt upgrade
```

- Press `Y` when prompted and wait for the process to complete.

### **Step 3: Reboot the System**

After upgrading, reboot the Raspberry Pi:

```bash
sudo systemctl reboot
```

---

### **3. Installing Ubuntu Desktop**

### **Step 1: Install the Desktop Environment**

1. Run the following command to install Ubuntu GNOME 3 desktop:
    
    ```bash
    sudo apt install ubuntu-desktop
    ```
    
2. Press `Y` when prompted and wait for the installation to finish.

### **Step 2: Reboot to Apply Changes**

Reboot the Raspberry Pi:

```bash
sudo systemctl reboot
```

---

### **4. Using Ubuntu Desktop 20.04 LTS**

After rebooting, the **GNOME Display Manager (GDM3)** will load, allowing you to log in to the desktop environment.

---

### 3. Install Ubuntu Desktop GUI

1. Install the desktop environment:
    
    ```bash
    sudo apt update
    sudo apt install ubuntu-desktop
    ```
    
2. Reboot the system:
    
    ```bash
    sudo reboot
    ```
    
3. Upon reboot, the system will boot into the GUI interface.

---

### 4. Install OpenVINO Toolkit

1. Open a browser and download the OpenVINO Toolkit.
2. Install OpenVINO Runtime:
    - Follow the instructions for your specific Ubuntu version on the official OpenVINO website.
3. Initialize the OpenVINO environment:
    
    ```bash
    source /opt/intel/openvino_2024/setupvars.sh
    ```
    

---

---

### 5. Additional Configurations

1. Install **CMake**:
    
    ```bash
    sudo apt install cmake
    ```
    
2. Set up environment variables:
    
    ```bash
    source /opt/intel/openvino_2024/setupvars.sh
    ```
    
3. Make OpenVINO available to all users:

```jsx
sudo usermod -a -G users "$(whoami)"
echo "source /opt/intel/openvino_2024/setupvars.sh" >> ~/.bashrc
source ~/.bashrc
```

1. convert the model type eg. .pth or etc to onnx for movidius openvino 

1. ACTIVATE OPENVINO ENVIRONMENT 

```jsx
	source ./bin/activate
```

1. DOWNLOAD THE MODEL 
2. CONVERT THE MODEL FROM ITS ORIGINAL FORMAT TO ONNX FORMAT
3. after converting the file to onnx model convert the model to xml and bin format 

```jsx
mo --input_model /home/kids/Downloads/ResEmoteNet.onnx --output_dir ./Desktop --Data_type FP16
```

1. Write a python code to run the model
2. emotion_detection.py
3. 

```jsx
python3 emotion_detection.py /
- i 0
- m <path of the model
```
