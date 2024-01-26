# Bootstrap

Information on how I go about bootstrapping my lab.  This is the BIOS settings, OS install, and other things I do to get the lab up and running.

## OS

I took much of my inspiration for this setup from this [blog](https://www.jimangel.io/posts/automate-ubuntu-22-04-lts-bare-metal/).  Much credit to Jim Angel for his excellent work. Do read this blog before continuing. It will help.

I am using modern Ubuntu for this lab.  At this time I am using 22.04.  I want to use a UEFI boot from a USB stick that will pull a cloud-init user-data file from a known HTTP location for a given host so that I can have a unique user-data file for each host.  Because I could not find many ways to dynamically pass some unique value like a machine id an HTTP path in the kernel parameters (except to edit the kernel line in grub, but I want a fully automated install) I created a USB stick for each server, each with a slightly different `ks=http://ip/paht/` so I can simply hold the user-data in different folders on the web server.

The key to this is the autoinstall kernel parameters set in the /cd/boot/grub/grub.cfg file.  We want to change this:

```
linux   /casper/vmlinuz ---
```

to something like this (the ip changes depending on where you host the user-data file):

```
linux   /casper/vmlinuz autoinstall "ds=nocloud;s=http://10.0.0.115:8080/machine1/" ipv6.disable=1 ---
```

This has a few changes.  

- `autoinstall`: This tells the installer that we are doing an autoinstall.  The user-data file will give it more info when it starts.
- `ds=nocloud`: This tells the installer that we are using the [nocloud](https://cloudinit.readthedocs.io/en/latest/reference/datasources/nocloud.html) data source for cloud-init.
- `s=[http://](http://10.0.0.115:8080/machine1/)`: This is the location on the network to fetch the user-data file.  It will append `meta-data` and `user-data` to the end of the path.  In my case I only use user-data.   I also want to be able to tell the requests from each machine apart so this is where I add the machine id.  I am hard coding the machine id and creating a unique bootable usb per lab machine.  There is automation for this and a extra USB stick costs about $3.00.
- `ipv6.disable=1`: This is not required, but when I leave it on during the install the logs fill up with some errors.  I found this switch on the internet and it prevents the noise.

## BIOS

I choose to use UEFI therefore I disable CSM stands for Compatibility Support Module.  I used to use BIOS / PXE, however this is a huge pain in the butt.

Each hardware type has its own settings.  

### Gigabyte

### Kangaroo

### Rasberry Pi

