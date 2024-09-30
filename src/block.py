def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    return list(map(lambda block: block.strip(), blocks))


class BlockTypes():
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"
    paragraph = "paragraph"

    def __is_heading(self):
        pattern = " "
        for i in range(6):
            pattern = "#" + pattern
            if self.__block.find(pattern, 0, i + 2) != -1:
                return True
        return False

    def __is_code(self):
        pattern = "```"
        if self.__block[:3] == pattern and self.__block[-3:] == pattern:
            return True
        return False

    def __is_quote(self):
        status = True
        lines = self.__block.split("\n")
        for line in lines:
            if line[:2] != "> " and line != "":
                status = False
        return status

    def __is_ul(self):
        status = True
        lines = self.__block.split("\n")
        for line in lines:
            if line[:2] != "- " and line[:2] != "* " and line != "":
                status = False
        return status

    def __is_ol(self):
        status = True
        lines = self.__block.split("\n")
        for line in lines:
            line_number = lines.index(line) + 1
            if line[:3] != f"{line_number}. " and line != "":
                status = False
        return status

    def get_type(self, block):
        self.__block = block

        if self.__is_heading():
            return self.heading
        if self.__is_code():
            return self.code
        if self.__is_quote():
            return self.quote
        if self.__is_ul():
            return self.unordered_list
        if self.__is_ol():
            return self.ordered_list

        return self.paragraph


def block_to_block_type(text_block):
    return BlockTypes().get_type(text_block)
