## Deployment notes

The containerized deployment is pretty easy, here's the command:

`$ python-tdd-book % ansible-playbook --user=ubuntu --private-key ~/.ssh/superlists_keys.pem -i <host_name>, infra/deploy-playbook.yaml -v `