# Pi_server_Core Configuration Guide

This document provides a detailed explanation of the `config.txt` file used in the `Pi_server_Core` project. The `config.txt` file is a critical configuration file for Raspberry Pi devices, allowing users to enable or disable hardware interfaces, configure display settings, and optimize performance.

## Overview

The `config.txt` file is used to configure various hardware and software settings for the Raspberry Pi. It is located in the `/boot` directory and is read during the boot process. Modifications to this file can impact the functionality and performance of the device.

For more options and detailed information, refer to the official Raspberry Pi documentation: [Raspberry Pi Configuration Documentation](http://rptl.io/configtxt).

---

## Configuration Details

### 1. **Hardware Interfaces**
The following hardware interfaces are enabled or can be enabled by uncommenting the respective lines:
- **I2C Interface**: Enabled using `dtparam=i2c_arm=on`.
- **SPI Interface**: Enabled using `dtparam=spi=on`.
- **I2S Interface**: Disabled by default. Uncomment `#dtparam=i2s=on` to enable.

### 2. **Audio**
Audio support is enabled by default:
```plaintext
dtparam=audio=on
```
This loads the `snd_bcm2835` audio driver.

### 3. **Camera and Display Auto-Detection**
- **Camera Auto-Detection**: Automatically loads overlays for detected cameras.
  ```plaintext
  camera_auto_detect=1
  ```
- **DSI Display Auto-Detection**: Automatically loads overlays for detected DSI displays.
  ```plaintext
  display_auto_detect=1
  ```

### 4. **Initramfs Auto-Loading**
Automatically loads `initramfs` files if they are found:
```plaintext
auto_initramfs=1
```

### 5. **Graphics and Display Settings**
- **Enable DRM VC4 V3D Driver**: Improves GPU performance.
  ```plaintext
  dtoverlay=vc4-kms-v3d
  max_framebuffers=2
  ```
- **Disable Firmware KMS Setup**: Prevents the firmware from creating an initial `video=` setting in `cmdline.txt`. The kernel's default is used instead.
  ```plaintext
  disable_fw_kms_setup=1
  ```

### 6. **64-Bit Mode**
Enables 64-bit mode for the ARM processor:
```plaintext
arm_64bit=1
```

### 7. **Display Overscan**
Disables compensation for displays with overscan:
```plaintext
disable_overscan=1
```

### 8. **Performance Boost**
Enables the Raspberry Pi to run as fast as the firmware and board allow:
```plaintext
arm_boost=1
```

---

## Conditional Settings

### [cm4] - Raspberry Pi Compute Module 4
- Enables host mode on the built-in XHCI USB controller:
  ```plaintext
  otg_mode=1
  ```
  **Note**: Remove this line if the legacy DWC2 controller is required (e.g., for USB device mode) or if USB support is not needed.

### [cm5] - Raspberry Pi Compute Module 5
- Configures the DWC2 USB controller in host mode:
  ```plaintext
  dtoverlay=dwc2,dr_mode=host
  ```

---

## Universal Settings

### UART
Enables the UART interface for serial communication:
```plaintext
enable_uart=1
```

### GPIO Fan Control
Configures a GPIO-controlled fan:
- **GPIO Pin**: 4
- **Temperature Threshold**: 60°C
  ```plaintext
  dtoverlay=gpio-fan,gpiopin=4,temp=60000
  ```

### 4K Display Support
Enables support for 4K resolution at 60Hz:
```plaintext
dmi_enable_4kp60=1
```

---

## Optional Overclocking

### Maximum Stable Overclock
The following settings are commented out by default. Uncomment and adjust these values to overclock the Raspberry Pi:
- **ARM Frequency**: `2800 MHz`
- **GPU Frequency**: `900 MHz`
- **Over Voltage Delta**: `50000`
  ```plaintext
  #arm_freq=2800
  #gpu_freq=900
  #over_voltage_delta=50000
  ```

**Warning**: Overclocking can void your warranty and may cause hardware instability or damage. Proceed with caution.

---

## USB Power Configuration

### Maximum USB Power
Enables maximum USB power output:
```plaintext
usb_max_current_enable=1
```

---

## Notes
- Additional overlays and parameters are documented in `/boot/firmware/overlays/README`.
- Some settings may impact device functionality. Refer to the official documentation for more details: [Raspberry Pi Configuration Documentation](http://rptl.io/configtxt).

---

## Changelog
- **Initial Version**: Added `config.txt` with default and optional configurations for hardware interfaces, performance, and display settings.

---

## License
This configuration file is provided as part of the `Pi_server_Core` project. Use and modify it as needed for your Raspberry Pi setup.