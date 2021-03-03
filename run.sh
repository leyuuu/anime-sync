drivepath="NutStore:Downloads/sync"

curl https://rclone.org/install.sh | sudo bash
rclone copy $drivepath/config.json .

pip3 install -r requirements.txt
python3 main.py

aria2c --seed-time=0 -d downloads -i dlist.txt
rm downloads/*.torrent
rclone copy downloads $drivepath
rclone copy config.json $drivepath
