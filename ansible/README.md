# Ansible

I used these playbooks to configure my lab.  Make sure to create a venv and install the requirements.

```shell
python3.12 -m venv venv 
source venv/bin/activate
pip --isolated install --upgrade pip
pip --isolated install -r requirements.txt'
source ./venv/bin/activate
ansible-galaxy install -r requirements.yml
```

## livefs-editor

```shell
source ./venv/bin/activate
ansible-playbook -i ./inventory/ ./playbooks/livefs-editor.yaml --extra-vars "target=your_host.local"
```

## boot-server

```shell
source ./venv/bin/activate
ansible-playbook -i ./inventory/ ./playbooks/boot-server.yaml --extra-vars "target=your_host.local"
```
