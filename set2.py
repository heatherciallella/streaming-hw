from nltk.tokenize import word_tokenize
import numpy as np


def data_stream():
    """Stream the data in 'leipzig100k.txt' """
    with open('leipzig100k.txt', 'r') as f:
        for line in f:
            for w in word_tokenize(line):
                if w.isalnum():
                    yield w


def bloom_filter_set():
    """Stream the data in 'Proper.txt' """
    with open('Proper.txt', 'r') as f:
        for line in f:
            yield line.strip()


############### DO NOT MODIFY ABOVE THIS LINE #################


# Implement a universal hash family of functions below: each function from the
# family should be able to hash a word from the data stream to a number in the
# appropriate range needed.

from itertools import count
from math import e, sqrt


def find_prime(min_value):
    for i in count(min_value + 1):
        if all(i % j != 0 for j in range(2, int(sqrt(min_value + 1)))):
            return i


def uhf(p, rng):
    """Returns a hash function that can map a word to a number in the range
    0 - rng
    """
    a = np.random.randint(1, p)
    b = np.random.randint(0, p)
    return lambda x: ((a * x + b) % p) % rng


###############

################### Part 1 ######################

from bitarray import bitarray

# size = 2 ** 18  # size of the filter
#
# hash_fns = [uhf(find_prime(1000000000), size) for _ in range(5)]  # place holder for hash functions
# bloom_filter = bitarray(size)
# bloom_filter.setall(False)
# num_words = 0  # number in data stream
# num_words_in_set = 0  # number in Bloom filter's set
# num_positives = 0
# false_positives = 0
#
# for word in bloom_filter_set():  # add the word to the filter by hashing etc.
#     for location in [fn(int(''.join(str(ord(letter)) for letter in word))) for fn in hash_fns]:
#         if not bloom_filter[location]:
#             bloom_filter[location] = True
#
#     num_words_in_set += 1
#
# true_set = [word for word in bloom_filter_set()]
#
# for word in data_stream():  # check for membership in the Bloom filter
#     if all(bloom_filter[location] for location in
#            [fn(int(''.join(str(ord(letter)) for letter in word))) for fn in hash_fns]):
#         num_positives += 1
#
#         if word not in true_set:
#             false_positives += 1
#
#     num_words += 1
#
# fp_prob = (1 - e ** (-5 * num_words_in_set / size)) ** 5
#
# print('Total number of words in stream = %s' % (num_words,))
# print('Total number of words added to bloom filter = %s' % (num_words_in_set,))
# print('Total number of words in stream identified to be in bloom filter = %s' % (num_positives,))
# print('False positive probability = %s' % (fp_prob,))
# print('Expected number of false positives in stream = %s' % (fp_prob * num_words))
# print('Actual number of false positives in stream = %s' % (false_positives,))

################### Part 2 ######################
# from statistics import median
#
# hash_range = 24  # number of bits in the range of the hash functions
# fm_hash_functions = [uhf(find_prime(1000000000), 2**hash_range) for _ in range(35)] # Create the appropriate hashes here
#
# def num_trailing_bits(n):
#     """Returns the number of trailing zeros in bin(n)
#
#     n: integer
#     """
#     n = format(n, 'b')
#
#     return len(n) - len(n.rstrip('0'))
#
# trailing_zeros = [[] for _ in range(35)]
#
# for word in data_stream(): # Implement the Flajolet-Martin algorithm
#     word_as_number = int(''.join(str(ord(letter)) for letter in word))
#     i = 0
#
#     for fn in fm_hash_functions:
#         trailing_zeros[i].append(num_trailing_bits(fn(word_as_number)))
#         i += 1
#
# estimates = [2 ** max(i) for i in trailing_zeros]
# print("Estimate of number of distinct elements = %s" % (median([sum(estimates[i - 5:i]) / len(estimates[i - 5:i])
#                                                                 for i in range(5, 36, 5)]),))

################### Part 3 ######################

var_reservoir = [0] * 512
tracked_words = []

# You can use numpy.random's API for maintaining the reservoir of variables
i = 0

for word in data_stream(): # Implement the AMS algorithm here
    if len(tracked_words) < len(var_reservoir) and (word not in tracked_words):
        tracked_words.append(word)
        var_reservoir[len(tracked_words) - 1] += 1

    elif word in tracked_words:
        var_reservoir[tracked_words.index(word)] += 1

    elif len(tracked_words) == 512:
        rand_number = np.random.randint(0, i)

        if rand_number < 512 and (word not in tracked_words):
            tracked_words[rand_number] = word
            var_reservoir[rand_number] = 1

    i += 1

second_moments = [i * (2 * j - 1) for j in var_reservoir]
third_moments = [i * (3 * j **2 - 3 * j + 1) for j in var_reservoir]

print("Estimate of second moment = %s" % (sum(second_moments) / len(second_moments),))
print("Estimate of third moment = %s" % (sum(third_moments) / len(third_moments),))
