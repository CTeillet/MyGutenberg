from research.regex.regex_symbol import CONCAT, ETOILE, ALTERN, DOT


class RegExTree:
    def __init__(self, root: chr, sub_trees):
        self.root = root
        self.sub_trees = sub_trees

    def root_to_chr(self):
        if self.root == CONCAT:
            return '.'
        if self.root == ETOILE:
            return '*'
        if self.root == ALTERN:
            return '|'
        if self.root == DOT:
            return '.'
        return chr(self.root)

    def to_string(self):
        if len(self.sub_trees) == 0:
            return self.root_to_chr()
        result = self.root_to_chr() + "(" + self.sub_trees[0].to_string()
        for st in self.sub_trees[1:]:
            result += "," + st.to_string()
        return result + ")"

    def __str__(self):
        return self.to_string()
