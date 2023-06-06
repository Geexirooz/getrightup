# getrightup
This tool gives you daily write-ups to read from [PentesterLand](https://pentester.land/) website.

# Prerequisites
## Install Firefox
```
sudo apt update -y && sudo apt upgrade -y && apt install firefox
```

## Install geckodriver
Download [Geckodriver](https://github.com/mozilla/geckodriver/releases), extract it and then put it in your PATH (suggestion -> `~/.local/bin`)

# Setup
```
git clone https://github.com/Geexirooz/getrightup.git
pip3 install -r requirements.txt
```

# Run 
Tested with Python 3.11.2
```
python3 getrightup.py -d https://discord.com/api/webhooks/YOUR_WEBHOOK
```

# Crontab
Every 2 hours
```
0 */2 * * * cd /path/to/getrightup/; /usr/bin/python3 getrightup.py -d https://discord.com/api/webhooks/YOUR_WEBHOOK
```
