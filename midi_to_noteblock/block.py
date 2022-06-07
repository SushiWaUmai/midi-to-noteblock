class Block:
    max_tags = 0
    blocks = []
    palette = {}

    def create(name):
        if name in Block.palette:
            return Block.blocks[Block.palette[name]]

        block = Block()
        block.name = name
        block.index = Block.max_tags

        Block.max_tags += 1
        Block.blocks.append(block)

        Block.palette[block.name] = block.index

        return block

    def get(index):
        return Block.blocks[index]
