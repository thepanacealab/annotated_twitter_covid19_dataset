import sys
import csv
import pandas as pd
import numpy as np
import codecs

#Converting the TSV file from the medaCy annotations into a dataframe
fileN = sys.argv[1]
df_medacy_annotations = pd.read_csv(fileN, sep='\t',encoding = 'utf8', low_memory=False, dtype=str)
df_medacy_annotations = df_medacy_annotations[df_medacy_annotations['Text_section'].notna()]

#Converting the TSV file from the medSpaCy annotations into a dataframe
fileN = sys.argv[2]
df_medspacy_annotations = pd.read_csv(fileN, sep='\t',encoding = 'utf8', low_memory=False, dtype=str)
df_medspacy_annotations = df_medspacy_annotations[df_medspacy_annotations['Text_section'].notna()]

#Converting the TSV file from the medSpacy annotations into a dataframe
fileN = sys.argv[3]
df_scispacy_annotations = pd.read_csv(fileN, sep='\t',encoding = 'utf8', low_memory=False, dtype=str)
df_scispacy_annotations  = df_scispacy_annotations[df_scispacy_annotations ['Text_section'].notna()]

df_annotation_evaluation = pd.DataFrame(columns=['Tweet_id','tags_medacy','tags_medspacy','tags_scispacy'])

print("Counting the number of ocurrences for each tagger...")
#Counts the number of annotations ocurred per tweet in the medaCy tagger
df_medacy_annotations['count'] = df_medacy_annotations.groupby('Tweet_id')['Tweet_id'].transform('count')
df_medacy_annotations.loc[df_medacy_annotations['Text_section'].isnull(), ['count']] = 0
df_medacy_annotations_temp = df_medacy_annotations.drop_duplicates(subset='Tweet_id', keep="last")

#We add the number of ocurrences in the new dataframe
df_annotation_evaluation['Tweet_id'] = df_medacy_annotations_temp['Tweet_id']
df_annotation_evaluation['tags_medacy'] = df_medacy_annotations_temp['count']

#Counts the number of annotations ocurred per tweet in the medSpaCy tagger
df_medspacy_annotations['count'] = df_medspacy_annotations.groupby('Tweet_id')['Tweet_id'].transform('count')
df_medspacy_annotations.loc[df_medspacy_annotations['Text_section'].isnull(), ['count']] = 0
df_medspacy_annotations_temp = df_medspacy_annotations.drop_duplicates(subset='Tweet_id', keep="last")

#We add the number of ocurrences in the new dataframe
for index, row in df_medspacy_annotations_temp.iterrows():
    df_annotation_evaluation.loc[df_annotation_evaluation["Tweet_id"] == row["Tweet_id"], "tags_medspacy"] = row["count"]

#Counts the number of annotations ocurred per tweet in the sciSpaCy tagger
df_scispacy_annotations['count'] = df_scispacy_annotations.groupby('Tweet_id')['Tweet_id'].transform('count')
df_scispacy_annotations.loc[df_scispacy_annotations['Text_section'].isnull(), ['count']] = 0
df_scispacy_annotations_temp = df_scispacy_annotations.drop_duplicates(subset='Tweet_id', keep="last")

#We add the number of ocurrences in the new dataframe
for index, row in df_scispacy_annotations_temp.iterrows():
    df_annotation_evaluation.loc[df_annotation_evaluation["Tweet_id"] == row["Tweet_id"], "tags_scispacy"] = row["count"]

#We fill empty values with zeros
df_annotation_evaluation = df_annotation_evaluation.fillna(0)

print("Counting overlaps...")

