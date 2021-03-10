import re
import pandas as pd
import csv
import sys
import spacy
import medspacy
import en_info_3700_i2b2_2012
from medspacy.util import DEFAULT_PIPENAMES
from medspacy.section_detection import Sectionizer
from medspacy.context import ConTextComponent, ConTextRule
import codecs
import warnings
warnings.filterwarnings("ignore")

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
#Part of the code was obtained from here: https://github.com/medspacy/medspacy/blob/master/notebooks/11-QuickUMLS_Extraction.ipynb 
#and here: https://github.com/medspacy/medspacy/blob/master/notebooks/section_detection/1-Clinical-Sectionizer.ipynb

df_medspacy_annotations = pd.DataFrame(columns=['Tweet_id','Text_section','Span_start','Span_end','Annotation_type','Extras'])
df_medspacy_tweets_tagged = pd.DataFrame(columns=['Tweet_id','Tweet_full_text'])

#------------We setup the tagger using Quick UMLS-------------------
print("Configuring the Medspacy tagger. Please wait...")

nlp ={}

#Configuring the Medspacy Tagger
nlp['default'] = en_info_3700_i2b2_2012.load()
sectionizer = Sectionizer(nlp['default'])
nlp['default'].add_pipe(sectionizer)

for index, row in df_filtered.iterrows():

    annotation_default = nlp['default'](str(row['tweet_text']))

    #Default model
    if len(annotation_default.ents) > 0:
        df_medspacy_tweets_tagged.loc[len(df_medspacy_tweets_tagged.index)] = [row['tweet_id'], row['tweet_text']]

        for ent in annotation_default.ents:
            df_medspacy_annotations.loc[len(df_medspacy_annotations)] = [row['tweet_id'], ent, ent.start_char, ent.end_char, ent.label_, ent._.section_category] 
    
    else:
        df_medspacy_annotations.loc[len(df_medspacy_annotations)] = [row['tweet_id'], None, None, None, None, None]


with codecs.open(fileN[:-4]+"_medspacy_annotations.tsv",'w','utf-8') as write_tsv:
    write_tsv.write(df_medspacy_annotations.to_csv(sep='\t', index=False))

with codecs.open(fileN[:-4]+"_medspacy_tweets_tagged.tsv",'w','utf-8') as write_tsv:
    write_tsv.write(df_medspacy_tweets_tagged.to_csv(sep='\t', index=False))

print("Done!")