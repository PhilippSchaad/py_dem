from collections import Counter
import marshal


# Huffman-Tree-Node object class.
class _Node(object):

    # Object creation procedure.
    def __init__(self, weight, char_set, l_child=None, r_child=None):
        self.char_set = char_set
        self.weight = weight
        self.l_child = l_child
        self.r_child = r_child


# Huffman-Tree object class.
class _HuffmanTree(object):

    # Object creation procedure.
    def __init__(self):
        self.root = None


# Huffman Encoder/Decoder object class.
class HuffmanCoder(object):

    # Create the huffman-encoding table.
    def _create_encoding_table(self):
        char_counter = Counter(self._input_string)
        for c in self._input_string:
            self._total_char_count += 1
            if c not in self._occurrence_dict.keys():
                self._occurrence_dict[c] = char_counter[c]

        tree = _HuffmanTree()
        levels = []
        t_bottom = []
        for k in self._occurrence_dict.keys():
            t_bottom.append(_Node(self._occurrence_dict[k], {k}))
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
            if min_1.weight < min_2.weight:
                n_l_child = min_2
                n_r_child = min_1
            else:
                n_l_child = min_1
                n_r_child = min_2
            n_level.append(_Node(n_weight, n_char_set,
                                 n_l_child, n_r_child))
            levels.append(n_level)

        tree.root = levels[-1][0]
        if tree.root.weight != self._total_char_count:
            print("Oops! An error has occurred..")
            print("Your file has not been properly encoded.")
            print("Please check the file and try again..")
            exit()

        for c in self._occurrence_dict.keys():
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
            self._encoding_table[c] = encoding
            self._decoding_table[encoding] = c

    # Do the encoding.
    def _encode(self):
        code_length = buffer = length = 0
        for c in self._input_string:
            code = self._encoding_table[c]
            for bit in list(code):
                if bit == '1':
                    buffer = (buffer << 1) | 0x01
                else:
                    buffer <<= 1
                length += 1
                if length == 8:
                    self._output_array.append(buffer)
                    buffer = length = 0
            code_length += len(code)

        if length != 0:
            self._output_array.append(buffer << (8 - length))

    # Do the decoding.
    def _decode(self):
        buffer = ''
        for byte in self._input_string:
            for buffer_length in range(8):
                if (int(byte) >> (7 - buffer_length)) & 1:
                    buffer += '1'
                else:
                    buffer += '0'
                if buffer in self._decoding_table.keys():
                    self._output_array.append(self._decoding_table[buffer])
                    buffer = ''

    # Write the decoded sequence to the file.
    def _write_text_file(self):
        with open(self._output_file_name, 'w') as output_file:
            output_file.write(''.join(self._output_array))

    # Write the encoded sequence to the file.
    def _write_huff_file(self):
        with open(self._output_file_name, 'wb') as output_file:
            marshal.dump((self._decoding_table, bytearray(self._output_array)), output_file)

    # Read the file into a string.
    def _read_text_file(self):
        with open(self._input_file_name, 'r') as input_file:
            self._input_string = input_file.read()

    # Read the huffman file.
    def _read_huff_file(self):
        with open(self._input_file_name, 'rb') as input_file:
            self._decoding_table, self._input_string = marshal.load(input_file)

    # Do the encoding.
    def encode(self, filename, output_filename):
        self._total_char_count = 1
        self._occurrence_dict = {'EOF': 1}
        self._input_string = ''
        self._encoding_table = {}
        self._decoding_table = {}
        self._output_array = []
        self._input_file_name = filename
        self._output_file_name = output_filename

        self._read_text_file()
        self._create_encoding_table()
        self._encode()
        self._write_huff_file()

    # Do the decoding of a file.
    def decode(self, filename, output_filename):
        self._total_char_count = 0
        self._occurrence_dict = {}
        self._input_string = ''
        self._encoding_table = {}
        self._decoding_table = {}
        self._output_array = []
        self._input_file_name = filename
        self._output_file_name = output_filename

        self._read_huff_file()
        self._decode()
        self._write_text_file()

    # Object creation procedure.
    def __init__(self):
        self._total_char_count = 1
        self._occurrence_dict = {'EOF': 1}
        self._input_string = self._input_file_name = self._output_file_name = ''
        self._encoding_table = {}
        self._decoding_table = {}
        self._output_array = []


def main():
    coder = HuffmanCoder()
    coder.encode('input.txt', 'test.huff')
    coder.decode('test.huff', 'output.txt')

main()
