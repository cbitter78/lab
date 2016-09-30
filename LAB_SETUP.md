# Lab OpenStack Install Process

## Basic Host Setup

From the jumpbox

### Remove a older openstack-ansible config

As root

```shell

mv /opt/openstack-ansible /opt/openstack-ansible_`date +%Y-%m-%d`
git clone -b master https://github.com/openstack/openstack-ansible.git /opt/openstack-ansible
cd /opt/openstack-ansible
ANSIBLE_ROLE_FETCH_MODE=git-clone scripts/bootstrap-ansible.sh
chown -R lab:lab /opt/openstack-ansible
chown -R lab:lab /etc/ansible


# Blow away any old inventory files and facts
rm -rf /etc/openstack_deploy/ansible_facts/*
rm /etc/openstack_deploy/openstack_inventory.json
rm /etc/openstack_deploy/openstack_hostnames_ips.yml
rm /etc/openstack_deploy/backup_openstack_inventory.tar
rm -rf /etc/openstack_deploy/env.d/*

```

As the `lab` user

```shell

# Copy custom playbooks into ansible playbook folder
cp ~/openstack_lab/playbooks/custom_plays/* /opt/openstack-ansible/playbooks/

cd ~/openstack_lab
ansible-galaxy install -r requirements.yml -p roles
cd ~/openstack_lab/playbooks
ansible-playbook target-host-prep.yml

# Use the configs from the lab repo for OSA
cp ~/openstack_lab/etc/openstack_deploy/*.yml /etc/openstack_deploy/
cp ~/openstack_lab/etc/openstack_deploy/env.d/*.yml /etc/openstack_deploy/env.d/

# Generate the secrets config file
cd /opt/openstack-ansible/scripts
python pw-token-gen.py --file /etc/openstack_deploy/user_secrets.yml
```

## OpenStack Install

From the jumpbox as the `lab` user.

```shell
cd /opt/openstack-ansible/playbooks
openstack-ansible setup-hosts.yml
openstack-ansible setup-infrastructure.yml
# create the telemetry-specific RabbitMQ cluster
openstack-ansible -e "rabbitmq_host_group=telemetry_rabbitmq_all" rabbitmq-install.yml
openstack-ansible os-keystone-install.yml
openstack-ansible os-glance-install.yml
openstack-ansible os-nova-install.yml
openstack-ansible os-neutron-install.yml
openstack-ansible os-heat-install.yml
openstack-ansible mongodb-install.yml
openstack-ansible os-ceilometer-install.yml
openstack-ansible ovs-setup.yml
```

## OpenStack bootstrapping

The playbook below is not idempotent, so only run it once.

```shell
cd /opt/openstack-ansible/playbooks
openstack-ansible bootstrap_region.yml -vvv
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