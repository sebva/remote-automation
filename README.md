# Remote automation files

Collection of [Fabric](http://www.fabfile.org/) scripts for easy initial configuration of freshly provisioned machines.
Intended for my personal use.

## Install dependencies

```bash
virtualenv -p /usr/bin/python2.7 .venv
pip install -r requirements.txt
```

## Usage

**Activate _virtualenv_**
```bash
. ./.venv/bin/activate
```

**Example:** Use _zsh_ as the default shell with my custom `.zshrc` on machines eiger-1.maas and eiger-2.maas in parallel:

```bash
fab -P -H "eiger-1.maas,eiger-2.maas" zsh
```
