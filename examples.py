import math
import os
import dat
import pandas as pd

# preset parameters
INPUT_CSV_DELIMITER = ','
OUTPUT_CSV_DELIMITER = ','

def distance_matrix(task_name):
    # choose language: you should write it in the terminal and then press enter
    lang = input("Choose a language. Please type EN or ES, then press enter: ")
    if lang == "EN":
        fname = f"{task_name}_Eng"
    elif lang == "ES":
        fname = f"{task_name}_Spa"
    else:
        raise Exception("lang should be either EN or ES")

    # read input csv
    print(f'loading input/{fname}.csv')
    path = 'input/' + fname + '.csv'
    df = pd.read_csv(path, delimiter=INPUT_CSV_DELIMITER)
    
    first_word_index = 1
    columns_to_select = ['subject', 'Block', 'Trial'] + [f'FF{i}.text' for i in range(1, 21)]
    
    if task_name == "FF":
        df = df[columns_to_select]
        first_word_index = 3
        
    num_rows = len(df.index)
    num_cols = len(df.columns)
    print('number of columns: ', len(df.columns))
    print('number of rows: ', num_rows)

    # load model
    print('loading model...')
    model = dat.Model(lang=lang)

    # create output directory
    output_dir = f'output/{fname}/'
    os.makedirs(output_dir, exist_ok=True)
    normal_dir = output_dir + 'normal/'
    os.makedirs(normal_dir, exist_ok=True)
    pivot_dir = output_dir + 'pivot/'
    os.makedirs(pivot_dir, exist_ok=True)

    # output a csv of cosine distance between each pair of the words
    # high cosine distance indicates low relevance
    dat_column_values = []
    invalid_word_column_values = []

    # a list of list to store FF values
    ff_values = []
    
    # a list of all the individual word scores
    all_individual_dfs = []
    
    for i in range(num_rows):
        id = df.iloc[i, 0]
        input_words = df.iloc[i, first_word_index:].to_list()

        # get average scores number, scores dict, and invalid words of the current participant
        total_scores, scores_dict, invalid_words = model.dat(input_words)
        dat_column_values.append(total_scores)
        invalid_word_column_values.append(invalid_words)

        # convert scores dict to dataframe
        individual_df = pd.DataFrame([i, j, v]
                                     for i in scores_dict.keys()
                                     for j, v in scores_dict[i].items())
        individual_df.columns = ['word1', 'word2', 'cosine distance']

        # save the normal word pair scores table
        individual_df.to_csv(normal_dir + str(i) + '.csv', sep=OUTPUT_CSV_DELIMITER, encoding=model.encoding)

        # output a pivot table just as the figures shown in the Olson paper
        individual_df_pivot = pd.DataFrame(columns=input_words, index=input_words)
        used = []
        for word1 in input_words:
            used.append(word1)
            col = []
            for word2 in input_words:
                # if the score between word1 and word2 is already calculated, we should skip it
                if word2 in used:
                    col.append(math.nan)
                else:
                    col.append(scores_dict[word1][word2])
            individual_df_pivot[word1] = col

        # save the scores in a pivot table
        individual_df_pivot.to_csv(pivot_dir + str(i) + '.csv', sep=OUTPUT_CSV_DELIMITER, encoding=model.encoding)

        # calculate ff value
        ff_value = individual_df_pivot.mean(axis=1, numeric_only=True).round(3).to_list()
        ff_values.append(ff_value)
        
        # Add subject, block, trial
        if task_name == "FF":
            individual_df['subject'] = df.iloc[i, 0]
            individual_df['block'] = df.iloc[i, 1]
            individual_df['trial'] = df.iloc[i, 2]
            individual_df = individual_df[['subject', 'block', 'trial', 'word1', 'word2', 'cosine distance']]
        
        else:
            # using row_id here for now since the input file doesn't have subject, block, trial
            individual_df['id'] = id
            individual_df = individual_df[['id', 'word1', 'word2', 'cosine distance']]
        
        # append to the list
        all_individual_dfs.append(individual_df)
    
    # concatenate all individual dataframes into one
    combined_df = pd.concat(all_individual_dfs, ignore_index=True)

    # save the combined dataframe to a single CSV file
    combined_df.to_csv(output_dir + fname +'_words.csv', sep=OUTPUT_CSV_DELIMITER, encoding=model.encoding, index=False)

    if task_name == "DAT":
        # create the DAT overview of all the candidates.
        # It keeps the original input and appends DAT scores and invalid words at the end
        df['dat'] = dat_column_values
        df['invalid words'] = invalid_word_column_values
        print('-' * 60)
        print('printing overview...')
        print(df.to_string())
        # save the overview result
        df.to_csv(output_dir + fname + '.csv', sep=OUTPUT_CSV_DELIMITER, encoding=model.encoding)

    else:
        # create FF serial flow for all the candidates
        rows = []
        for i in range(num_rows):
            # Original row
            original_row = df.iloc[i, :].to_list() + [None]
            rows.append(original_row)
            
            # Insert ff_values below the row
            ff_row = [None, None, None] + ff_values[i] + [invalid_word_column_values[i]]
            rows.append(ff_row)
            
            # Insert blank rows
            rows.append([None] * len(ff_row))

        # Convert the updated structure back into a DataFrame
        df = pd.DataFrame(rows, columns=df.columns.tolist() + ['invalid words'])
        
        # Convert decimals to integers while leaving blank values (NaN) untouched
        df['subject'] = pd.to_numeric(df['subject'], errors='coerce').round().astype('Int64')
        df['Block'] = pd.to_numeric(df['Block'], errors='coerce').round().astype('Int64')
        df['Trial'] = pd.to_numeric(df['Trial'], errors='coerce').round().astype('Int64')

        # Rename columns
        df = df.rename(columns={'Block': 'block', 'Trial': 'trial'})

        df.to_csv(output_dir + fname + '.csv', sep=OUTPUT_CSV_DELIMITER, encoding=model.encoding)
    print("Done")

def DAT_Task():
    distance_matrix(task_name="DAT")


def FF_Task():
    distance_matrix(task_name="FF")


if __name__ == '__main__':
    task_name = input ("Enter the task name (DAT or FF): ")
    if task_name == "DAT":
        DAT_Task()
    elif task_name == "FF":
        FF_Task()
    else:
        print("Invalid task name. Please enter either 'DAT' or 'FF'.")

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
