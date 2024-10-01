from parentnode import ParentNode
from leafnode import LeafNode
from conversion import text_to_text_nodes, text_node_to_html_node


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
                self.__heading_length = i + 1
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

    def to_html(self, block):
        self.__block = block

        if self.__is_heading():
            children = []
            for node in text_to_text_nodes(block[self.__heading_length + 1:]):
                children.append(text_node_to_html_node(node))

            return ParentNode(
                children,
                f"h{self.__heading_length}",
            )
        if self.__is_code():
            return ParentNode([LeafNode(block[3:-3].strip(), "code")], "pre")
        if self.__is_quote():
            new_block = ""
            for line in block.split("\n"):
                new_block += line[2:] + "\n"

            children = []
            for node in text_to_text_nodes(new_block.strip()):
                children.append(text_node_to_html_node(node))
            return ParentNode(children, "quote")
        if self.__is_ul():
            children = []
            for line in block.split("\n"):
                inner_children = []
                for node in text_to_text_nodes(line[2:]):
                    inner_children.append(text_node_to_html_node(node))
                children.append(ParentNode(inner_children, "li"))
            return ParentNode(children, "ul")
        if self.__is_ol():
            children = []
            for line in block.split("\n"):
                inner_children = []
                for node in text_to_text_nodes(line[3:]):
                    inner_children.append(text_node_to_html_node(node))
                children.append(ParentNode(inner_children, "li"))
            return ParentNode(children, "ol")

        children = []
        for node in text_to_text_nodes(block):
            children.append(text_node_to_html_node(node))

        return ParentNode(children, "p")


def block_to_block_type(text_block):
    return BlockTypes().get_type(text_block)