#Counting the overlaps between the medaCy and medSpaCy tagger
frames = [df_medacy_annotations,df_medspacy_annotations]
df_medacy_medspacy = pd.concat(frames)
df_medacy_medspacy_group_by = df_medacy_medspacy.groupby(['Tweet_id','Span_start','Span_end']).size()
new_df = df_medacy_medspacy_group_by.to_frame(name = 'size').reset_index()
new_df = new_df.drop(['Span_start','Span_end'], 1)
#It will only conserve those rows who had a match between two taggers, so, the size must be 2
new_df = new_df[new_df['size'] == 2]
#We group again by Tweet ID, and with this, we get the number of matches per tweet
new_df_group_by = new_df.groupby(['Tweet_id']).size()
new_df = new_df_group_by.to_frame(name = 'size').reset_index()
#Left join which allow us to pass the results from the overlaps to the main dataframe
df_annotation_evaluation = pd.merge(df_annotation_evaluation, new_df, on='Tweet_id', how='left')
#Fill empty spaces (tweets with no overlaps) with 0
df_annotation_evaluation['size'].fillna(value=0, inplace=True)
#Converts the column for the medaCy/medSpacy overlaps to integer
df_annotation_evaluation['size'] = df_annotation_evaluation['size'].astype(int)
#We rename the last column joined
df_annotation_evaluation.columns = [*df_annotation_evaluation .columns[:-1], 'overlap_medacy_medspacy']

#Counting the overlaps between the medaCy and sciSPacy tagger
frames = [df_medacy_annotations,df_scispacy_annotations]
df_medacy_scispacy = pd.concat(frames)
df_medacy_scispacy_group_by = df_medacy_scispacy.groupby(['Tweet_id','Span_start','Span_end']).size()
new_df = df_medacy_scispacy_group_by.to_frame(name = 'size').reset_index()
new_df = new_df.drop(['Span_start','Span_end'], 1)
#It will only conserve those rows who had a match between two taggers, so, the size must be 2
new_df = new_df[new_df['size'] == 2]
#We group again by Tweet ID, and with this, we get the number of matches per tweet
new_df_group_by = new_df.groupby(['Tweet_id']).size()
new_df = new_df_group_by.to_frame(name = 'size').reset_index()
#Left join which allow us to pass the results from the overlaps to the main dataframe
df_annotation_evaluation = pd.merge(df_annotation_evaluation, new_df, on='Tweet_id', how='left')
#Fill empty spaces (tweets with no overlaps) with 0
df_annotation_evaluation['size'].fillna(value=0, inplace=True)
#Converts the column for the medaCy/sciSpacy overlaps to integer
df_annotation_evaluation['size'] = df_annotation_evaluation['size'].astype(int)
#We rename the last column joined
df_annotation_evaluation.columns = [*df_annotation_evaluation .columns[:-1], 'overlap_medacy_scispacy']

#Counting the overlaps between the medSpacy and sciSPacy tagger
frames = [df_medspacy_annotations,df_scispacy_annotations]
df_medspacy_scispacy = pd.concat(frames)
df_medspacy_scispacy_group_by = df_medspacy_scispacy.groupby(['Tweet_id','Span_start','Span_end']).size()
new_df = df_medspacy_scispacy_group_by.to_frame(name = 'size').reset_index()
new_df = new_df.drop(['Span_start','Span_end'], 1)
#It will only conserve those rows who had a match between two taggers, so, the size must be 2
new_df = new_df[new_df['size'] == 2]
#We group again by Tweet ID, and with this, we get the number of matches per tweet
new_df_group_by = new_df.groupby(['Tweet_id']).size()
new_df = new_df_group_by.to_frame(name = 'size').reset_index()
#Left join which allow us to pass the results from the overlaps to the main dataframe
df_annotation_evaluation = pd.merge(df_annotation_evaluation, new_df, on='Tweet_id', how='left')
#Fill empty spaces (tweets with no overlaps) with 0
df_annotation_evaluation['size'].fillna(value=0, inplace=True)
#Converts the column for the medspacy/sciSpacy overlaps to integer
df_annotation_evaluation['size'] = df_annotation_evaluation['size'].astype(int)
#We rename the last column joined
df_annotation_evaluation.columns = [*df_annotation_evaluation .columns[:-1], 'overlap_medspacy_scispacy']

#Converting it to TSV File
with codecs.open("annotation_evaluation.tsv",'w','utf-8') as write_tsv:
    write_tsv.write(df_annotation_evaluation.to_csv(sep='\t', index=False))
print("Done!")