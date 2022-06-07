import os
import argparse
from midi_to_noteblock import generate_schematic

home_dir = os.path.expanduser("~")
default_schem_dir = os.path.join(
    home_dir, ".minecraft/config/worldedit/schematics")

parser = argparse.ArgumentParser(
    description="Generate a schematic from a MIDI file")
parser.add_argument("midi_file", help="The MIDI file to convert")
parser.add_argument("-s", "--schematic-file",
                    help="The name of the schematic to create", required=False)
parser.add_argument("-d", "--schematic-dir",
                    help="The directory to save the schematic to", default=default_schem_dir)


def main():
    args = parser.parse_args()
    midi_file = args.midi_file
    schematic_filename = args.schematic_file
    schematic_dir = args.schematic_dir

    if not os.path.exists(schematic_dir):
        os.makedirs(schematic_dir)

    if not schematic_filename:
        schematic_filename = os.path.basename(midi_file)
        schematic_filename = os.path.splitext(schematic_filename)[0] + ".schem"

    target_path = os.path.join(schematic_dir, schematic_filename)
    generate_schematic(midi_file, target_path)


if __name__ == "__main__":
    main()
