# YangonIndex

##Dependencies
```sh
pip install flask, requests, MySQL-python
```

##AWS setup,   
(1) Provision a Amazon Linux AMI.  
(2) Install [LAMP](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-LAMP.html)  
(3) Install WSGI.  
```sh
$ sudo yum install mod24_wsgi-python27.x86_64
```
(4) Setup SSL with [CertBot](https://certbot.eff.org).  
(5) Add [users](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/managing-users.html) and add to **wheel** group.  
(6) Add user to wheel.  
```sh
$ sudo usermod -aG wheel {userName}
```
(7) Change /etc/sudoers to allow people in wheel to run all commands without password by uncommenting the following line.  
```sh
%wheel  ALL=(ALL)       NOPASSWD: ALL
```
  
##Logging into AWS  
```sh
ssh -i {path/to/privateKey} {userName}@yangonindex.com
```
or  
```sh
ssh -i {path/to/privateKey} {userName}@52.74.138.31
```

The apache document root for yangonindex is /var/www/vhost/yangonindex.  