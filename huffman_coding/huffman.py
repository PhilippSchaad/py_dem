from collections import Counter


# Huffman-Tree-Node object class.
class Node(object):

    # Object creation procedure.
    def __init__(self, weight, char_set, l_child=None, r_child=None):
        self.char_set = char_set
        self.weight = weight
        self.l_child = l_child
        self.r_child = r_child


# Huffman-Tree object class.
class HuffmanTree(object):

    # Object creation procedure.
    def __init__(self):
        self.root = None


# Huffman Encoder/Decoder object class.
class HuffmanCoder(object):

    # Create the huffman-encoding table.
    def create_encoding_table(self):
        char_counter = Counter(self.input_string)
        for c in self.input_string:
            self.total_char_count += 1
            if c not in self.occurance_dict.keys():
                self.occurance_dict[c] = char_counter[c]

        tree = HuffmanTree()
        levels = []
        t_bottom = []
        for k in self.occurance_dict.keys():
            t_bottom.append(Node(self.occurance_dict[k], {k}))
        levels.append(t_bottom)

        for i in range(5000):
            if len(levels[i]) < 2:
                break
            n_level = []
            min_1 = min_2 = None
            for node in levels[i]:
                if min_1 is None:
                    min_1 = node
                elif min_2 is None:
                    min_2 = node
                else:
                    if min_1.weight == max(min_1.weight, min_2.weight):
                        if node.weight < min_1.weight:
                            min_1 = node
                    elif node.weight < min_2.weight:
                        min_2 = node
            for node in levels[i]:
                if (node is not min_1) and (node is not min_2):
                    n_level.append(node)
            n_weight = min_1.weight + min_2.weight
            n_char_set = min_1.char_set | min_2.char_set
            n_l_child = n_r_child = None
            if min_1.weight < min_2.weight:
                n_l_child = min_2
                n_r_child = min_1
            else:
                n_l_child = min_1
                n_r_child = min_2
            n_level.append(Node(n_weight, n_char_set,
                n_l_child, n_r_child))
            levels.append(n_level)

        tree.root = levels[-1][0]
        if tree.root.weight != self.total_char_count:
            print("Oops! An error has occured..")
            print("Your file has not been properly encoded.")
            print("Please check the file and try again..")
            exit()

        for c in self.occurance_dict.keys():
            seq = []
            active = tree.root
            while not (active.l_child is None or active.r_child is None):
                if c in active.l_child.char_set:
                    seq.append('0')
                    active = active.l_child
                else:
                    seq.append('1')
                    active = active.r_child
            encoding = ''.join(seq)
            self.encoding_table[c] = encoding
            self.decoding_table[encoding] = c

    # Read the file into a string.
    def read_file(self):
        with open(self.input_file_name, 'r') as input_file:
            self.input_string = input_file.read()

    # Do the encoding.
    def encode(self, filename):
        self.input_file_name = filename
        self.read_file()
        self.create_encoding_table()

    # Object creation procedure.
    def __init__(self):
        self.total_char_count = 1
        self.occurance_dict = {'EOF': 1}
        self.input_string = self.input_file_name = ''
        self.encoding_table = {}
        self.decoding_table = {}

def main():
    coder = HuffmanCoder()
    coder.encode('input.txt')
    print("Encoding table:", coder.encoding_table)
    print("Decoding table:", coder.decoding_table)
    
main()

