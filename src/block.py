from md_types import BlockTypes


def is_heading(block):
    pattern = " "
    for i in range(6):
        pattern = "#" + pattern
        if block.find(pattern, 0, i + 2) != -1:
            return True
    return False


def is_code(block):
    pattern = "```"
    if block[:3] == pattern and block[-3:] == pattern:
        return True
    return False


def is_quote(block):
    status = True
    lines = block.split("\n")
    for line in lines:
        if line[:2] != "> " and line != "":
            status = False
    return status


def is_ul(block):
    status = True
    lines = block.split("\n")
    for line in lines:
        if line[:2] != "- " and line[:2] != "* " and line != "":
            status = False
    return status


def is_ol(block):
    status = True
    lines = block.split("\n")
    for line in lines:
        line_number = lines.index(line) + 1
        if line[:3] != f"{line_number}. " and line != "":
            status = False
    return status


def block_to_block_type(block):
    block_types = BlockTypes()

    if is_heading(block):
        return block_types.heading
    if is_code(block):
        return block_types.code
    if is_quote(block):
        return block_types.quote
    if is_ul(block):
        return block_types.unordered_list
    if is_ol(block):
        return block_types.ordered_list

    return block_types.paragraph


def get_heading_length(block):
    heading_length = 1

    for i in range(len(block)):
        char = block[i]
        if char == "#" and block[i - 1] == "#":
            heading_length += 1

    return heading_length
