"""
This is supposed to get a dictionary file and get the nicer words out of it.
By nicer I mean easy to remember and type (in theory);
"""

import sys
import re

if __name__ == "__main__":

    only_letters = re.compile('^[a-z]{1,5}$')
    bad_sequences = re.compile('(ea|ae|ch|sch|au|eu)+')

    for word in sys.stdin:
        word = word.strip().lower()

        if only_letters.match(word) is None:
            continue

        if bad_sequences.match(word) is not None:
            continue

        print (word)
