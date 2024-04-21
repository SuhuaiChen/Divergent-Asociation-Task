"""Compute score for Divergent Association Task,
a quick and simple measure of creativity
(Copyright 2021 Jay Olson; see LICENSE)"""
import math
import re
import numpy
import scipy.spatial.distance
from tqdm import tqdm
from utils import normalize


class Model:
    """Create model to compute DAT"""

    def __init__(self, pattern="^[a-z][a-z-]*[a-z]$", lang='EN'):
        """Join model and words matching pattern in dictionary"""
        if lang == "EN":
            model = "model/glove.840B.300d.txt"
            dictionary = "model/words.txt"
        elif lang == "ES":
            model = "model/SBW-vectors-300-min5.txt"
            dictionary = "model/spanishWords.txt"
        else:
            raise Exception("Only EN and ES are supported")

        # Keep unique words matching pattern from file
        # The diccionary was used to make sure that the words are from that language. However, it tured
        words = set()
        with open(dictionary, "r", encoding="utf-8") as f:
            for line in tqdm(f):
                if re.match(pattern, line):
                    words.add(line.rstrip("\n"))
        print("dictionary loaded")

        # Join words with model
        vectors = {}
        with open(model, "r", encoding="utf-8") as f:
            for i, line in tqdm(enumerate(f)):
                token = line.split(" ")
                word = token[0]
                word = normalize(word)
                if lang == "EN" and word not in words:
                    # only applying the dictionary filter on the English words because I haven't found a complete spanish dictionary
                    # for example the current spanish dictionary does not have ojo and computadora
                    continue
                vector = numpy.asarray(token[1:], "float32")
                vectors[word] = vector
        print("word vectors loaded")
        self.vectors = vectors
        self.lang = lang
        self.encoding = "utf-8"

    def validate(self, word):
        """Clean up word and find best candidate to use"""

        # Strip unwanted characters
        clean = re.sub(r"[^a-zA-ZáéíñóúüÁÉÍÑÓÚÜ\- ]+", "", word).lower().strip()
        if len(clean) <= 1:
            return None # Word too short

        # Generate candidates for possible compound words
        # "valid" -> ["valid"]
        # "cul de sac" -> ["cul-de-sac", "culdesac"]
        # "top-hat" -> ["top-hat", "tophat"]
        candidates = []
        if " " in clean:
            candidates.append(re.sub(r" +", "-", clean))
            candidates.append(re.sub(r" +", "", clean))
        else:
            candidates.append(clean)
            if "-" in clean:
                candidates.append(re.sub(r"-+", "", clean))
        for cand in candidates:
            if cand in self.vectors:
                return cand # Return first word that is in model
        return None # Could not find valid word

    def distance(self, word1, word2):
        """Compute cosine distance (0 to 2) between two words"""
        try:
            return scipy.spatial.distance.cosine(self.vectors.get(word1), self.vectors.get(word2))
        except Exception as e:
            print(e)
            return math.nan

    def dat(self, words, minimum=10):

        # add a nested dictionary to save individual scores
        outer = {}

        # a list to save invalid words
        invalid_words = []

        """Compute DAT score"""
        # Keep only valid unique words
        uniques = []
        for word in words:
            valid = self.validate(word)
            if valid and valid not in uniques:
                uniques.append(valid)
            else:
                print(word + " is not a valid word")
                invalid_words.append(word)

        invalid_words = ','.join(invalid_words)

        # Keep subset of words
        if len(uniques) >= minimum:
            subset = uniques[:minimum]
        else:
            # Not enough valid words
            return 0, None, invalid_words

        # Compute distances between each pair of words. Enumerate the combinations
        distances = []
        for i in range(minimum):
            inner = {}
            word1 = subset[i]
            for j in range(i+1, minimum):
                word2 = subset[j]
                dist = int(self.distance(word1, word2) * 100)
                distances.append(dist)
                inner[word2] = dist

            outer[word1] = inner

        # Return the DAT score (average semantic distance multiplied by 100)
        # Return the nested dictionary 'outer', which has all the pair-wise word distances
        # Also return the invalid words for diagnostics
        return int(sum(distances) / len(distances)), outer, invalid_words
