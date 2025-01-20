from datetime import datetime, timezone
import socket
import psutil
import requests
import os
import logging
import time

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)


def get_network_interfaces() -> dict[str, list[str]]:
    """Get information about network interfaces and their IP addresses.

    Returns:
        Dict mapping interface names to lists of IP addresses
    """
    interfaces = {}

    # Get all network interfaces
    for interface, addresses in psutil.net_if_addrs().items():
        ip_list = []
        for addr in addresses:
            # Only include IPv4 and IPv6 addresses
            if addr.family == socket.AF_INET:
                ip_list.append(addr.address)
        if ip_list:
            interfaces[interface] = ip_list

    return interfaces


def create_network_embed(interfaces: dict[str, list[str]]) -> dict:
    """Create a Discord embed with network interface information.

    Args:
        interfaces: Dict mapping interface names to lists of IPv4 addresses

    Returns:
        Dict containing the Discord embed data
    """
    # Format network interface info into Discord embed fields
    fields = []
    for interface, ips in interfaces.items():
        fields.append({"name": interface, "value": "\n".join(ips), "inline": True})

    embed = {
        "title": "Network Interfaces",
        "description": f"Network interfaces on {socket.gethostname()}",
        "color": 3447003,  # Blue color
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fields": fields,
    }

    return embed


def send_discord_webhook(webhook_url: str, embed: dict) -> None:
    """Send an embed to a Discord webhook.

    Args:
        webhook_url: The Discord webhook URL
        embed: The embed data to send
    """
    # Prepare the webhook payload
    payload = {"embeds": [embed]}

    # Send webhook request
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            log.info("Successfully sent network interface info to Discord")
        else:
            log.error(f"Failed to send webhook. Status code: {response.status_code}")
    except requests.RequestException as e:
        log.error(f"Error sending webhook: {e}")


def get_check_interval() -> int:
    """Get the check interval from environment variable with fallback to default."""
    try:
        return int(os.getenv("CHECK_INTERVAL", "300"))
    except ValueError:
        log.warning("Invalid CHECK_INTERVAL value, using default of 300 seconds")
        return 300


def main():
    # Get Discord webhook URL from environment variable
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        log.error("DISCORD_WEBHOOK_URL environment variable not set")
        exit(1)

    check_interval = get_check_interval()
    previous_interfaces = None

    log.info(f"Starting network interface monitor with {check_interval}s interval")

    while True:
        current_interfaces = get_network_interfaces()

        # Send update if this is the first check or if interfaces have changed
        if previous_interfaces is None or current_interfaces != previous_interfaces:
            log.info("Network interface changes detected, sending update")
            embed = create_network_embed(current_interfaces)
            send_discord_webhook(webhook_url, embed)
            previous_interfaces = current_interfaces
        else:
            log.debug("No network interface changes detected")

        time.sleep(check_interval)


if __name__ == "__main__":
    main()
