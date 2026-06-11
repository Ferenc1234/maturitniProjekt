#!/usr/bin/env bash
# connect-vpn.sh – connect to your OpenVPN server from inside a Codespace.
#
# Usage:
#   bash .devcontainer/scripts/connect-vpn.sh <path-to-config.ovpn>
#
# Environment variables (optional):
#   OVPN_USERNAME  – VPN username  (required if the server uses auth-user-pass)
#   OVPN_PASSWORD  – VPN password  (required if the server uses auth-user-pass)
#
# Example (credentials stored as Codespaces secrets):
#   OVPN_USERNAME=$OVPN_USERNAME OVPN_PASSWORD=$OVPN_PASSWORD \
#     bash .devcontainer/scripts/connect-vpn.sh ~/my-server.ovpn

set -euo pipefail

OVPN_CONFIG_FILE="${1:-}"

if [ -z "$OVPN_CONFIG_FILE" ]; then
  echo "Usage: $0 <path-to-config.ovpn>"
  exit 1
fi

if [ ! -f "$OVPN_CONFIG_FILE" ]; then
  echo "Error: config file not found: $OVPN_CONFIG_FILE"
  exit 1
fi

WORK_CONFIG=$(mktemp --suffix=.ovpn)
cp "$OVPN_CONFIG_FILE" "$WORK_CONFIG"

# Append auth-user-pass block if credentials are available
if [ -n "${OVPN_USERNAME:-}" ] && [ -n "${OVPN_PASSWORD:-}" ]; then
  AUTH_FILE=$(mktemp)
  printf '%s\n%s\n' "$OVPN_USERNAME" "$OVPN_PASSWORD" > "$AUTH_FILE"
  echo "auth-user-pass $AUTH_FILE" >> "$WORK_CONFIG"
  echo "Credentials file written."
fi

echo "Starting OpenVPN..."
sudo openvpn --config "$WORK_CONFIG" --daemon --log /tmp/openvpn.log

echo "Waiting for tunnel interface (tun0) to come up..."
for i in $(seq 1 30); do
  if ip addr show tun0 2>/dev/null | grep -q "inet "; then
    echo ""
    echo "VPN connected successfully!"
    ip addr show tun0
    echo ""
    echo "Your local AI model should now be reachable."
    echo "Test with:  curl http://10.8.0.1:11434/api/tags"
    exit 0
  fi
  printf "."
  sleep 1
done

echo ""
echo "Warning: tun0 interface not detected after 30 seconds."
echo "Check the log with:  cat /tmp/openvpn.log"
exit 1
