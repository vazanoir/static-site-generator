class TextTypes():
    def __init__(self):
        self.text = "text"
        self.bold = "bold"
        self.italic = "italic"
        self.code = "code"
        self.link = "link"
        self.image = "image"

    def is_valid_type(self, type_to_test):
        return type_to_test in self.__dict__


class BlockTypes():
    def __init__(self):
        self.heading = "heading"
        self.code = "code"
        self.quote = "quote"
        self.unordered_list = "unordered_list"
        self.ordered_list = "ordered_list"
        self.paragraph = "paragraph"

    def is_valid_type(self, type_to_test):
        return type_to_test in self.__dict__
