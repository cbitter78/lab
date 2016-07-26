# Lab OpenStack Install Process

## Basic Host Setup

From the jumpbox

### Remove a older openstack-ansible config

As root

```shell

mv /opt/openstack-ansible /opt/openstack-ansible_`date +%Y-%m-%d`
git clone -b master https://github.com/openstack/openstack-ansible.git /opt/openstack-ansible
cd /opt/openstack-ansible
scripts/bootstrap-ansible.sh
chown -R lab:lab /opt/openstack-ansible
chown -R lab:lab /etc/ansible


# Blow away any old inventory files and facts
rm -rf /etc/openstack_deploy/ansible_facts/*
rm /etc/openstack_deploy/openstack_inventory.json
rm /etc/openstack_deploy/openstack_hostnames_ips.yml
rm /etc/openstack_deploy/backup_openstack_inventory.tar

```

See [DVR_PATCH](DVR_PATCH.md) if you need to patch OSA

As the `lab` user

```shell

# Copy custom playbooks into ansible playbook folder
cp ~/openstack_lab/playbooks/custom_plays/* /opt/openstack-ansible/playbooks/

cd ~/openstack_lab
ansible-galaxy install -r requirements.yml -p roles
cd ~/openstack_lab/playbooks
ansible-playbook target-host-prep.yml

# Use the configs from the lab repo for OSA
cp ~/openstack_lab/configs/*.yml /etc/openstack_deploy/

# Generate the secrets config file
cd /opt/openstack-ansible/scripts
python pw-token-gen.py --file /etc/openstack_deploy/user_secrets.yml
```

## OpenStack Install

From the jumpbox as the `lab` user.

```shell
# Run the OSA playbooks that apply to us
cd /opt/openstack-ansible/playbooks
openstack-ansible setup-lab.yml

```


## OpenStack bootstrapping

On any `utility-container` as `root` user.

### Network setup

```shell
cd /root
source openrc

# Create the provider network
neutron net-create physnet1 --shared \
  --provider:physical_network physnet1 \
  --provider:network_type vlan \
  --provider:segmentation_id 101

# Create the subnet for the provider net
neutron subnet-create physnet1 192.168.2.0/24 \
  --name physnet-subnet \
  --gateway 192.168.2.1
```

### OpenStack setup for testing

```shell
cd /root
source openrc

# Create a nano flavor so we don't tax the lab resources
openstack flavor create --id 0 --vcpus 1 --ram 64 --disk 1 m1.nano

# Create a demo tenant/project
openstack project create \
  --domain default \
  --description "Demo Project" demo

openstack user create \
  --domain default \
  --password demo demo

openstack role create user

openstack role add \
  --project demo \
  --user demo user

# Create an openrc for our demo tenant
cp openrc demo-openrc
```

Edit `demo-openrc` to adjust username, project and password.
You want to ensure you have the following content in the file:

```shell
export OS_USERNAME=demo
export OS_PASSWORD=demo
export OS_PROJECT_NAME=demo
export OS_TENANT_NAME=demo
```

```shell
cd /root
# Create an ssh key for the demo tenancy
ssh-keygen -q -N ""

# Add the key to the demo tenancy
source demo-openrc
openstack keypair create --public-key ~/.ssh/id_rsa.pub mykey

# Give ourselves some access to instances in the demo tenancy
openstack security group rule create \
  --proto icmp default
openstack security group rule create \
  --proto tcp --dst-port 22 default

# Grab the cirros image
wget http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img

# we need to be admin to upload the image
source openrc

# Upload the cirros image to Glance
openstack image create "cirros" \
  --file cirros-0.3.4-x86_64-disk.img \
  --disk-format qcow2 \
  --container-format bare \
  --public
```

## Test an instance launch

On any `utility-container` as `root` user.

```shell
cd /root
# Use the demo tenancy
source demo-openrc

# Validate that we can see the network and image
openstack image list
openstack network list

# Launch our damn instance already
openstack server create \
  --flavor m1.nano \
  --image cirros \
  --security-group default \
  --key-name mykey provider-instance
```