# SIP Configuration for 192.168.10.3

This document describes the SIP/VoIP configuration specific to the server at `192.168.10.3`.

## Environment Variables

Add these to your `.env` file when connecting to `192.168.10.3`:

```bash
# SIP Configuration
VITE_SIP_HOST=192.168.10.3
VITE_SIP_WS_URL=wss://192.168.10.3:8089/ws
VITE_SIP_PASSWORD=0

# AMI WebSocket (Asterisk Manager Interface)
VITE_AMI_WS_URL=wss://192.168.10.3:8384/ami/

# ICE/STUN Server
VITE_ICE_HOST=stun:192.168.10.3:3479

# Call timeout in milliseconds (30 seconds)
VITE_SIP_CALL_TIMEOUT=30000
```

## Configuration Details

| Variable | Value | Description |
|----------|-------|-------------|
| `VITE_SIP_HOST` | `192.168.10.3` | PBX server IP address |
| `VITE_SIP_WS_URL` | `wss://192.168.10.3:8089/ws` | SIP WebSocket URL (port 8089) |
| `VITE_SIP_PASSWORD` | `0` | SIP password prefix (see password logic below) |
| `VITE_AMI_WS_URL` | `wss://192.168.10.3:8384/ami/` | Asterisk Manager Interface WebSocket (port 8384) |
| `VITE_ICE_HOST` | `stun:192.168.10.3:3479` | STUN server for WebRTC ICE |
| `VITE_SIP_CALL_TIMEOUT` | `30000` | Call timeout in milliseconds |

## Password Logic

This site uses a **prefix-based password system**, which differs from the demo site.

### How It Works

The SIP password is dynamically constructed as:

```
SIP Username = VITE_SIP_PASSWORD + extension_number
SIP Password = VITE_SIP_PASSWORD + extension_number
```

For example, for extension `200`:
- SIP Username: `0` + `200` = `0200`
- SIP Password: `0` + `200` = `0200`

### JavaScript Implementation

The application uses this logic to determine the password:

```javascript
authorizationPassword = VA_SIP_PASS_PREFIX + exten;

// Special case: if prefix is long (a fixed password), use it as-is
if (VA_SIP_PASS_PREFIX.length >= 5) {
    VOICEAPPS_UA.uao.authorizationPassword = VA_SIP_PASS_PREFIX;
}
```

## Comparison: Demo Site vs 192.168.10.3

| Setting | Demo Site | 192.168.10.3 |
|---------|-----------|--------------|
| `VITE_SIP_HOST` | `demo-openchs.bitz-itc.com` | `192.168.10.3` |
| `VITE_SIP_WS_URL` | `wss://demo-openchs.bitz-itc.com/ws/` | `wss://192.168.10.3:8089/ws` |
| `VITE_SIP_PASSWORD` | `<set in .env>` (fixed) | `0` (prefix) |
| WebSocket Port | 443 (default) | 8089 |
| AMI Port | N/A | 8384 |
| Password Mode | Fixed (same for all users) | Prefix (appended to extension) |

## Network Ports

Ensure the following ports are accessible:

| Port | Protocol | Service |
|------|----------|---------|
| 8089 | WSS | SIP over WebSocket |
| 8384 | HTTPS/WSS | Asterisk Manager Interface |
| 3479 | UDP | STUN server |

## SSL Certificate Note

The server at `192.168.10.3` uses a certificate issued for `helpline.sematanzania.org`. When accessing via IP address, you may encounter certificate warnings. To bypass in Chrome, type `thisisunsafe` on the warning page.

## Discovered: January 28, 2026

Configuration discovered by analyzing console messages and network requests during:
1. Login with test credentials
2. Join Queue action
3. Leave Queue action

Key console message revealing SIP registration:
```json
{
  "userAgentString": "VoiceApps UA (SIP.js)",
  "displayName": "200",
  "uri": {
    "scheme": "sip",
    "user": "0200",
    "host": "192.168.10.3"
  },
  "authorizationUsername": "0200",
  "authorizationPassword": "0200",
  "transportOptions": {
    "server": "wss://192.168.10.3:8089/ws"
  }
}
```
