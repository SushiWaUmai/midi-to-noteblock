from nbt import nbt
from .block import Block


class Region:
    def __init__(self, width, height, length):
        self.width = width
        self.height = height
        self.length = length
        self.blocks = [0] * width * height * length

    def xrange(self):
        return range(self.width)

    def yrange(self):
        return range(self.height)

    def zrange(self):
        return range(self.length)

    def positionToIndex(self, x, y, z):
        # first x then z then y
        return x + z * self.width + y * self.width * self.length

    def setblock(self, x, y, z, block):
        self.blocks[self.positionToIndex(x, y, z)] = block.index

    def getblock(self, x, y, z):
        return Block.get(self.blocks[self.positionToIndex(x, y, z)])

    # PalleteMax TAG_Int
    # Pallete TAG_Compound
    #   Blockname TAG_Int index
    # Version TAG_Int
    # Length TAG_Short z
    # Width TAG_Short x
    # Height TAG_Short y
    # Metadata TAG_Compound
    # BlockData TAG_Byte_Array

    def as_nbt(self):
        nbt_file = nbt.NBTFile()
        nbt_file["Metadata"] = nbt.TAG_Compound()

        nbt_file["Width"] = nbt.TAG_Short(self.width)
        nbt_file["Height"] = nbt.TAG_Short(self.height)
        nbt_file["Length"] = nbt.TAG_Short(self.length)

        block_data = nbt.TAG_Byte_Array()
        block_data.value = self.blocks

        nbt_file["BlockData"] = block_data
        nbt_file["PaletteMax"] = nbt.TAG_Int(Block.max_tags)
        nbt_file["Palette"] = nbt.TAG_Compound()

        for key, value in Block.palette.items():
            nbt_file["Palette"][key] = nbt.TAG_Int(value)

        nbt_file["Version"] = nbt.TAG_Int(2)
        nbt_file["DataVersion"] = nbt.TAG_Int(2975)

        return nbt_file
