#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict
import json
import re
import shlex
import sys


cores = defaultdict(lambda: {"name": ""})
mras = list()

computers = set([
    'Amstrad',
    'ao486',
    'Apogee',
    'Apple-II',
    'Apple-I',
    'Archie',
    'Atari800',
    'AtariST',
    'BBCMicro',
    'BK0011M',
    'C16',
    'C64',
    'EDSAC',
    'Galaksija',
    'Jupiter',
    'MacPlus',
    'Minimig',
    'MSX',
    'MultiComp',
    'ORAO',
    'Oric',
    'PDP1',
    'PET2001',
    'QL',
    'SAMCoupe',
    'SharpMZ',
    'Specialist',
    'Ti994a',
    'TRS-80',
    'TSConf',
    'Vector-06C',
    'VIC20',
    'X68000',
    'ZX81',
])

consoles = set([
    'Astrocade',
    'Atari2600',
    'Atari5200',
    'AY-3-8500',
    'ColecoVision',
    'Gameboy',
    'GBA',
    'Genesis',
    'MegaCD',
    'NeoGeo',
    'NES',
    'Odyssey2',
    'SMS',
    'SNES',
    'TurboGrafx16',
    'Vectrex',
])

arcades = set([
    'SkySkipper',
])

others = set([
    'Arduboy',
    'Chip8',
    'FlappyBird',
    'GameOfLife',
])

utils = set([
    'memtest',
    'menu',
])


def decide_location(data):
    if data["extra"].get("type", None) == "Arcade" or data["extra"]["name"] in arcades:
        return f"_Arcade/cores/{data['extra']['name']}_{data['extra']['date']}.rbf"
    elif data["extra"]["name"] in computers:
        return f"_Computer/{data['name']}"
    elif data["extra"]["name"] in consoles:
        return f"_Console/{data['name']}"
    elif data["extra"]["name"] in utils:
        return f"_Utils/{data['name']}"
    else:
        return f"_Others/{data['name']}"



exprs = list(map(re.compile, [
    r'^(?P<type>Arcade)-(?P<name>[^_]+)_(?P<date>\d{8}[a-z]?).rbf$',
    r'^(?P<name>[^_]+)_(?P<date>\d{8}[a-z]?).rbf$'
]))


if __name__ == '__main__':
    for line in sys.stdin:
        data=json.loads(line)
        if data["type"] == "RBF":
            for e in exprs:
                if (m := e.match(data['name'])) is not None:
                    data["extra"] = m.groupdict()
                    cores[m.group("name")] = max(cores[m.group("name")], data, key=lambda x: x["name"])
                    break
            else:
                print("Not matched", data["name"], file=sys.stderr)
        elif data["type"] == "MRA":
            mras.append(data)


    print("insecure")
    print("create-dirs")
    for k, v in cores.items():
        print(f"""
# {k}
url = "{v["url"]}"
output = "{decide_location(v)}"
""")

    for m in mras:
        print(f"""
# {m['name']}
url = "{m['url']}"
output = "_Arcade/{m['name']}"
""")
