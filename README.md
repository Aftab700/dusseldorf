# dusseldorf

Dusseldorf is an out-of-band security tool to help in security research.

Fork of https://github.com/microsoft/dusseldorf.git

## Installation

Install Python-3.12.9:

```sh
sudo apt update
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
sudo apt-get install pkg-config
wget https://www.python.org/ftp/python/3.12.9/Python-3.12.9.tgz
tar -xvf Python-3.12.9.tgz
cd Python-3.12.9
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall
cd ..
python3.12 --version
```

Remove the downloaded Python source code:

```sh
rm -rf Python-3.12.9
rm -rf Python-3.12.9.tgz
```

Create a virtual environment:
```sh
python3.12 -m venv venv

source venv/bin/activate
```

Build zentralbibliothek library:

```sh
pip install --upgrade pip
cd zentralbibliothek/
bash build.sh
cd ..
```

Installing requirements:
```sh
pip install -r requirements.txt --only-binary :all:
```


Install MongoDB:
```sh
sudo apt-get install gnupg curl
curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg \
   --dearmor
echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] http://repo.mongodb.org/apt/debian bookworm/mongodb-org/8.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
sudo apt-get update
sudo apt-get install mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
sudo systemctl status mongod
```

Set up MongoDB database:
```sh
mongosh < env/mongo-scripts/init.js
```

Setup the admin user & password using [api/src/api/manage_users.py](api/src/api/manage_users.py) file. Use `python api/src/api/manage_users.py -h` for help.
```sh
python api/src/api/manage_users.py upsert -u admin -p your_super_secret_passwd -r admin owner -n Admin
```

Setup domain and ip:
```sh
python env/mongo-scripts/mongo-database.py --domain aftabsama.com --delete --ips 69.53.13.44
```

Setting up systemd services:
```sh
cd service/
bash setup-systemd-service.sh
```

> Note: update the dusseldorf path in the `*.service` files to match your installation directory.
