import json
from collections import Counter
from heapq import heappush, heappop

from collections import Counter
from heapq import heappush, heappop



class Huffman:
    def __init__(self, huff_dict = {}):
        self.huff_dict = huff_dict
        self.exchange_huff_dict = dict((v, k) for k,v in self.huff_dict.items())
        self.text = text


    def encode(self, text):
        freq = Counter(text)
        heap = [[weight, [char, ""]] for char, weight in freq.items()]
        while len(heap) > 1:
            lo = heappop(heap)
            hi = heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        self.huff_dict = dict(heappop(heap)[1:])
        self.exchange_huff_dict = dict((v, k) for k,v in self.huff_dict.items())
        print("Huff dict = ", self.huff_dict)
        print("Exchange key val = ", self.exchange_huff_dict)
        encoded_text = ''.join([self.huff_dict[char] for char in text])
        return encoded_text

    def decode(self, encoded_text):
        current_code = ""
        decoded_text = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.exchange_huff_dict:
                decoded_text += self.exchange_huff_dict[current_code]
                current_code = ""
        return decoded_text

if __name__ == '__main__':
    text = "ab,ba,ca\n,0.1,0.2,0.3\n0.4,0.5,0.6\n0.10,0.12,0.16"
    print("length = ", len(text), ", Text: ", text)

    h = Huffman()

    enc_text = h.encode(text)
    print("length = ", len(enc_text), ", Encrypt bin: ", enc_text)

    h2 = Huffman(huff_dict={'1': '000', '6': '0010', '\n': '0011', '0': '01', 'a': '1000', 'b': '1001', '4': '10100', '2': '10101', '5': '101100', 'c': '101101', '3': '10111', ',': '110', '.': '111'})
    rev_text = h2.decode(enc_text)
    print("length = ", len(rev_text), ", Decrypt text: ", rev_text)



