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

## License

> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
>
> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.
>
> You should have received a copy of the GNU General Public License
> along with this program.  If not, see <http://www.gnu.org/licenses/>.
