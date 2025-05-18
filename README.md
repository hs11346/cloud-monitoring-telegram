# Cloud Monitoring Telegram Bot Setup

This repository provides a basic template and instructions for setting up a simple Python-based monitoring script as a background service on a Linux cloud server (e.g., DigitalOcean, AWS EC2, Linode, etc.) using `systemd`. The script will send notifications via a Telegram bot.

**Intended Audience:** Beginners learning to deploy simple, long-running scripts on cloud servers.

## Features

* Basic Python script template for sending Telegram messages.
* Example `systemd` service configuration for running the script reliably.
* Helper scripts to start, stop, and check the status of the service.

## Applications
What can you do with this? Anything from serious applications to quality of life improvements, like:
* Running trading bots and sending live updates to yourself.
* Scrapping websites or news sources continuously.
* Setting up regular reminders.

## Prerequisites

1.  **A Linux Cloud Server:** Any modern distribution that uses `systemd` (Ubuntu 16.04+, Debian 8+, CentOS 7+, Fedora 15+). Examples include a DigitalOcean Droplet.
2.  **SSH Access:** You need to be able to connect to your server via SSH.
3.  **Python 3:** Usually pre-installed. Verify with `python3 --version`.
4.  **pip (Python Package Installer):** To install dependencies. Install if needed (e.g., `sudo apt update && sudo apt install python3-pip` on Debian/Ubuntu).
5.  **Git:** To clone this repository (e.g., `sudo apt install git`).
6.  **Telegram Bot Token:** Obtain one by talking to the [BotFather](https://t.me/botfather) on Telegram.
7.  **Telegram Chat ID:** The ID of the chat (user, group, or channel) where the bot should send messages. 

## Setup Instructions

1.  **Connect to your Server:**
    ```bash
    ssh your_username@your_server_ip
    ```

2.  **Clone your Repository:**
    ```bash
    git clone <your-repository-url> # Replace with your repo URL
    ```
    * For private repos, it is recommended that you use the "Deploy Keys" function of Github. You can refer to this [link](https://dylancastillo.co/posts/how-to-use-github-deploy-keys.html) for instructions.

3.  **Configure the Python Script:**
    * Navigate to the Python script directory: `cd python_scripts`
    * Install the required Python library:
        ```bash
        pip install requests
        ```
    * Edit the script (`telegram_bot_template.py`) using `nano` or `vim`:
        ```bash
        nano telegram_bot_template.py
        ```
    * **Replace placeholders:**
        * Update `TELEGRAM_TOKEN` with your actual bot token.
        * Update `chat_id` with your target Telegram chat ID.
        * **Crucially:** Modify the `while True:` loop. Replace `# do something` and `send_message("YOUR DATA")` with your actual monitoring logic (e.g., check disk space, ping a server, check website status) and the message you want to send.

4.  **Create the systemd Service File:**
    * You need root privileges for this. Use `sudo`.
    * Create and edit the service file. We'll name it `myscript.service` to match the helper scripts.
        ```bash
        sudo nano /etc/systemd/system/myscript.service
        ```
    * Paste the following content into the file. **Adjust paths and user/group as needed.**

        ```ini
        [Unit]
        Description=My Custom Telegram Monitoring Bot
        After=network.target

        [Service]
        # Consider creating a dedicated user/group instead of using root or your own user
        User=your_linux_user # CHANGE THIS to the user who will run the script
        Group=your_linux_group # CHANGE THIS to the group for the user

        # IMPORTANT: Update this path if you cloned the repo elsewhere
        WorkingDirectory=/home/your_linux_user/cloud-monitoring/python_scripts # CHANGE THIS to the correct absolute path
        # IMPORTANT: Ensure the path to python3 and the script are correct
        ExecStart=/usr/bin/python3 /home/your_linux_user/cloud-monitoring/python_scripts/telegram_bot_template.py # CHANGE THIS to the correct absolute path

        Restart=on-failure
        RestartSec=5

        [Install]
        WantedBy=multi-user.target
        ```

    * **Explanation:**
        * `User`/`Group`: The Linux user/group the script runs as. Avoid `root`. Make sure this user has permissions to read the script file.
        * `WorkingDirectory`: The *absolute path* to the directory containing `telegram_bot_template.py`.
        * `ExecStart`: The *absolute path* to the `python3` executable and the *absolute path* to your script (`telegram_bot_template.py`). Find the Python path with `which python3`.
        * Save and close the editor (Ctrl+X, then Y, then Enter in `nano`).

5.  **Set Permissions and Reload systemd:**
    ```bash
    sudo chmod 644 /etc/systemd/system/myscript.service
    sudo systemctl daemon-reload # Tell systemd about the new file
    ```

6.  **Enable the Service (to start on boot):**
    ```bash
    sudo systemctl enable myscript.service
    ```

## Managing the Service

You can now manage your monitoring bot service using `systemctl` directly or the provided helper scripts (make sure they are executable: `chmod +x scripts/*.sh`).

* **Start:**
    ```bash
    sudo ./scripts/start.sh
    ```
    OR
    ```bash
    sudo systemctl start myscript.service
    ```

* **Stop:**
    ```bash
    sudo ./scripts/stop.sh
    ```
    OR
    ```bash
    sudo systemctl stop myscript.service
    ```

* **Check Status:**
    ```bash
    sudo ./scripts/status.sh
    ```
    OR
    ```bash
    sudo systemctl status myscript.service
    ```
    (This shows if it's running, any recent errors, etc.)

* **View Logs:**
    ```bash
    sudo journalctl -u myscript.service
    ```
    * To follow logs in real-time: `sudo journalctl -f -u myscript.service`
    * To see the last 100 lines: `sudo journalctl -n 100 -u myscript.service`

## Customization

* The core logic is in `telegram_bot_template.py`. Modify it to perform the specific monitoring tasks you need.
* Adjust the `myscript.service` file if you change file locations, user, or script name. Remember to run `sudo systemctl daemon-reload` after modifying the service file.

## Contributing

Feel free to fork this repository, make improvements, and submit pull requests.
