# Lab OpenStack Install Process

## Basic Host Setup

From the jumpbox as the `lab` user.

```shell
cd ~/openstack_lab
ansible-galaxy install -r requirements.yml -p roles
cd ~/openstack_lab/playbooks
ansible-playbook target-host-prep.yml

# Use the configs from the lab repo for OSA
cp ../configs/*.yml /etc/openstack_deploy/

# Blow away any old inventory files and facts
rm -rf /etc/openstack_deploy/ansible_facts/*
rm /etc/openstack_deploy/openstack_inventory.json
rm /etc/openstack_deploy/openstack_hostnames_ips.yml
rm /etc/openstack_deploy/backup_openstack_inventory.tar

# Generate the secrets config file
cd /opt/openstack-ansible/scripts
python pw-token-gen.py --file /etc/openstack_deploy/user_secrets.yml
```

## OpenStack Install

From the jumpbox as the `lab` user.

```shell
# Run the OSA playbooks that apply to us
cd /opt/openstack-ansible/playbooks

# Get our hosts and containers ready
openstack-ansible setup-hosts.yml
openstack-ansible setup-infrastructure.yml

# Install a limited set of OpenStack services
openstack-ansible os-keystone-install.yml
openstack-ansible os-glance-install.yml
openstack-ansible os-nova-install.yml

# I saw issues with losing connectivity to the neutron server containers
# during the first run, However re-running the playbook got it to complete.
openstack-ansible os-neutron-install.yml

# Horizon is definitely optional
openstack-ansible os-horizon-install.yml
```

## OpenVSwitch Manual work

### Neutron Agents

On each `neutron-agents-container` as `root` user.

```shell
# Setup the OVS bridge to our provider network
# eth12 is the container interface linked to the
# br-vlan on the physical host
ovs-vsctl add-br br-provider
ovs-vsctl add-port br-provider eth12

# Bounce the agent
service neutron-openvswitch-agent restart
```

### Compute hosts

On each compute host as `root` user.

```shell
# Setup the OVS bridge to our provider network
# eth0 is the physical host network interface
# that will provide link to the provider network VLAN
ovs-vsctl add-br br-provider
ovs-vsctl add-port br-provider br-vlan

# Bounce the agent
service neutron-openvswitch-agent restart
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