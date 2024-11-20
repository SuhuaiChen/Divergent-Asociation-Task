"""Compute score for Divergent Association Task,
a quick and simple measure of creativity"""

import math
import re
import numpy as np
from spacy.lang.en.stop_words import STOP_WORDS as EN_STOP_WORDS
from spacy.lang.es.stop_words import STOP_WORDS as ES_STOP_WORDS
import scipy.spatial.distance
from tqdm import tqdm

class Model:
    """Create model to compute DAT"""

    def __init__(self, lang='EN'):
        """Join model and words matching pattern in dictionary"""
        if lang == "EN":
            model = "model/glove.840B.300d.txt"
            # dictionary = "model/words.txt"
            self.encoding = "utf-8"
            self.stopwords = EN_STOP_WORDS | {'use', 'thing', 'things'}
            
        elif lang == "ES":
            model = "model/SBW-vectors-300-min5.txt"
            # dictionary = "model/spanishWords.txt"
            self.encoding = "utf-8"
            self.stopwords = ES_STOP_WORDS | {'usar', 'uso','usa', 'usan', 'cosa', 'cosas'}
        else:
            raise Exception("Only EN and ES are supported")
        
        print("stopwords:", self.stopwords)

        # Keep unique words matching pattern from file
        # The diccionary was used to make sure that the words are from that language. However, it tured
        # words = set()
        # with open(dictionary, "r", encoding=self.encoding) as f:
        #     for line in tqdm(f):
        #         if re.match(pattern, line):
        #             words.add(line.rstrip("\n"))
        # print("dictionary loaded")

        # Join words with model
        vectors = {}
        with open(model, "r", encoding=self.encoding) as f:
            for i, line in tqdm(enumerate(f)):
                token = line.split(" ")
                word = token[0].lower()

                # word = normalize(word)
                # if lang == "EN" and word not in words:
                #     # only applying the dictionary filter on the English words because I haven't found a complete spanish dictionary
                #     # for example the current spanish dictionary does not have ojo and computadora
                #     continue
                vector = np.asarray(token[1:], "float32")

                # The words in spanish model text are ordered from most frequent to least frequent
                # We only use the most frequent word if there are duplicate words
                if word not in vectors:
                    vectors[word] = vector

        print("word vectors loaded")
        self.vectors = vectors
        self.lang = lang

    def validate(self, candidate):
        """Clean up words in a candidate and compute mean vector if necessary"""

        # Strip unwanted characters from the candidate
        clean_phrase = re.sub(r"[^a-zA-ZáéíñóúüÁÉÍÑÓÚÜ\s-]+", "", candidate).lower().strip()
        if len(clean_phrase) <= 0:
            return None  # Empty word

        words = clean_phrase.split()
        words = [word for word in words if word not in self.stopwords]
        
        valid_vectors = []
        
        for word in words:
            clean_word = word.strip()
            if clean_word in self.vectors:
                valid_vectors.append(self.vectors[clean_word])

        if valid_vectors:
            # Compute mean pooling for candidate
            return np.mean(valid_vectors, axis=0)
        return None  # No valid words found in the candidate

    def distance(self, vec1, vec2):
        """Compute cosine distance (0 to 2) between two vectors"""
        return round(float(scipy.spatial.distance.cosine(vec1, vec2)), 3)

    def dat(self, words):

        # add a nested dictionary to save individual scores
        outer = {}

        # a list to save invalid words
        invalid_words = []

        """Compute DAT score"""
        # Keep only valid unique words
        words_validated = []
        for word in words:
            valid = self.validate(word)
            if valid is not None:
                words_validated.append(valid)
            else:
                words_validated.append(word)
                print(word + " is not a valid word")
                invalid_words.append(word)

        invalid_words = ','.join(invalid_words)

        # Compute distances between each pair of words. Enumerate the combinations
        distances = []
        for i in range(len(words)):
            inner = {}
            word1 = words[i]
            
            # Skip if word1 already exists in the dictionary
            if word1 in outer:
                continue
            
            word1_validated = words_validated[i]
            for j in range(i+1, len(words)):
                word2 = words[j]
                word2_validated = words_validated[j]
                try:
                    dist = self.distance(word1_validated, word2_validated)
                    distances.append(dist)
                except:
                    dist = math.nan

                inner[word2] = dist

            outer[word1] = inner

        # Only take the first 7 valid words to compute the average semantic distance
        if len(distances) > 7:
            distances = distances[:7]
            
        score = 0 if len(distances) == 0 else int((sum(distances) / len(distances))*100)

        # Return the DAT score (average semantic distance multiplied by 100)
        # Return the nested dictionary 'outer', which has all the pair-wise word distances
        # Also return the invalid words for diagnostics
        return score, outer, invalid_words