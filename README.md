# Raspberry Pi TFT Web Image Controller (ST7789 SPI Display)

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Compatible-red)
![SPI](https://img.shields.io/badge/Interface-SPI-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A web-based controller for a **2.4" ST7789 SPI TFT display** using Raspberry Pi.  
Upload, crop, zoom, and invert images through a browser interface and display them on the TFT screen in real time.
# Raspberry Pi TFT Web Image Controller (ST7789 SPI Display)

A **web-based image controller for SPI TFT displays** using Raspberry Pi.  
This project allows users to **upload, crop, zoom, invert, and display images** on a **2.4" ST7789 TFT screen (320×240)** through a browser interface.

The system uses **Flask for the web server**, **Pillow for image processing**, and **SPI communication** to render images on the TFT display.

---

# UI Preview

Below is the web interface used to edit and send images to the TFT display.

![UI Preview](screenshots/ui_preview.png)

---

# Features

- Upload images directly from browser
- Crop image to **320×240 TFT resolution**
- Zoom in / Zoom out
- Invert image colors
- Live preview before display
- Send image directly to TFT display
- Works over **WiFi through web interface**
- Compatible with **Raspberry Pi OS Lite**

---

# Hardware Requirements

- Raspberry Pi (tested on **Raspberry Pi 3B+**)
- 2.4" SPI TFT Display
- Driver: **ST7789**
- Resolution: **320 × 240**
- Interface: **SPI**
- Jumper wires

---

# TFT to Raspberry Pi Wiring

| TFT Pin | Function | Raspberry Pi Pin |
|------|------|------|
| VCC | Power | 3.3V (Pin 1) |
| GND | Ground | GND (Pin 6) |
| CS | Chip Select | GPIO8 / CE0 (Pin 24) |
| RESET | Reset | GPIO25 (Pin 22) |
| DC | Data/Command | GPIO24 (Pin 18) |
| SDI (MOSI) | SPI Data | GPIO10 MOSI (Pin 19) |
| SCK | SPI Clock | GPIO11 SCLK (Pin 23) |
| LED | Backlight | 3.3V (Pin 17) |
| SDO (MISO) | SPI Read | GPIO9 MISO (Pin 21) |

---

# Enabling SPI on Raspberry Pi

Enable SPI using:

```bash
sudo raspi-config
```

Navigate to:

```
Interface Options → SPI → Enable
```

Verify SPI is enabled:

```bash
ls /dev/spidev*
```

Expected output:

```
/dev/spidev0.0
/dev/spidev0.1
```

---

# Software Dependencies

Install required libraries:

```bash
pip3 install flask pillow st7789
```

---

# Project Architecture

```
Browser UI
     ↓
Flask Web Server
     ↓
Image Processing (Pillow)
     ↓
SPI Communication
     ↓
ST7789 TFT Display
```

---

# Running the Project

Clone the repository:

```bash
git clone https://github.com/ALT3RNATOR/Raspberry-Pi-TFT-Web-Image-Controller-ST7789-SPI-Display.git
cd tft-web-controller
```
Run the program:

```bash
python3 wifi_display.py
```

Find your Raspberry Pi IP address:

```bash
hostname -I
```

Open the interface in browser:

```
http://<raspberry_pi_ip>:5000
```

---

# Repository Structure

```
tft-web-controller
│
├── wifi_display.py
├── README.md
├── LICENSE
├── requirements.txt
│
├── screenshots
│   └── ui_preview.png
│
└── docs
    └── wiring_diagram.png
```

---

# Future Improvements

Potential enhancements:

- Live TFT screen streaming to browser
- GIF animation support
- Image slideshow mode
- Mobile UI optimization
- Drag & drop image upload
- Camera streaming to TFT

---

# License

This project is licensed under the **MIT License**.

---

# Author

**Ankit Singh**
