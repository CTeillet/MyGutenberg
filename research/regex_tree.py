from research.rg_symbole import CONCAT, ETOILE, ALTERN, DOT


class RegExTree:
    def __init__(self, root, sub_trees):
        self.root = root
        self.sub_trees = sub_trees

    def root_to_string(self):
        if self.rootroot == CONCAT:
            return "."
        if self.root == ETOILE:
            return "*"
        if self.root == ALTERN:
            return "|"
        if self.root == DOT:
            return "."
        return chr(self.root)

    def to_string(self):
        if len(self.sub_trees) == 0:
            return self.rootToString()
        result = self.rootToString() + "(" + self.sub_trees[0].toString()
        for st in self.sub_trees:
            result += st.toString() + ","
        return result + ")"
