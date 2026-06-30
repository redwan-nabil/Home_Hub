# Home Assistant ↔ Google Home Integration

This repository documents a custom Home Assistant integration with Google Home, designed to combine secure cloud account linking with fast local device execution.

The setup uses Google’s ecosystem for authentication, voice intent handling, and device synchronization, while keeping the Home Assistant instance as the source of truth for smart home control. It is built to be reliable, privacy-conscious, and optimized for local network performance.

## Overview

This integration connects:

- **Home Assistant** as the smart home controller
- **Google Home / Google Assistant** as the voice and discovery layer
- **Cloudflare Tunnel** for secure external access
- **mDNS / Local Fulfillment** for fast LAN-based execution where supported

The result is a hybrid architecture that provides:

- Secure account linking
- Fast local control on the home network
- Centralized home automation management
- Lower latency for supported intents
- A clean, maintainable setup for personal or portfolio use

---

## Architecture

### Core Components

- **Server Hardware:** Raspberry Pi 5 with NVMe SSD
- **Home Automation Hub:** Home Assistant
- **Remote Access:** Cloudflare Tunnel
- **Voice Ecosystem:** Google Home Developer Console
- **Cloud APIs:** Google Cloud Console / HomeGraph API
- **Local Discovery:** Multicast DNS (mDNS)

### Flow

1. A user speaks a command to Google Home.
2. Google handles authentication and intent processing.
3. The request is routed to the Home Assistant integration.
4. If local fulfillment is available, Google Home discovers Home Assistant on the LAN via mDNS.
5. Home Assistant executes the command and updates state reporting back to Google when configured.

---

## Setup Guide

### 1) Google Cloud Project Setup

To enable secure state reporting and account integration:

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **HomeGraph API**.
3. Create a **Service Account** and generate a JSON key.
4. Save the file as `SERVICE_ACCOUNT.json` in your Home Assistant configuration directory.

---

### 2) Google Home Developer Console Setup

1. Open the [Google Home Developer Console](https://console.home.google.com/).
2. Create a **Cloud-to-Cloud** integration.
3. Configure account linking using your Cloudflare Tunnel domain.

#### Account Linking URLs

- **Authorization URL:** `https://[YOUR_DOMAIN]/auth/authorize`
- **Token URL:** `https://[YOUR_DOMAIN]/auth/token`
- **Fulfillment URL:** `https://[YOUR_DOMAIN]/api/google_assistant`

#### Required Scopes

Use the following scopes:

- `email`
- `name`

#### OAuth Client ID

Set the OAuth redirect client ID to:

`https://oauth-redirect.googleusercontent.com/r/[YOUR_PROJECT_ID]`

---

### 3) Local Fulfillment Configuration

To enable faster LAN-based execution:

1. Enable **Local Fulfillment** in the Google Home Developer Console.
2. Upload the required local fulfillment SDK bundle for your target runtime.
3. Ensure test URLs remain blank if they interfere with local routing.
4. Configure device discovery with **mDNS** so Google Home can locate the server on the local network.

#### Discovery Settings

- **Protocol:** `mDNS`
- **Service Name:** `_home-assistant._tcp.local`
- **Regex Match:** `.*\._home-assistant\._tcp\.local`

---

### 4) Home Assistant Configuration

Add the Google Assistant integration block to `configuration.yaml`:

```yaml
google_assistant:
  project_id: your-google-project-id
  service_account: !include SERVICE_ACCOUNT.json
  report_state: true
  exposed_domains:
    - switch
    - light
    - script
    - input_boolean
```

Restart Home Assistant after saving the configuration.

---

### 5) OAuth Linking and Device Sync

1. Open the **Google Home** app on your phone.
2. Go to **Devices > Add > Works with Google**.
3. Select the integration you created in the Developer Console.
4. Sign in through your secure Cloudflare Tunnel endpoint using your Home Assistant credentials.
5. Trigger device discovery by saying:

   > Hey Google, sync my devices.

---

## Performance Notes

This setup is especially well-suited to a Raspberry Pi 5 with SSD storage, but a few best practices help keep it stable and responsive.

### Recommended Optimizations

- Keep `report_state` enabled only for entities that truly need it.
- Avoid exposing noisy entity types such as high-frequency sensors or rapidly updating device trackers.
- Prefer built-in Home Assistant integrations over custom command-line sensors when possible.
- Use a memory-friendly log strategy if you are protecting SSD write endurance.
- Ensure `internal_url` is set correctly for LAN-based access when local fulfillment is used.

### Common Pitfalls

- Exposing too many entities can increase memory usage and API traffic.
- Misconfigured URLs can break authentication or local discovery.
- Incorrect SSL handling on local addresses can prevent Google Home from reaching Home Assistant.
- Overly chatty sensors can create unnecessary log noise and system overhead.

---

## Notes

This repository is intended as a clean reference for documenting the Home Assistant and Google Home integration process. It highlights both the cloud-linked setup and the local fulfillment path used for improved responsiveness and reliability.

---

## License

Add your preferred license here.
