# FreePBX Discord IP Truster

## Setup

1. Place `main.py` in `/opt/freepbx-discord-ip-truster` directory.
2. Install dependencies:

    ```bash
    pip install discord.py
    ```

3. Create a systemd service at `/etc/systemd/system/freepbx-discord-ip-truster.service`:

    ```ini
    [Unit]
    Description=FreePBX Discord IP Truster
    After=network.target

    [Service]
    ExecStart=python /opt/freepbx-discord-ip-truster/main.py
    Restart=on-failure
    User=root
    Environment="DISCORD_TOKEN=bot_token_here"

    [Install]
    WantedBy=multi-user.target
    ```

4. Enable and start service:

    ```bash
    sudo systemctl enable freepbx-discord-ip-truster
    sudo systemctl start freepbx-discord-ip-truster
    ```

## Usage

Invite the bot to your server with the `/applications.commands` scope, then use:

```
/iptrust 192.168.1.100
```
