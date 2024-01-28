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
linux   /casper/vmlinuz autoinstall "ds=nocloud;s=http://10.0.0.254/machine1/" ipv6.disable=1 ---
```

This has a few changes.  

- `autoinstall`: This tells the installer that we are doing an autoinstall.  The user-data file will give it more info when it starts.
- `ds=nocloud`: This tells the installer that we are using the [nocloud](https://cloudinit.readthedocs.io/en/latest/reference/datasources/nocloud.html) data source for cloud-init.
- `s=[http://](http://10.0.0.254/machine1/)`: This is the location on the network to fetch the user-data file.  It will append `meta-data` and `user-data` to the end of the path.  In my case I only use user-data.   I also want to be able to tell the requests from each machine apart so this is where I add the machine id.  I am hard coding the machine id and creating a unique bootable usb per lab machine.  There is automation for this and a extra USB stick costs about $3.00.
- `ipv6.disable=1`: This is not required, but when I leave it on during the install the logs fill up with some errors.  I found this switch on the internet and it prevents the noise.

I used the [livefs-editor](./ansible/playbooks/livefs-editor.yaml) playbook sets up an ubuntu host to run [livefs-editor](https://github.com/mwhudson/livefs-editor) to modify the grub.conf on a ubuntu live cd to point to a URL with the name of a given machine in it.  This play will create a grub.conf for each machine, then after setting up to run livefs-editor will run it to create a unique iso for each machine. I then write each iso to its own USB stick / sd card and that lives in the given machine then, that unique USB stick is plugged into each machine and stays there.

To write the iso file to the USB drives I used this script

```shell
lsblk # Find the usb device
 
export USB_DISK=/dev/sdc
export ISO= ./ubuntu-<machine>.iso
dd bs=4M if=$ISO of=$USB_DISK conv=fdatasync status=progress
```

I also made sure I set up each host to ONLY use EFI not BIOS.  For the [Gigabyte](./README.md#node-type-1) hosts I had to disable CMS (Compatibility Support Module) and for the [kangaroo](./README.md#kangaroo) I had to set it to UEFI only.

With a bootable usb device per machine that each points to 10.0.0.254/machine I just need to set up a host to respond on that ip and serve the correct metadata for each machine.  The [](./ansible/playbooks/boot-server.yaml) playbook sets up apache and creates the user-data files needed. It also adds a [python utility](./ansible/playbooks/files/build_logs_server.py) that when run will listen on port 8088 (just a port I picked and defined in the user-data script) for the ubuntu install reporting logs.  This lets you watch the install logs from a central place.  Running build_logs_server.py to watching the logs is not required but its nice.

If you look at the [late-commands](./ansible/playbooks/templates/user-data.j2) in the user-data template you will see that it calls `efibootmgr` after the install is done.  It is looking for the USB device and removing it from the efi boot record so on the next boot it will not use that device.  This means you need to know what that device will look like on boot.  For me I just ran `efibootmgr` and found a unique string I could grep by.  Here is an example

```shell
$ efibootmgr

BootCurrent: 0000
Timeout: 1 seconds
BootOrder: 0000,0002,0004,0005,0006,0001,0003
Boot0000* ubuntu
Boot0001* Hard Drive
Boot0002* UEFI: IP4 Realtek PCIe GBE Family Controller
Boot0003  Network Card
Boot0004* ubuntu
Boot0005* UEFI OS
Boot0006* UEFI:  USB DISK 3.0 PMAP
```

In this case because I am using [MicroCenter USB drives](https://www.amazon.com/dp/B09YCXYVCL) in almost all the hosts (except the kangaroo where I use an SD card because it has a built in reader) they show up as `UEFI:  USB DISK 3.0 PMAP`.  I define this in the var files for the host that will serve the meta-data.  In my case its [giga1](./ansible/inventory/host_vars/giga1.local.json)

The first time I booted a host I had to hook up a keyboard, mouse, and monitor so that I could ensure we were using EFI boot was set and that I took note of the hard drive seral number I wanted the OS installed on so I could update the [boot_server_configs](./ansible/inventory/host_vars/giga1.local.json) so that the meta-data file could be customized for each machine.  After that I just needed to boot from the USB Disk and watch it go (or not).

To rebuild a host, I just need to log into it via ssh and use efibootmgr to tell it on next boot use the usb stick.  This is why I switched to all EFI because from the OS I can select the next boot.  This is done by listing the efiboot options with `efibootmgr` finding the boot number for the USB stick and running `efibootmgr -n Number` so in our case

```shell
$ efibootmgr

BootCurrent: 0000
Timeout: 1 seconds
BootOrder: 0000,0002,0004,0005,0006,0001,0003
Boot0000* ubuntu
Boot0001* Hard Drive
Boot0002* UEFI: IP4 Realtek PCIe GBE Family Controller
Boot0003  Network Card
Boot0004* ubuntu
Boot0005* UEFI OS
Boot0006* UEFI:  USB DISK 3.0 PMAP
```

I would run

```shell
efibootmgr -n 6 #We use the number after Boot000
reboot
```

This will rebuild the host completely unattended.


### Raspberry Pi
