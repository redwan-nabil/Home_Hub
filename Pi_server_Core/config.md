# 🚀 Release Notes

The following updates have been made to the `config.txt` file in the `Pi_server_Core` repository:

1. **PCIe Configuration**:
   - Added `dtparam=pciex1` to enable PCIe x1 support.
   - Added `dtparam=pciex1_gen=3` to configure PCIe to use Gen 3 speeds.

2. **General Enhancements**:
   - Improved comments for better clarity and maintainability.
   - No changes were made to existing configurations.

---

# README

## Overview

This repository contains the `config.txt` file for configuring the Raspberry Pi firmware. The `config.txt` file is a critical configuration file located in the `/boot/firmware/` directory. It allows users to enable or disable hardware interfaces, configure system behavior, and optimize performance for specific use cases.

The latest update introduces support for PCIe x1 and Gen 3 speeds, which enhances the Raspberry Pi's compatibility and performance with PCIe devices.

---

## File Structure

The `config.txt` file is structured into sections and parameters that control various aspects of the Raspberry Pi's hardware and software configuration. Below is a breakdown of the key sections and parameters:

### General Settings
- **`dtparam=i2c_arm=on`**: Enables the I2C interface.
- **`dtparam=spi=on`**: Enables the SPI interface.
- **`dtparam=audio=on`**: Enables the onboard audio interface.
- **`camera_auto_detect=1`**: Automatically loads overlays for detected cameras.
- **`display_auto_detect=1`**: Automatically loads overlays for detected DSI displays.
- **`auto_initramfs=1`**: Automatically loads initramfs files if found.
- **`dtoverlay=vc4-kms-v3d`**: Enables the DRM VC4 V3D driver for improved graphics performance.
- **`max_framebuffers=2`**: Sets the maximum number of framebuffers to 2.
- **`disable_fw_kms_setup=1`**: Prevents the firmware from creating an initial `video=` setting in `cmdline.txt`.
- **`arm_64bit=1`**: Enables 64-bit mode.
- **`disable_overscan=1`**: Disables compensation for displays with overscan.
- **`arm_boost=1`**: Enables maximum CPU performance as allowed by the firmware and board.

### Compute Module 4 (CM4) Specific Settings
- **`otg_mode=1`**: Enables host mode on the 2711 built-in XHCI USB controller. This line should be removed if the legacy DWC2 controller is required or if USB support is not needed.

### Compute Module 5 (CM5) Specific Settings
- **`dtoverlay=dwc2,dr_mode=host`**: Configures the DWC2 USB controller in host mode.

### Universal Settings
- **`enable_uart=1`**: Enables the UART interface.
- **`dtoverlay=gpio-fan,gpiopin=4,temp=60000`**: Configures a GPIO fan to activate when the temperature exceeds 60°C.
- **`dmi_enable_4kp60=1`**: Enables support for 4K resolution at 60Hz.

### Performance Enhancements
- **Maximum Stable Overclock** (commented out by default):
  - `arm_freq=2800`: Sets the CPU frequency to 2800 MHz.
  - `gpu_freq=900`: Sets the GPU frequency to 900 MHz.
  - `over_voltage_delta=50000`: Increases the CPU voltage for stability during overclocking.
- **`usb_max_current_enable=1`**: Enables maximum USB power output.

### New PCIe Configuration
- **`dtparam=pciex1`**: Enables PCIe x1 support.
- **`dtparam=pciex1_gen=3`**: Configures PCIe to use Gen 3 speeds for improved performance.

---

## Usage

1. **Location**: Place the `config.txt` file in the `/boot/firmware/` directory of your Raspberry Pi's boot partition.
2. **Editing**: Use a text editor to modify the file. Ensure you have proper permissions to edit the file.
3. **Reboot**: After making changes, reboot the Raspberry Pi for the new settings to take effect.

---

## Notes

- **Hardware Compatibility**: Some settings may not be compatible with all Raspberry Pi models. Refer to the official Raspberry Pi documentation for compatibility details.
- **Overclocking**: Overclocking settings are commented out by default. Use them cautiously, as they may void your warranty or cause hardware instability.
- **PCIe Settings**: The newly added PCIe parameters are intended for advanced users who require PCIe functionality. Ensure your hardware supports these configurations before enabling them.

---

## Troubleshooting

- If the Raspberry Pi fails to boot after modifying the `config.txt` file, you can revert to the default configuration by removing the SD card, inserting it into another device, and editing the `config.txt` file to restore previous settings.
- For detailed information about each parameter, visit the official Raspberry Pi documentation: [http://rptl.io/configtxt](http://rptl.io/configtxt).

---

## Contributing

Contributions to improve or extend the `config.txt` file are welcome. Please submit a pull request with a detailed explanation of your changes.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.