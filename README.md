# MQTT Producer Example (Temperature and Humidity Sensor)

## Installation

install dependencies

```bash
pip3 install -r requirements.txt
```

## Usage

run the code by executing this command:

```bash
python3 run.py
```

## Service Installation and Configuration

```bash
sudo cp sensorreader.service /etc/systemd/system/sensorreader.service
sudo systemctl daemon-reload
sudo systemctl start sensorreader.service
sudo systemctl enable sensorreader.service
```
