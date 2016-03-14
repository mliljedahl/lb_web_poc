# lb_web_poc

Proof of concept for setting up a load balancer and any number of web nodes using Ansible and Vagrant.

To test the distribution of requests run: `python lbtest.py --requests 100`. Then one load balancer and tree web nodes will start and in this case 100 requests will be sent and a summary of the request distribution will be shown. It is possible to specify number of web nodes with `-n X` where X is any number between 1 and 239.

Since this kind of setup installs every machine almost from scratch it is very time consuming to develop and start the test so, be patient ;) To speed up things a little bit the setup uses the virtualbox image "precise32" which is older and faster image than for example trusty64.

## Requirements

* Virtualbox - [virtualbox.org](https://www.virtualbox.org/wiki/Linux_Downloads)
* Vagrant - [vagrantup.com](https://www.vagrantup.com/downloads.html)

## Usage

```
$ python lbtest.py -h
usage: lbtest.py [-h] [-n NODES] [-l LOADBALANCER] -r REQUESTS

Test how a load balancer is distributing client requests across a group of
servers.

optional arguments:
  -h, --help            show this help message and exit
  -n NODES, --nodes NODES
                        number web server nodes
  -l LOADBALANCER, --loadbalancer LOADBALANCER
                        load balancer ip address

required named arguments:
  -r REQUESTS, --requests REQUESTS
                        number of http requests
```