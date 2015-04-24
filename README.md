<img src="http://www.elao.com/images/corpo/logo_red_small.png"/>

# Ansible Role: Supervisor

This role will assume the setup ofSupervisor

It's part of the ELAO [Ansible stack](http://ansible.elao.com) but can be used as a stand alone component.

## Requirements

- Ansible 1.7.2+

## Dependencies

- Pip

## Installation

Using ansible galaxy:

```bash
ansible-galaxy install elao.supervisor
```
You can add this role as a dependency for other roles by adding the role to the meta/main.yml file of your own role:

```yaml
dependencies:
  - { role: elao.supervisor }
```

## Role Handlers

|Name|Type|Description|
|----|----|-----------|
|supervisor restart|Service|Restart supervisor service

## Role Variables

|Name|Default|Type|Description|
|----|-------|----|-----------|
|elao_supervisor_config|{}|Array|Config
|elao_supervisor_configs|[]|Array|Configs

### Configuration example

```yaml
elao_supervisor_config:
  loglevel: info
```

Enable http server

```yaml
elao_supervisor_configs:
  - file:     inet_http_server.conf
    template: configs/inet_http_server_default.conf.j2
    config:
      port:     "*:9001"
```

Program

```yaml
elao_supervisor_configs:
  - file:     foo.conf
    template: configs/program_default.conf.j2
    config:
      name: foo
      command: "bar"
```

## Example playbook

    - hosts: servers
      roles:
         - { role: elao.supervisor }

# Licence

MIT

# Author information

ELAO [**(http://www.elao.com/)**](http://www.elao.com)
