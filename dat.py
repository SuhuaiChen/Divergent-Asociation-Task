"""Compute score for Divergent Association Task,
a quick and simple measure of creativity
(Copyright 2021 Jay Olson; see LICENSE)"""
import math
import re
import numpy
import scipy.spatial.distance


class Model:
    """Create model to compute DAT"""

    def __init__(self, pattern="^[a-z][a-z-]*[a-z]$", lang='EN'):
        """Join model and words matching pattern in dictionary"""
        if lang == "EN":
            encoding = "utf-8"
            model = "model/glove.840B.300d.txt"
            dictionary = "model/words.txt"
        elif lang == "ES":
            encoding = "iso-8859-1"
            model = "model/SBW-vectors-300-min5.txt",
            dictionary = "model/spanishWords.txt"
        else:
            raise Exception("Only EN and ES are supported")
        # Keep unique words matching pattern from file
        words = set()
        with open(dictionary, "r", encoding=encoding) as f:
            for line in f:
                if re.match(pattern, line):
                    words.add(line.rstrip("\n"))

        # Join words with model
        vectors = {}
        with open(model, "r", encoding=encoding) as f:
            for line in f:
                token = line.split(" ")
                word = token[0]
                if word in words:
                    vector = numpy.asarray(token[1:], "float32")
                    vectors[word] = vector
        self.vectors = vectors
        self.encoding = encoding
        self.lang = lang

    def validate(self, word):
        """Clean up word and find best candidate to use"""

        # Strip unwanted characters
        clean = re.sub(r"[^a-zA-Z- ]+", "", word).strip().lower()
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

        """
        Modification of the original script starts here
        """
        # add a nested dictionary to save individual scores!
        outer = {}

        """Compute DAT score"""
        # Keep only valid unique words
        uniques = []
        for word in words:
            valid = self.validate(word)
            if valid and valid not in uniques:
                uniques.append(valid)

        # Keep subset of words
        if len(uniques) >= minimum:
            subset = uniques[:minimum]
        else:
            return None # Not enough valid words

        # Compute distances between each pair of words
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

        # Compute the DAT score (average semantic distance multiplied by 100)
        # passing the nested dictionary 'outer' to get individual score charts later
        return int(sum(distances) / len(distances)), outer
