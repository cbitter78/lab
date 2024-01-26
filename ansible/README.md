# Ansible

I used these playbooks to configure my lab.  Make sure to create a venv and install the requirements.

```shell
python3.12 -m venv venv 
source venv/bin/activate
pip --isolated install --upgrade pip
pip --isolated install -r requirements.txt'
source ./venv/bin/activate
```


## Usage

```shell
source ./venv/bin/activate
ansible-playbook -i ./inventory.yml ./playbooks/livefs-editor.yaml --extra-vars "target=giga1.local"
```