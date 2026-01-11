sudo apt update

# Install MongoDB Community Edition: https://www.mongodb.com/docs/manual/administration/install-on-linux/
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

# Set up MongoDB database
mongosh < env/mongo-scripts/init.js

# Install Python
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
sudo apt-get install pkg-config
wget https://www.python.org/ftp/python/3.12.9/Python-3.12.9.tgz
tar -xvf Python-3.12.9.tgz
cd Python-3.12.9
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall

python3.12 --version

cd ..
rm -rf Python-3.12.9
rm -rf Python-3.12.9.tgz

rm -rf ./venv/

python3.12 -m venv venv --copies # python3.12 -m venv venv

source venv/bin/activate

pip install --upgrade pip

echo Building zentralbibliothek/build.sh
cd zentralbibliothek/
bash build.sh

cd ..

echo Installing api requirements
pip install -r api/src/api/requirements.txt

echo Installing dns listener requirements
pip install -r listener.dns/src/requirements.txt

echo Installing http listener requirements
pip install -r listener.http/src/requirements.txt
