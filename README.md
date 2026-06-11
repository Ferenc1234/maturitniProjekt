# maturitniProjekt

This project is configured to access a **local AI model** (e.g. [Ollama](https://ollama.ai/)) from inside **GitHub Codespaces** or the **Copilot cloud agent** through an OpenVPN tunnel.

---

## OpenVPN tunnel to a local AI model

### How it works

```
Your machine (AI model on :11434)
        │
        │  OpenVPN tunnel
        ▼
GitHub Codespace / Copilot cloud agent
        │
        └─ curl http://10.8.0.1:11434/api/tags
```

Your machine runs an OpenVPN **server** (or you point both ends at a VPS). The Codespace / Copilot agent runs as an OpenVPN **client** and can reach your locally-running AI model through the tunnel IP.

---

## Setup

### 1 – Generate or obtain an `.ovpn` client config

Export the client configuration from your VPN server (OpenVPN Access Server, PiVPN, or a manual config). The file should contain the server address, certificates, and keys.

### 2 – Store secrets

#### For the **Copilot cloud agent** (`.github/workflows/copilot-setup-steps.yml`)

Open your repository → **Settings → Environments → copilot** and add:

| Name | Type | Value |
|---|---|---|
| `OVPN_CONFIG` | Secret | Full text content of your `.ovpn` file |
| `OVPN_USERNAME` | Secret | VPN username *(only if your server uses `auth-user-pass`)* |
| `OVPN_PASSWORD` | Secret | VPN password *(only if your server uses `auth-user-pass`)* |
| `AI_MODEL_URL` | Variable | Base URL of your AI model, e.g. `http://10.8.0.1:11434` *(defaults to this value)* |

#### For **GitHub Codespaces** (`.devcontainer/`)

Open your repository → **Settings → Secrets and variables → Codespaces** and add the same secrets (`OVPN_CONFIG`, `OVPN_USERNAME`, `OVPN_PASSWORD`). They will be available as environment variables inside your Codespace.

### 3 – Connect from a Codespace terminal

```bash
# Copy your .ovpn config into the Codespace (or decode from secret)
echo "$OVPN_CONFIG" > /tmp/my.ovpn

# Run the helper script
bash .devcontainer/scripts/connect-vpn.sh /tmp/my.ovpn

# Verify the AI model is reachable
curl http://10.8.0.1:11434/api/tags
```

### 4 – Test with Ollama (example)

```bash
curl http://10.8.0.1:11434/api/generate \
  -d '{"model":"llama3","prompt":"Hello!"}'
```

---

## Repository structure

```
.github/
  workflows/
    copilot-setup-steps.yml   # Installs OpenVPN and connects before Copilot starts
.devcontainer/
  devcontainer.json           # Codespaces config (NET_ADMIN + /dev/net/tun)
  scripts/
    connect-vpn.sh            # Helper to connect to VPN in an interactive Codespace
```