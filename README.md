# My Openstack Lab

This lab is for my personal use.  


# Hardware

see [hardware.md](hardware.md)


# Network


![image](lab.png)


You can access the swithc with
```
telnet 10.0.0.150

```

You can also connect to the web interface by connecting to the lab with a ssh prot fordwarding to 10.0.0.150:80

If you dont knwo the user and password then your out of luck.  ;)


## DHCP


DHCP is managed by systemctl

```
systemctl stop    isc-dhcp-server
systemctl start   isc-dhcp-server
systemctl status  isc-dhcp-server
systemctl restart isc-dhcp-server
```

There are Host directives in /etc/dhcp/dhcpd.conf that reserve an IP for each host in the lab.

This is the cureent configureation:

```
option domain-name "bitter.net";
option domain-name-servers 8.8.8.8, 4.4.4.4;
default-lease-time 600;
max-lease-time 7200;
log-facility local7;
ddns-update-style none;

host control1.bitter.net {
  hardware ethernet fc:aa:14:dc:95:d7;
  fixed-address 192.168.1.20;
        supersede host-name = "control2.bitter.net";
}
host control2.bitter.net {
  hardware ethernet fc:aa:14:dd:67:ee;
  fixed-address 192.168.1.21;
        supersede host-name = "control2.bitter.net";
}
host control3.bitter.net {
  hardware ethernet fc:aa:14:dc:94:aa;
  fixed-address 192.168.1.22;
        supersede host-name = "control3.bitter.net";
}

host compute1.bitter.net {
  hardware ethernet fc:aa:14:df:a8:32;
  fixed-address 192.168.1.23;
        supersede host-name = "compute2.bitter.net";
}
host compute2.bitter.net {
  hardware ethernet fc:aa:14:df:a7:c7;
  fixed-address 192.168.1.24;
        supersede host-name = "compute2.bitter.net";
}

subnet 192.168.1.0 netmask 255.255.255.0{
        range 192.168.1.30 192.168.1.39;
        option routers 192.168.1.1;
        server-identifier 192.168.1.1;
        next-server 192.168.1.1;
        filename "pxelinux.0";
}

```

### PXE Booting 

I am using [PXEMonster](https://github.com/cbitter78/pxemonster) to create pxelinux.cfg files uing the ip address.  Post build the kick start will call pxemonister to remove the pxelinux.cfg file so on next boot it wont rebuild but will boot from local disk. 


To rebuild a host you use these commands (these will create a pxelinux file for 192.168.1.20 which should be control1.bitter.net.  Change the ip or passed in to define a differnt host)

```
curl -X POST "http://192.168.1.1:8080/pxe?spoof=192.168.1.20

```


```
/home/lab/pxelinux.cfg/prep_for_rebuild.sh 20
```
After you have run this script you will see a file prefixed with C0A8011 in /home/lab/pxelinux.cfg folder.   Jsut reboot the host and it will rebuld.

#### PXEMonster


PXE Monister is a docker container.  To see if its running you can 

```
docker ps

```

To restart it you can 

```
service docker restart
docker run -ti -d -p 192.168.1.1:8080:80 -v /var/lib/tftpboot/pxelinux.cfg:/pxelinux.cfg cbitter78/pxemonister:0.0.3-0

```

This is the /var/lib/tftpboot/pxemonster.yml file

```
---
- ip: 192.168.1.20
  pxe_template: ubuntu_1404.erb
  kickstart_url: http://192.168.1.1/ubuntu_14_04/ubuntu.ks
- ip: 192.168.1.21
  pxe_template: ubuntu_1404.erb
  kickstart_url: http://192.168.1.1/ubuntu_14_04/ubuntu.ks
- ip: 192.168.1.22
  pxe_template: ubuntu_1404.erb
  kickstart_url: http://192.168.1.1/ubuntu_14_04/ubuntu.ks
- ip: 192.168.1.23
  pxe_template: ubuntu_1404.erb
  kickstart_url: http://192.168.1.1/ubuntu_14_04/ubuntu.ks
- ip: 192.168.1.24
  pxe_template: ubuntu_1404.erb
  kickstart_url: http://192.168.1.1/ubuntu_14_04/ubuntu.ks

```

The ubuntu_1404.erb looks like this

```
default ubuntu1404

label ubuntu1404
  kernel ubuntu1404/linux
  append initrd=ubuntu1404/initrd.gz ks=<%= @host_info['kickstart_url'] %>
  prompt 0
  timeout 0

```
