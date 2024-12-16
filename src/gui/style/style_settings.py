import qdarkstyle


class StyleSheetModifier:
    """Loads qdarkstyle style sheet and allows to modify the style for the whole project"""

    def __init__(self):
        self.dark_stylesheet = ''
        self.dark_stylesheet_raw = qdarkstyle.load_stylesheet()
        self.modify()

    @staticmethod
    def skip_line(iterator, number_of_lines):
        """Skip a line or two"""
        for x in range(number_of_lines):
            next(iterator, None)
        return iterator

    def modify(self):
        """Modify style by removing QComboBox::item:checked and QComboBox::item:selected due to an error"""
        line_iterator = iter(self.dark_stylesheet_raw.splitlines())
        for line in line_iterator:
            if 'QComboBox::item:checked' in line or 'QComboBox::item:selected' in line:
                line_iterator = self.skip_line(line_iterator, 2)
            else:
                self.dark_stylesheet += line
