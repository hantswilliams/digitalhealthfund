# digitalhealthfund.com website / built with Flask 

## technologies utilized: 
- Python: flask / python 3.6 / pyENV 
- NGINX 
- GUNICORN 

## to add in the near future: 
- automation with `ansible` -- to setup EC2 instance with docker, docker-compose, python 
- deployment with `docker` and `docker-compose` - containerize python (flask), nginx


## Instructions for modifying live website 
- Currently deployed on AWS - EC2 instance with Gunicorn + Nginx 
- To make changes to the existing app, go into app folder (SFTP), modify files, then perform 
	- `sudo pkill gunicorn` to stop the existing service 
	- `gunicorn app:app -b :8000 &` to re-run the app 
	- after this, go to digitalhealth.com and make sure things are back up and running 

## Original deployment: 
- Utilization of NGINX instructions:
	- `sudo apt-get update`
	- `sudo apt-get install -y nginx`
	- `sudo service nginx start`
- remove default file 
	- `sudo rm /etc/nginx/sites-enabled/default`
- create a new default file 
	- `sudo nano /etc/nginx/sites-available/digitalhealthfund.com`
- now lets add things to it, e.g., each of the local hosts will be specific flask apps running (gunicorn app:app -b :8000) (gunicorn app:app -b :80001) etc...

##############################################################################
## Setup with non-SSL (HTTP:)
##############################################################################


```
server {
        listen 80;
        server_name digitalhealthfund.com www.digitalhealthfund.com;
        location / {
                proxy_pass http://127.0.0.1:8000/;
        }
        location /app1 {
                proxy_pass http://127.0.0.1:8001/;
        }
        location /app2 {
                proxy_pass http://127.0.0.1:8002/;
        }
}
```

```
server {
        listen 80;
        server_name app.digitalhealthfund.com www.app.digitalhealthfund.com;
        location / {
                proxy_pass        http://127.0.0.1:8002/;
                proxy_set_header  Host             $http_host;
                proxy_set_header  X-Real-IP        $remote_addr;
                proxy_set_header  X-Forwarded-For  $proxy_add_x_forwarded_for;
        }
}
```


##############################################################################
## Setup with SSL (HTTPS:)
##############################################################################

- Followed this: https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04
	- `sudo add-apt-repository ppa:certbot/certbot`
	- `sudo apt install python-certbot-nginx`
- then restart the services 
	- `sudo nginx -t`
	- `sudo systemctl reload nginx`
	- `sudo ufw enable`
- This will give: Command may disrupt existing ssh connections. Proceed with operation (y|n)? - DO YES 
	- Firewall is active and enabled on system startup
	- for testing purposes, make it soo Nginx Full, OpenSSH, and the TCP22 ports are open; 
		- `sudo ufw status`
		- `sudo ufw allow 'Nginx Full'`
		- `sudo ufw allow ssh`
		- `sudo ufw allow OpenSSH`
- Then run this: 
	- `sudo certbot --nginx -d digitalhealthfund.com -d www.digitalhealthfund.com` 
- OR do this for manual if :80 is closed 
	- `sudo certbot -d digitalhealthfund.com -d www.digitalhealthfun.com --manual --preferred-challenges dns certonly`
- IMPORTANT NOTE FOR GODADDY/DNS FILE FOR SUB-DOMAINS IF YOU DO ANYTHING:  
	- note dont add in the domain to the dns record just do 
		- `host = _acme-challenge`
		- `host = _acme-challenge.www`
	- or for subdomain
		- `_acme-challenge.subdomainA`
		- `_acme-challenge.www.subdomainA`
- then add the redirects to force the http to go to https / the one below is generic and should work for all 
```
server {
        listen 80 default_server;
        server_name _;
        return 301 https://$host$request_uri;
}
```
	- `sudo nginx -t`
	- `sudo systemctl reload nginx`

- The keys are found in: 
	- `/etc/letsencrypt/live/cs-virtualhealth.com/fullchain.pem`
	- `/etc/letsencrypt/live/cs-virtualhealth.com/privkey.pem`



##############################################################################
## RENEWING CERTBOOK / SSL 
##############################################################################
- RENEWING SSL keys (HTTPS) when it is time to renew, if auto renewel is not setup: 
	- `sudo certbot renew --dry-run`




##############################################################################
## FINAL POTENTIAL NGINX FILE SETUP: 
##############################################################################

- So it should now look like this: 
```
server {
        server_name digitalhealthfund.com www.digitalhealthfund.com;
        location / {
                proxy_pass http://127.0.0.1:8000/;
        }
        location /app1 {
                proxy_pass http://127.0.0.1:8001/;
        }
        location /app2 {
                proxy_pass http://127.0.0.1:8002/;
        }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/digitalhealthfund.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/digitalhealthfund.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}
```

```
server {
    if ($host = www.digitalhealthfund.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    if ($host = digitalhealthfund.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

        listen 80;
        server_name digitalhealthfund.com www.digitalhealthfund.com;
    return 404; # managed by Certbot

}
```


##############################################################################
## Configuration of Subdomains and Running
##############################################################################

- NOTE, to get the SUBDOMAIN - app.digitalhealthfund.com working  will need to add that to the godaddy DNS - this means going to DNS service in godaddy, creating a new A record; then typ in the following fields: 
	- Type: A 
	- Name: app 
	- Value: the IP address of the ec2 instance 
	- TTL: 600 seconds 
- Then create symbolic link 
	- 1sudo ln -s /etc/nginx/sites-available/digitalhealthfund.com /etc/nginx/sites-enabled/digitalhealthfund.com`
- Next, restart NGINX services  
	- `sudo nginx -t`
	- `sudo service nginx restart`
- Finally, create the apps, each with their own virtual environment / create virtual environment
	- `pip install gunicorn`
- Again, to run the app:
	- `gunicorn app:app -b :8000 &`




