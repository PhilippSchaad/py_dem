# -*- coding: utf-8 -*-
# ============================================= #
# File: huffman.py                              #
# Brief: This file contains a module for      / #
# / encoding .txt files with huffman-encoding / #
# / into compressed .huff files.                #
# Author: Philipp Schaad                        #
# Creation Date: 111215                         #
# Version: 1.0.0                                #
# ============================================= #

# ============================================= #
# Copyright:                                    #
# This piece of software is released under the  #
# GNU General Public License (GNU GPL). As      #
# such, it is free and open source. For more    #
# detailed information please refer to the      #
# provided LICENSE.txt file.                    #
# ============================================= #
"""Huffman-Coding module.

This module contains the necessary functions to encode/compress a .txt file with
Huffman-Coding in to a .huff file, and extract/decompress a .huff file back in to
a human-readable .txt file.
"""

from collections import Counter
import marshal


class _Node(object):
    """[INTERNAL] Node-Element of a Huffman-Tree.

    The node is a central element in a Huffman-Tree. Each node can be either an
    internal node, or a leaf node. Leaf nodes are representative of a single
    character in the huffman-encoding. Internal nodes represent a set of characters,
    consisting of each of their child-sets combined.

    Attributes:
        char_set (set[char]): A set of characters. If this set contains only one character,
            the node is a leaf-node. In the case of an internal node, this set contains
            all the characters of the child-node's char_set's combined.
        weight (int): Keeps track of the weight of this node. The weight is representative
            of the total number of occurrences of the characters contained in the node's
            char_set inside the (to be compressed) text.
        l_child (Node): If the node is an internal node, it will have child-nodes. In this
            case, l_child points to the left child node. If this node is a leaf node,
            l_child will hold the value None.
        r_child (Node): If the node is an internal node, it will have child-nodes. In this
            case, r_child points to the right child node. If this node is a leav node,
            r_child will hold the value None.
    """

    def __init__(self, weight, char_set, l_child=None, r_child=None):
        """Create a new Node.

        Args:
            :param weight (int): The weight of the node.
            :param char_set (set[char]): The characters represented by this node.
            :param l_child (Node): The left child node (default: None)
            :param r_child (Node): The right child node (default: None)
        """
        self.char_set = char_set
        self.weight = weight
        self.l_child = l_child
        self.r_child = r_child


class _HuffmanTree(object):
    """[INTERNAL] Huffman-Tree structure.

    This class is representative of the basic Huffman-Tree. It only serves as a container
    for the root-node. The functionality and purpose of the huffman-tree is entirely
    provided by it's central elements, the Node.

    Attributes:
        root (Node): This points to the root of the tree. Upon creation of a new Tree,
            it will point to None, hence it will need to be assigned after tree creation,
            to a pre-existing Node.
    """

    def __init__(self):
        self.root = None


# Writes a given encoding to the buffer and appends it to the output. For internal use.
def _write_to_buffer(code, buffer, length, output_array):
    """Write a given string (character-encoding) to an integer buffer, representing a byte.

    Given a binary character-encoding in the form of a string of 1's and 0's, this function
    converts it in to byte-code by examining every 'bit' in the code and modifying an integer
    buffer accordingly. If the buffer's length gets to 8 bits, the buffer is appended to the
    output-buffer (which later gets written to the .huff file), and then flushed, to be re-written.

    Args:
        :param code (str): The binary-encoding of a character, in the form of a string of 1's and 0's.
        :param buffer (int): The buffer to continue writing to. Will be 0 if it is empty, otherwise
            it will already contain an integer value in the range of 0-255.
        :param length (int): The current length of the buffer. (eg: how many bits are written)
        :param output_array (List[int]): The output-buffer to append to.

    Returns:
        :return buffer (int): Return the buffer, in case it is not full yet.
        :return length (int): The length of the returned buffer.
    """
    for bit in list(code):
        # Iterate through the code, modifying the buffer accordingly.
        if bit == '1':
            buffer = (buffer << 1) | 0x01
        else:
            # bit == 0:
            buffer <<= 1
        length += 1
        if length == 8:
            # The buffer is full (1 byte), append it to the output and flush it.
            output_array.append(buffer)
            buffer = length = 0
    return buffer, length


