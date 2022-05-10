# -------- CS315 - Programming Assignment 2 --------
# -------------- SAMYAK PIYA (spi254) --------------


def make_array(filename):
    file = open(filename, "r")
    lines = file.readlines()
    power_list = []

    for i in range(len(lines)):
        lines[i] = lines[i].rstrip("\n")
        lines[i] = int(lines[i])
        power_list.append(lines[i])
    return power_list


# Class for BST nodes representation
class BSTNode:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.parent = None
        self.key = value


# Function to insert new node with given key in BST
def insert(node, key):

    # if the tree is empty, return a new node
    if node is None:
        return BSTNode(key)

    # If less than root, recursively call left subtree
    if key < node.key:
        lchild = insert(node.left, key)
        node.left = lchild
        lchild.parent = node

    # Else recursively call right subtree
    elif key > node.key:
        rchild = insert(node.right, key)
        node.right = rchild
        rchild.parent = node

    return node


# Function to search a given value in the BST
def tree_search(root, value):
    if root is None or value == root.key:
        return root

    if root.key < value:
        return tree_search(root.right, value)

    return tree_search(root.left, value)


# Function that returns the node holding the minimum value for a given BST
def find_min(root):
    while root.left is not None:
        root = root.left
    return root


# Function that returns the node holding the maximum value for a given BST
def find_max(root):
    while root.right is not None:
        root = root.right
    return root


# Function that replaces a tree u with tree v
def transplant(root, u, v):
    if u.parent is None:
        root = v
    elif u == u.parent.left:
        u.parent.left = v
    else:
        u.parent.right = v
    if v is not None:
        v.parent = u.parent


# Function that deletes a node holding a given value as key
def delete_node(root, value):
    node = tree_search(root, value)
    if node is None:
        return False
    else:
        if node.left is None:
            transplant(root, node, node.right)
        elif node.right is None:
            transplant(root, node, node.left)
        else:
            successor = find_min(node.right)
            if successor.parent is not node:
                transplant(root, successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor
            transplant(root, node, successor)
            successor.left = node.left
            successor.left.parent = successor
        return True


# Function that prints the tree in preorder traversal
def preorder(root):
    if root:
        print(root.key, end=" ")
        preorder(root.left)
        preorder(root.right)


# Function that prints the tree in postorder traversal
def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.key, end=" ")


# Function that prints the tree in inorder traversal
def inorder(root):
    if root:
        inorder(root.left)
        print(root.key, end=" ")
        inorder(root.right)


# Function that makes a corresponding BST for a given array
def make_bst(array):
    root = BSTNode(array[0])
    for i in range(1, len(array)):
        root = insert(root, array[i])
    return root


# ------------------- Execution ------------------- #

# creating corresponding arrays from the csv file
array1 = make_array("test1.csv")
array2 = make_array("test2.csv")
array3 = make_array("test3.csv")

# creating BSTs from those arrays
BST1 = make_bst(array1)
BST2 = make_bst(array2)
BST3 = make_bst(array3)

# Testing for tree_search, find_max, and find_min
print(f"Searching for '0' in the tree from 'test1.csv' returns the node {tree_search(BST1, 0)} but searching"
      f" for -1 and 129 returns {tree_search(BST1, -1)} and {tree_search(BST1, 129)} respectively.");
print(f"The key of max in 'test1.csv', 'test2.csv', and 'test3.csv' are {find_max(BST1).key}, {find_max(BST2).key}, "
      f"and {find_max(BST3).key} respectively.")
print(f"The key of min in 'test1.csv', 'test2.csv', and 'test3.csv' are {find_min(BST1).key}, {find_min(BST2).key}, "
      f"and {find_min(BST3).key} respectively.")


# Testing traversals with BST generated from 'test1.csv'
print()
print("Preorder traversal for BST resulting from 'test1.csv':")
preorder(BST1)
print(end="\n\n")

print("Postorder traversal for BST resulting from 'test1.csv':")
postorder(BST1)
print(end="\n\n")


print("Inorder traversal for BST resulting from 'test1.csv':")
inorder(BST1)
print(end="\n\n")

# Testing for delete_node (on BST1)
print("Inorder traversal before any deletion:")
inorder(BST1)
print()

print("Inorder traversal after deleting 32 from BST resulting from 'test1.csv'")
delete_node(BST1, 32)
inorder(BST1)
print()

print("Inorder traversal after deleting 64 from BST resulting from 'test1.csv'")
delete_node(BST1, 64)
inorder(BST1)
print()

print("Inorder traversal after deleting 96 from BST resulting from 'test1.csv'")
delete_node(BST1, 96)
inorder(BST1)
print()

print("Inorder traversal after deleting 128 from BST resulting from 'test1.csv'")
delete_node(BST1, 128)
inorder(BST1)
print()


