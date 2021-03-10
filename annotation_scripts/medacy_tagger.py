#Input format should be a TSV file with at least the following columns (with no headers) and in this order:
#Tweet_Id, Date, Time, Verified, Tweet_Text, Language
import re
import pandas as pd
import csv
import sys
from medacy.model.model import Model
import codecs

pd.options.mode.chained_assignment = None

#Reading the TSV file into a pandas dataframe
fileN = sys.argv[1]
df = pd.read_csv(fileN, sep='\t',encoding = 'utf8',lineterminator='\n', 
                   quoting=csv.QUOTE_NONE, usecols = [0,4,5], names=['tweet_id','tweet_text','tweet_lang'] ,low_memory=False, dtype=str)

#Filtering the tweets to only have English as language
df_filtered = df.loc[df['tweet_lang'] == "en"]
#Convert tweet id's to string
df_filtered['tweet_id'] = df_filtered['tweet_id'].apply(str)


#The following three functions were obtained from the SMMT toolkit. Thanks to the authors.
#https://github.com/thepanacealab/SMMT/tree/master/data_preprocessing
def remove_urls(text):
    result = re.sub(r"http\S+", "", text)
    return(result)

def remove_twitter_urls(text):
    clean = re.sub(r"pic.twitter\S+", "",text)
    return(clean)

def remove_emoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

df_filtered['tweet_text'] = df_filtered['tweet_text'].apply(lambda x : remove_urls(x))
df_filtered['tweet_text'] = df_filtered['tweet_text'].apply(lambda x : remove_twitter_urls(x))
df_filtered['tweet_text'] = df_filtered['tweet_text'].apply(lambda x : remove_emoji(x))

#Getting the annotations from each of the tweet's text
#Part of the following code was obtained from here:
#https://github.com/NLPatVCU/medaCy/

from medacy.model.model import Model

df_medacy_annotations = pd.DataFrame(columns=['Tweet_id','Text_section','Span_start','Span_end','Annotation_type','Extras'])
df_medacy_tweets_tagged = pd.DataFrame(columns=['Tweet_id','Tweet_full_text'])

model = Model.load_external('medacy_model_clinical_notes')

print("Configuring the Medacy tagger. Please wait...")
for index, row in df_filtered.iterrows():

    annotation = model.predict(row['tweet_text'])

    if len(annotation) > 0:
        df_medacy_tweets_tagged.loc[len(df_medacy_tweets_tagged.index)] = [row['tweet_id'], row['tweet_text']]

        for i in range(len(annotation)):
            df_medacy_annotations.loc[len(df_medacy_annotations)] = [row['tweet_id'], annotation.annotations[i][3], annotation.annotations[i][1], annotation.annotations[i][2], annotation.annotations[i][0], None] 
    else:
        df_medacy_annotations.loc[len(df_medacy_annotations)] = [row['tweet_id'], None, None, None, None, None]

with codecs.open(fileN[:-4]+"_medacy_annotations.tsv",'w','utf-8') as write_tsv:
    write_tsv.write(df_medacy_annotations.to_csv(sep='\t', index=False))

with codecs.open(fileN[:-4]+"_medacy_tweets_tagged.tsv",'w','utf-8') as write_tsv:
    write_tsv.write(df_medacy_tweets_tagged.to_csv(sep='\t', index=False))

print("Done!")