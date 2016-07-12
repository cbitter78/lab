# How to patch OSA

This assumes that you've cloned OSA master to `/opt/openstack-ansible`
and run `scripts/bootstrap-ansible.sh` already.

## OVS DVR Patch for Inventory groups

Review https://review.openstack.org/#/c/338546/

The url below is taken from the Patch-File download option in the
upper right corner of the Gerrit UI.

```shell
sudo su -
cd /opt/openstack-ansible
wget -O patch.zip https://review.openstack.org/changes/338546/revisions/7b5a742f2b3b8f16ce83c8401c4daaea2a45448c/patch?zip
unzip patch.zip
patch -p1 < 7b5a742f.diff
```

## OVS DVR Patch for Neutron role

Review https://review.openstack.org/#/c/338541/

The url below is taken from the Patch-File download option in the
upper right corner of the Gerrit UI.

```shell
sudo su -
cd /etc/ansible/roles/os_neutron
wget -O patch.zip https://review.openstack.org/changes/338541/revisions/a0cd4ac98a64797a0eeea8772cf9d73b579f6816/patch?zip
unzip patch.zip
patch -p1 < a0cd4ac9.diff
```
