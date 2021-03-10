import re
import pandas as pd
import csv
import sys
import spacy
import scispacy
import en_core_sci_lg
from scispacy.linking import EntityLinker
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

#Part of the following code was obtained from here:
#https://github.com/allenai/scispacy
#Getting the annotations from each of the tweet's text

df_scispacy_annotations = pd.DataFrame(columns=['Tweet_id','Text_section','Span_start','Span_end','Annotation_type','Extras'])
df_scispacy_tweets_tagged = pd.DataFrame(columns=['Tweet_id','Tweet_full_text'])

print("Configuring the Scispacy tagger. Please wait...")
nlp = {}
print("Configuring the UMLS linker. Please wait..")
#We setup the scispacy tagger using the UML linker first
nlp['umls'] = en_core_sci_lg.load()
linker = EntityLinker(resolve_abbreviations=True, name="umls")
nlp['umls'].add_pipe(linker)
linker_umls = nlp['umls'].get_pipe("EntityLinker")


print("Starting the tagging process. Please wait...")

for index, row in df_filtered.iterrows():

    annotation_umls = nlp['umls'](str(row['tweet_text']))

    #UMLS Linker
    count = 0
    if len(annotation_umls.ents) > 0:
        df_scispacy_tweets_tagged.loc[len(df_scispacy_tweets_tagged.index)] = [row['tweet_id'], row['tweet_text']]
        for ent in annotation_umls.ents:
            if len(ent._.kb_ents) > 0:
                df_scispacy_annotations.loc[len(df_scispacy_annotations)] = [row['tweet_id'], ent.text, ent.start_char, ent.end_char, 
                                                                             linker_umls.kb.cui_to_entity[ent._.kb_ents[0][0]].canonical_name, 
                                                                             linker_umls.kb.cui_to_entity[ent._.kb_ents[0][0]].concept_id]
                count += 1
    #If no annotations found from any of the taggers, and empty row will be generated with the tweet_id as the only non-empty field.
    if count == 0:
        df_scispacy_annotations.loc[len(df_scispacy_annotations)] = [row['tweet_id'], None, None, None, None, None]

with codecs.open(fileN[:-4]+"_scispacy_annotations.tsv",'w','utf-8') as write_tsv:
    write_tsv.write(df_scispacy_annotations.to_csv(sep='\t', index=False))

with codecs.open(fileN[:-4]+"_scispacy_tweets_tagged.tsv",'w','utf-8') as write_tsv:
    write_tsv.write(df_scispacy_tweets_tagged.to_csv(sep='\t', index=False))

print("Done!")