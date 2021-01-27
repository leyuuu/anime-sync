curl https://rclone.org/install.sh | sudo bash

rclone copy OneDrive:sync/config.json .

pip3 install -r requirements.txt

python3 main.py
aria2c --seed-time=0 -d downloads -i dlist
rclone copy downloads OneDrive:sync
rclone copy config.json OneDrive:sync