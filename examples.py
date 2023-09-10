import math
import os

import dat
import pandas as pd
# GloVe model from https://nlp.stanford.edu/projects/glove/
# Spanish Word2Vec model from https://crscardellino.ar/SBWCE/

# preset parameters
INPUT_CSV_DELIMITER = ','
OUTPUT_CSV_DELIMITER = ','

# load source file and model
fname = input("enter input file name: ")
path = 'input/'+fname
lang = input("EN or ES: ")
df = pd.read_csv(path, delimiter=INPUT_CSV_DELIMITER)
num_rows = len(df.index)
print('loading input...')
print('number of columns: ', len(df.columns))
print('number of rows: ', num_rows)
print(df.to_string())
print('loading model...')
model = dat.Model(lang=lang)

# create output directory
output_dir = 'output/%s/%s/' % (lang, fname)
os.makedirs(output_dir, exist_ok=True)
normal_dir = output_dir + 'normal/'
os.makedirs(normal_dir, exist_ok=True)
pivot_dir = output_dir + 'pivot/'
os.makedirs(pivot_dir, exist_ok=True)

# output a csv of cosine distance between each pair of the words
# high cosine distance indicates low relevance
dat_column_values = []
for i in range(num_rows):
    row_id = df.iloc[i, 0]
    row = df.iloc[i, 1:]
    total_scores, scores_dict = model.dat(row)

    dat_column_values.append(total_scores)
    # convert dict to dataframe
    individual_df = pd.DataFrame([i, j, v]
                                 for i in scores_dict.keys()
                                 for j, v in scores_dict[i].items())
    individual_df.columns = ['word1', 'word2', 'cosine distance * 100']
    individual_df.to_csv(normal_dir+str(row_id)+'.csv', sep=OUTPUT_CSV_DELIMITER, encoding=model.encoding)

    # output a pivot table just as the figures shown in the Olson paper
    individual_df_pivot = pd.DataFrame(columns=scores_dict.keys(), index=scores_dict.keys())
    used = []
    for word1 in scores_dict.keys():
        used.append(word1)
        col = []
        for word2 in scores_dict.keys():
            # if the score between word1 and word2 is already calculated, we should skip it
            if word2 in used:
                col.append(math.nan)
            else:
                col.append(scores_dict[word1][word2])
        individual_df_pivot[word1] = col

    individual_df_pivot.to_csv(pivot_dir+str(row_id)+'.csv', sep=OUTPUT_CSV_DELIMITER, encoding=model.encoding)

# output overview
df['dat'] = dat_column_values
print('-'*60)
print('printing overview...')
print(df.to_string())

df.to_csv(output_dir+fname+'.csv', sep=OUTPUT_CSV_DELIMITER, encoding=model.encoding)


'''
# Compound words are translated into words found in the model
print(model.validate("cul de sac")) # cul-de-sac

# Compute the cosine distance between 2 words (0 to 2)
print(model.distance("cat", "dog")) # 0.1983
print(model.distance("cat", "thimble")) # 0.8787

# Compute the DAT score between 2 words (average cosine distance * 100)
print(model.dat(["cat", "dog"], 2)) # 19.83
print(model.dat(["cat", "thimble"], 2)) # 87.87

# Word examples (Figure 1 in paper)
low = ["arm", "eyes", "feet", "hand", "head", "leg", "body"]
average = ["bag", "bee", "burger", "feast", "office", "shoes", "tree"]
high = ["hippo", "jumper", "machinery", "prickle", "tickets", "tomato", "violin"]

# Compute the DAT score (transformed average cosine distance of first 7 valid words)
print(model.dat(low)) # 50
print(model.dat(average)) # 78
print(model.dat(high)) # 95
'''
