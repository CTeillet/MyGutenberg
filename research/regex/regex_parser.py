import regex_tree as rt
import regex_symbol as rs


def parse_expression(expression: str) -> rt.RegExTree:
    result = []
    for c in expression:
        print(c)
        result.append(rt.RegExTree(rs.char_to_root(c), []))
    return parse(result)


def parse(result) -> rt.RegExTree:
    print(result, "0")
    while contain_parenthese(result):
        result = process_parenthese(result)
    print(result, "1")
    while contain_etoile(result):
        result = process_etoile(result)
    print( len(result[0].sub_trees), "2")
    while contain_concat(result):
        result = process_concat(result)
    print(result, "3")
    while contain_altern(result):
        result = process_altern(result)
    print(result, "4")
    if len(result) > 1:
        raise Exception
    return remove_protection(result[0])


def contain_parenthese(trees):
    for t in trees:
        if t.root == rs.PARENTHESEOUVRANT or t.root == rs.PARENTHESEFERMANT:
            return True
    return False


def process_parenthese(trees):
    result = []
    found = False
    for t in trees:
        if (not found) and t.root == rs.PARENTHESEFERMANT:
            done = False
            content = []
            while (not done) and len(result) != 0:
                if result[-1].root == rs.PARENTHESEOUVRANT:
                    done = True
                    result.pop()
                else:
                    content.insert(0, result.pop())
            if not done:
                raise Exception
            found = True
            sub_trees = [parse(content)]
            result.append(rt.RegExTree(rs.PROTECTION, sub_trees))
        else:
            result.append(t)
    if not found:
        raise Exception
    return result


def contain_etoile(trees):
    for t in trees:
        if t.root == rs.ETOILE and len(t.sub_trees) == 0:
            return True
    return False


def process_etoile(trees):
    results = []
    found = False
    for t in trees:
        if (not found) and t.root == rs.ETOILE and len(t.sub_trees) == 0:
            if len(results) == 0:
                raise Exception
            found = True
            last = results.pop()
            sub_trees = [last]
            results.append(rt.RegExTree(rs.ETOILE, sub_trees))
        else:
            results.append(t)
    return results


def contain_concat(trees):
    found = False
    for t in trees:
        if (not found) and t.root != rs.ALTERN:
            found = True
            continue
        if found:
            if t.root != rs.ALTERN:
                return True
            else:
                found = False
    return False


def process_concat(trees):
    result = []
    found = False
    first_found = False
    for t in trees:
        if (not found) and (not first_found) and t.root != rs.ALTERN:
            first_found = True
            result.append(t)
            continue
        if (not found) and first_found and t.root == rs.ALTERN:
            first_found = False
            result.append(t)
            continue
        if (not found) and first_found and t.root != rs.ALTERN:
            found = True
            last = result.pop()
            sub_trees = [last, t]
            result.append(rt.RegExTree(rs.CONCAT, sub_trees))
        else:
            result.append(t)
    return result


def contain_altern(trees):
    for t in trees:
        if t.root == rs.ALTERN and len(t.sub_trees) == 0:
            return True
    return False


def process_altern(trees):
    result = []
    found = False
    left: rt.RegExTree = None
    done = False
    for t in trees:
        if (not found) and t.root == rs.ALTERN and len(t.sub_trees) == 0:
            if len(result) == 0:
                raise Exception
            found = True
            left = result.pop()
            continue
        if found and not done:
            if left is None:
                raise Exception
            done = True
            sub_trees = [left, t]
            result.append(rt.RegExTree(rs.ALTERN, sub_trees))
        else:
            result.append(t)
    return result


def remove_protection(tree):
    if tree.root == rs.PROTECTION and len(tree.sub_trees) != 1:
        raise Exception
    if len(tree.sub_trees) == 0:
        return tree
    if tree.root == rs.PROTECTION:
        return remove_protection(tree.sub_trees()[0])

    sub_trees = []
    for t in tree.sub_trees:
        sub_trees.append(remove_protection(t))
    return rt.RegExTree(tree.root, sub_trees)
