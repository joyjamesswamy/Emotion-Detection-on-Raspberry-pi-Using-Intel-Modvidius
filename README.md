# Emotion-Detection-on-Raspberry-pi-Using-Intel-Modvidius
8 Face Emotion Detection on Raspberry pi Using Intel Modvidius
Raspberry Pi with Ubuntu 20.04 LTS and OpenVINO Setup

This repository provides step-by-step instructions on how to flash Ubuntu 20.04 LTS onto an SD card for a Raspberry Pi, configure Wi-Fi, upgrade packages, install the Ubuntu Desktop Environment, install the OpenVINO Toolkit, and set up emotion detection using pre-trained models.

Table of Contents

Flash Ubuntu 20.04 LTS to SD Card
Configure Wi-Fi Network
Upgrade Ubuntu Packages
Install Ubuntu Desktop
Install OpenVINO Toolkit
Clone and Set Up OpenVINO Model Zoo
Model Conversion and Setup for Emotion Detection
Run Emotion Detection
1. Flash Ubuntu 20.04 LTS to SD Card

Steps:
Download the Ubuntu 20.04 LTS Server image for Raspberry Pi from the official Ubuntu downloads.
Flash the image to an SD card using tools like Etcher or Raspberry Pi Imager.
Insert the SD card into the Raspberry Pi and boot it up.
2. Configure Wi-Fi Network

Step 1: Create a wpa_supplicant Configuration File
Open the terminal and create the configuration file:
sudo nano /etc/wpa_supplicant.conf
Add the following content to the file:
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=wheel
update_config=1
network={
    ssid="Your Wi-Fi SSID"
    scan_ssid=1
    psk="Your Wi-Fi Password"
    key_mgmt=WPA-PSK
}
Replace Your Wi-Fi SSID and Your Wi-Fi Password with your network credentials.
Replace US with your 2-character country code from the ISO Alpha-2 Code list.
Save and exit:
Press CTRL + X, then Y, and Enter.
Step 2: Connect to the Wi-Fi Network
Run the following command to connect:
sudo wpa_supplicant -B -iwlan0 -c /etc/wpa_supplicant.conf
Obtain an IP address via DHCP:
sudo dhclient -v wlan0
Verify the connection by running the ping command:
ping -c 5 google.com
If successful, the Raspberry Pi is connected to the internet.
3. Upgrade Ubuntu Packages

Step 1: Update the APT Package Cache
Run the following command to update the package repository cache:

sudo apt update
Step 2: Upgrade Existing Packages
Upgrade all installed packages to the latest versions:

sudo apt upgrade
Press Y when prompted and wait for the process to complete.
Step 3: Reboot the System
After upgrading, reboot the Raspberry Pi:

sudo systemctl reboot
4. Install Ubuntu Desktop

Step 1: Install the Desktop Environment
To install Ubuntu GNOME 3 desktop:

sudo apt install ubuntu-desktop
Press Y when prompted and wait for the installation to finish.
Step 2: Reboot to Apply Changes
Reboot the Raspberry Pi:

sudo systemctl reboot
5. Install OpenVINO Toolkit

Step 1: Download and Install OpenVINO
Go to the OpenVINO Toolkit page and download the appropriate version for Ubuntu.
Follow the installation instructions for Ubuntu.
Step 2: Initialize the OpenVINO Environment
Run the following command to set up OpenVINO:

source /opt/intel/openvino_2024/setupvars.sh
6. Clone and Set Up OpenVINO Model Zoo

Step 1: Clone the Open Model Zoo Repository
Clone the OpenVINO Model Zoo repository to your Raspberry Pi:

git clone --recurse-submodules https://github.com/openvinotoolkit/open_model_zoo.git
cd open_model_zoo/
Step 2: Build Demos
Navigate to the demos directory and build the demos:

cd demos
./build_demos.sh
7. Model Conversion and Setup for Emotion Detection

Step 1: Install CMake
You will need CMake to build some components:

sudo apt install cmake
Step 2: Convert a Pre-trained Model to ONNX Format
If you have a pre-trained model (e.g., .pth or other formats), convert it to ONNX format. If your model is already in ONNX format, skip this step.

# Use your own command to convert the model to ONNX format
python3 <convert_script.py> --input_model <model_file.pth> --output_model <model_output.onnx>
Step 3: Convert the ONNX Model to OpenVINO Format
After converting the model to ONNX, use the Model Optimizer to convert it to OpenVINO's XML and BIN format:

mo --input_model /path/to/your/model.onnx --output_dir /path/to/output --data_type FP16
8. Run Emotion Detection

Step 1: Install Required Dependencies
Ensure you have the necessary Python libraries installed:

sudo apt install python3-pip
pip3 install -r requirements.txt
Step 2: Write Python Code for Emotion Detection
Create a Python script (emotion_detection.py) that uses the converted OpenVINO model. Here's a basic template:

import sys
from openvino.inference_engine import IECore

def emotion_detection(model_path, image_path):
    # Initialize inference engine
    ie = IECore()
    net = ie.read_network(model=model_path, weights=model_path.replace(".xml", ".bin"))
    
    # Load model into the device
    exec_net = ie.load_network(network=net, device_name="CPU")
    
    # Read input image, preprocess, and run inference
    # (Implementation of image processing and inference here)
    # Print results

if __name__ == "__main__":
    model_path = sys.argv[2]  # Path to the .xml model file
    image_path = sys.argv[4]  # Path to the input image
    emotion_detection(model_path, image_path)
Step 3: Run Emotion Detection
Run the emotion detection script by providing the model and an image to test:

python3 emotion_detection.py -m /path/to/your/model.xml -i /path/to/input/image.jpg
Additional Configurations

Make OpenVINO available for all users by adding it to .bashrc:

echo "source /opt/intel/openvino_2024/setupvars.sh" >> ~/.bashrc
source ~/.bashrc
Conclusion

By following this guide, you will have a Raspberry Pi running Ubuntu 20.04 LTS, configured to connect to a Wi-Fi network, with the OpenVINO Toolkit installed and set up for emotion detection using a pre-trained model. You can extend this setup to explore other AI models and applications with OpenVINO.
