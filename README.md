Web page for OpenVPN user creation with Active Directory authorization

Based on Flask and pyOpenSSL

Steps to install:

1. Install additional packages on your server

```
apt install libsasl2-dev python-dev libldap2-dev libssl-dev
```

2. Install requirements

```
pip install -r requirements.txt
```

3. Fill app/config.py with your Active Directory credentials and needed certificate organization fields. Add path to your ca.crt and ca.key files

4. /app/static/certs/template.ovpn is template for your ovpn config files, fill it with your settings

