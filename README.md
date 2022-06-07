# Midi File to Minecraft Schematic

[![PyPI](https://shields.io/pypi/v/midi-to-noteblock?style=flat-square)](https://pypi.org/project/midi-to-noteblock/)
[![PyPI Wheel](https://shields.io/pypi/wheel/midi-to-noteblock?style=flat-square)](https://pypi.org/project/midi-to-noteblock/)
[![License](https://shields.io/pypi/l/midi-to-noteblock?style=flat-square)](https://github.com/SushiWaUmai/midi-to-noteblock/blob/main/LICENSE)

A CLI to convert midi files into world edit schematic files. 

## How to use
Install the CLI via [pip](https://pypi.org/project/midi-to-noteblock/)
```bash
pip install midi-to-noteblock
```

Then run the CLI with the following command:
```bash
midi-to-noteblock example.mid # the midi file to convert
```

Available Options:
```
usage: midi-to-noteblock [-h] [-s SCHEMATIC_FILE] [-d SCHEMATIC_DIR] midi_file

Generate a schematic from a MIDI file

positional arguments:
  midi_file             The MIDI file to convert

options:
  -h, --help            show this help message and exit
  -s SCHEMATIC_FILE, --schematic-file SCHEMATIC_FILE
                        The name of the schematic to create
  -d SCHEMATIC_DIR, --schematic-dir SCHEMATIC_DIR
                        The directory to save the schematic to

```

## Development
Clone the repo
```bash
git clone https://github.com/SushiWaUmai/midi-to-schematic.git
cd ./midi-to-schematic
```

Install all dependencies and run the python script
```bash
# use pip3 and python3 respectively
pip install -r requirements.txt

# Use -h for the help menu
python main.py -h
```

## License
This project is licensed under the [MIT license](https://github.com/SushiWaUmai/midi-to-noteblock/blob/main/LICENSE)