def encode(filename, output_filename):
    """Encode a given .txt file in to a compressed .huff file.

    Given a text (.txt) file, encode its content with Huffman-Encoding, compressing the file, and
    then write it back in to a .huff file, prefixed by the used character-encoding table, to make
    decoding the file possible.

    Args:
        :rtype None
        :param filename: Input text file to be compressed/encoded. Must be a string, containing
            the name of an existing, valid .txt file (including the '.txt' file-ending).
        :type filename: str
        :param output_filename: Output huffman-file to be written to. Must be a string, containing
            the name of the desired .huff file, including the '.huff' file ending.
        :type output_filename: str
    """
    # Check if the provided file-names are valid.
    if not filename.endswith('.txt'):
        print("Invalid input-file type! Please provide a '.txt' file!")
        exit()
    if not output_filename.endswith('.huff'):
        print("Invalid output-file type! Huffman encoded files have to be '.huff' files!")
        exit()

    # The encoding table used to encode this file. Will be generated.
    encoding_table = {}
    # The encoding table, inverted in to a decoding table.
    decoding_table = {}
    # The output buffer. Each encoded byte will be appended to this, before writing it to the file.
    output_array = []

    # Read the input text file.
    with open(filename, 'r') as file:
        input_string = file.read()

    # We first count each occurrence of every character in the input text, in order
    # to calculate each frequency and derive an optimal encoding.

    # Add an end-of-file (EOF) character with frequency 1 to the dictionary.
    occurrence_dict = {'EOF': 1}
    total_char_count = 1
    char_counter = Counter(input_string)
    for c in input_string:
        total_char_count += 1
        if c not in occurrence_dict.keys():
            occurrence_dict[c] = char_counter[c]

    # We now build a huffman-tree, according to the number of occurrences of each character.
    tree = _HuffmanTree()
    levels = []
    t_bottom = []
    for k in occurrence_dict.keys():
        t_bottom.append(_Node(occurrence_dict[k], {k}))
    levels.append(t_bottom)
    i = 0
    while True:
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
        i += 1
    tree.root = levels[-1][0]

    # Check if the tree we just built is valid (total-characters = root-weight).
    if tree.root.weight != total_char_count:
        print("Oops! An error has occurred..")
        print("Your file has not been properly encoded.")
        print("Please check the file and try again..")
        exit()

    # Build an encoding for each character in the tree, according to its position in the tree.
    for c in occurrence_dict.keys():
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
        encoding_table[c] = encoding
        decoding_table[encoding] = c

    # Write each encoding to the output buffer, after it has been converted in to binary format.
    buffer = length = 0
    for c in input_string:
        buffer, length = _write_to_buffer(encoding_table[c], buffer, length, output_array)
    buffer, length = _write_to_buffer(encoding_table['EOF'], buffer, length, output_array)
    if length != 0:
        output_array.append(buffer << (8 - length))

    # Write the encoded huffman file back.
    with open(output_filename, 'wb') as file:
        marshal.dump((decoding_table, bytearray(output_array)), file)


def decode(filename, output_filename):
    """Decode a given .huff file in to a human readable .txt text-file.

    Read in a given .huff file and extract the used encoding table. Using that encoding table,
    decode the file back in to human readable text-format, before writing it back in to the
    specified .txt file.

    Args:
        :rtype: None
        :param filename: The .huff file to decode. This should be a string containing a valid
            filename, of an existing .huff file, including the '.huff' file-extension.
        :type filename: str
        :param output_filename: The .txt file to write to. This should be a string containing
            a valid filename, including the '.txt' file-extension.
        :type output_filename: str
    """
    # Check if the provided file-names are valid.
    if not filename.endswith('.huff'):
        print("Invalid input-file type! Only '.huff' files can be decoded!")
        exit()
    if not output_filename.endswith('.txt'):
        print("Invalid output-file type! Please provide a '.txt' file!")
        exit()

    # Read the encoded huffman file.
    with open(filename, 'rb') as file:
        decoding_table, input_string = marshal.load(file)

    # Decode the file.
    output_array = []
    buffer = ''
    for byte in input_string:
        # Examine every byte in the input_string, bit by bit, appending 1's and 0's
        # to the buffer respectively.
        for buffer_length in range(8):
            if (int(byte) >> (7 - buffer_length)) & 1:
                buffer += '1'
            else:
                buffer += '0'
            if buffer in decoding_table.keys():
                # If at any stage we find the code currently in the buffer in the
                # decoding table, we append the decoded character to the output-buffer
                # and flush the buffer, to be re-filled.
                if decoding_table[buffer] == 'EOF':
                    break
                else:
                    output_array.append(decoding_table[buffer])
                    buffer = ''

    # Write the decoded text file back.
    with open(output_filename, 'w') as output_file:
        output_file.write(''.join(output_array))
