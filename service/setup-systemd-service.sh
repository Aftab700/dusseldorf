sudo cp dusseldorf-*.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable dusseldorf-api-server.service
sudo systemctl enable dusseldorf-http-server.service
sudo systemctl enable dusseldorf-https-server.service
sudo systemctl enable dusseldorf-dns-tcp-server.service
sudo systemctl enable dusseldorf-dns-udp-server.service
sudo systemctl enable dusseldorf-smtp-server.service

sudo systemctl start dusseldorf-api-server.service
sudo systemctl start dusseldorf-http-server.service
sudo systemctl start dusseldorf-https-server.service
sudo systemctl start dusseldorf-dns-tcp-server.service
sudo systemctl start dusseldorf-dns-udp-server.service
sudo systemctl start dusseldorf-smtp-server.service

sleep 5

sudo systemctl status dusseldorf-api-server.service
sudo systemctl status dusseldorf-http-server.service
sudo systemctl status dusseldorf-https-server.service
sudo systemctl status dusseldorf-dns-tcp-server.service
sudo systemctl status dusseldorf-dns-udp-server.service
sudo systemctl status dusseldorf-smtp-server.service

# sudo journalctl -u dusseldorf-api-server.service

# Free Up Port 53
# sudo nano /etc/systemd/resolved.conf
# Disable the stub listener. Find the line #DNSStubListener=yes, uncomment it (remove the #), and change yes to no:
# DNSStubListener=no
# Update your /etc/resolv.conf. The stub resolver manages this file, so you need to point it to the correct upstream resolver configuration.
# sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
# Restart the systemd-resolved service to apply the changes:
# sudo systemctl restart systemd-resolved.service

# Update the vps policy to allow port 53,80,443
