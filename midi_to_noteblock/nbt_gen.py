from .audio_splitter import split_midi
from .region import Region
from .block import Block

air = Block.create('minecraft:air')
repeater = Block.create('minecraft:repeater')
ticked_repeater = Block.create('minecraft:repeater[delay=4]')
white_concrete = Block.create('minecraft:white_concrete')
redstone = Block.create('minecraft:redstone_wire')
observer_down = Block.create('minecraft:observer[facing=down]')
powered_rail = Block.create('minecraft:powered_rail[shape=east_west]')
redstone_block = Block.create('minecraft:redstone_block')
redstone_lamp = Block.create('minecraft:redstone_lamp')
sticky_piston = Block.create('minecraft:sticky_piston[facing=south]')
lever = Block.create('minecraft:lever[face=floor]')

instrument_blocks = (
    Block.create('minecraft:oak_planks'),
    Block.create('minecraft:white_wool'),
    Block.create('minecraft:dirt'),
    Block.create('minecraft:clay'),
    Block.create('minecraft:gold_block')
)


def create_platforms(reg):
    for x in reg.xrange():
        for z in reg.zrange():
            reg.setblock(x, 0, z, white_concrete)
            reg.setblock(x, 6, z, white_concrete)


def create_repeater(reg, width, start=0):
    first = (start + 5) % 2
    for z in reg.zrange():
        if z >= 5:
            if z % 2 == first:
                reg.setblock(width+1, 1, z, repeater)
                reg.setblock(width-1, 1, z, repeater)
            else:
                reg.setblock(width+1, 1, z, redstone_lamp)
                reg.setblock(width-1, 1, z, redstone_lamp)


def create_firstlayer(reg, width, start=0):
    first = (start + 5) % 2
    for z in reg.zrange():
        if z >= start + 5:
            if z % 2 != first:
                reg.setblock(width+1, 2, z, observer_down)
            else:
                reg.setblock(width-1, 2, z, observer_down)


def create_toplayer(reg, start=0):
    for z in reg.zrange():
        if z < start + 5:
            continue
        for x in reg.xrange():
            reg.setblock(x, 3, z, white_concrete)
            reg.setblock(x, 4, z, powered_rail)
            reg.setblock(x, 5, z, observer_down)


def create_redstonelamps(reg, width, start=0):
    for z in reg.zrange():
        if z >= start + 5:
            reg.setblock(width, 7, z, redstone_lamp)


def create_layers(reg, width, start=0):
    create_platforms(reg)
    create_repeater(reg, width, start)
    create_firstlayer(reg, width, start)
    create_toplayer(reg, start)
    create_redstonelamps(reg, width, start)


def create_start(reg, width, start=0):
    reg.setblock(width, 7, start, lever)

    create_staircase(reg, width, start)
    create_nonpiston_connection(reg, width, start)
    create_piston_connection(reg, width, start)


def create_staircase(reg, width, start=0):
    # first block
    reg.setblock(width, 5, start+0, redstone)
    reg.setblock(width, 4, start+0, white_concrete)

    # second block
    reg.setblock(width, 4, start+1, redstone)
    reg.setblock(width, 3, start+1, white_concrete)

    # third block
    reg.setblock(width+1, 3, start+1, redstone)
    reg.setblock(width+1, 2, start+1, white_concrete)

    # forth block
    reg.setblock(width+1, 2, start+0, redstone)
    reg.setblock(width+1, 1, start+0, white_concrete)


def create_nonpiston_connection(reg, width, start=0):
    # One game tick repeater
    reg.setblock(width+1, 1, start+1, repeater)

    # Connection to noteblock repeaters
    reg.setblock(width+1, 1, start+2, redstone)
    reg.setblock(width+1, 1, start+3, redstone)
    reg.setblock(width+1, 1, start+4, redstone)


def create_piston_connection(reg, width, start=0):
    # Connection to the right side
    reg.setblock(width, 1, start+0, redstone)
    reg.setblock(width-1, 1, start+0, redstone)
    reg.setblock(width-2, 1, start+0, redstone)

    # Connection to Piston with block
    reg.setblock(width-2, 1, start+1, white_concrete)
    reg.setblock(width-2, 2, start+1, redstone)

    # Piston and block
    reg.setblock(width-2, 2, start+2, sticky_piston)
    reg.setblock(width-2, 2, start+3, white_concrete)

    # Redstone block and redstone wire under piston block
    reg.setblock(width-2, 1, start+3, redstone)
    reg.setblock(width-2, 0, start+3, redstone_block)

    # Connection to noteblock repeaters
    reg.setblock(width-1, 1, start+3, white_concrete)
    reg.setblock(width-1, 2, start+3, redstone)
    reg.setblock(width-1, 1, start+4, redstone)


def time_to_coord(time):
    return round(time * 30)


def create_note_block(reg, width, note, instrument_block, start):
    vel_pos = width - round((note.velocity * width) / 128)
    coord = time_to_coord(note.start) + start + 5
    note_block = Block.create(
        f'minecraft:note_block[note={str(note.pitch - 54)}]')

    if vel_pos > width / 2:
        vel_add = -1
    else:
        vel_add = 1

    while True:
        if vel_pos <= 0 or vel_pos > width:
            break
        if reg.getblock(width + vel_pos, 7, coord) == air:
            reg.setblock(width + vel_pos, 7, coord, note_block)
            reg.setblock(width + vel_pos, 6, coord, instrument_block)
            break
        elif reg.getblock(width - vel_pos, 7, coord) == air:
            reg.setblock(width - vel_pos, 7, coord, note_block)
            reg.setblock(width - vel_pos, 6, coord, instrument_block)
            break
        vel_pos += vel_add


def create_note_blocks(reg, width, audio_file, start=0):
    for i, instrument in enumerate(audio_file.instruments):
        for note in instrument.notes:
            create_note_block(reg, width, note, instrument_blocks[i], start)


def generate_schematic(midi_path, target_path, width=7, start=5):
    audio_file = split_midi(midi_path)

    reg = Region(width*2+1, 8, time_to_coord(audio_file.get_end_time() + 1))

    create_layers(reg, width, start)
    create_start(reg, width, start)
    create_note_blocks(reg, width, audio_file, start)

    nbt_file = reg.as_nbt()
    nbt_file.write_file(target_path)

    print(f"Generated File at {target_path}")
