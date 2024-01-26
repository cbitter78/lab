apt-get update && apt-get install -y xorriso squashfs-tools python3-debian gpg liblz4-tool python3-pip git
cd
mkdir autoinstall
# put the iso here
# modify the grub.cfg to add the autoinstall option
git clone https://github.com/mwhudson/livefs-editor livefs-editor
pip install .
cd ..
livefs-edit ubuntu-22.04.3-live-server-amd64.iso ubuntu-22.04.3-live-server-amd64-mod.iso --cp ./grub.cfg new/iso/boot/grub/grub.cfg

lsblk # Find the usb device
 
export USB_DISK=/dev/????
dd bs=4M if=./ubuntu-22.04.3-live-server-amd64-mod.iso of=$USB_DISK conv=fdatasync status=progress

```shell



```