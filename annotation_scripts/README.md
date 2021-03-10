# Annotation scripts - INSTRUCTIONS


## Requirements - General
Python 3.7+ is required for all scripts to work properly, as well as [Pandas](https://pypi.org/project/pandas/ "Pandas") and [NumPy](https://pypi.org/project/numpy/ "NumPy"). The specific requirements for each tagger, are listed down below:

### MedaCy -Requirements
- Gensim 3.8.x
```
pip install gensim
```
- SpaCy 2.2.2
```
pip install spacy==2.2.2
```
- [MedaCy](http://https://github.com/NLPatVCU/medaCy "MedaCy") 1.0.0
```
pip install git+https://github.com/NLPatVCU/medaCy.git
```
- Medacy Clinical Notes
```
pip install git+https://github.com/NLPatVCU/medaCy_model_clinical_notes.git
```

### MedSpaCy -Requirements
- [MedSpaCy](https://github.com/medspacy/medspacy "MedSpaCy") 0.1.0.1
```
pip install medspacy
```
- SpaCy 2.3.2
```
pip install spacy==2.3.2
```
- PyRuSH
```
pip install PyRush
```
- Model for MedSpaCy
```
pip install pip install https://github.com/abchapman93/spacy_models/raw/master/releases/en_info_3700_i2b2_2012-0.1.0/dist/en_info_3700_i2b2_2012-0.1.0.tar.gz
```

### SciSpaCy -Requirements
- [SciSpaCy](https://github.com/allenai/scispacy "MedSpaCy") 0.3.0
```
pip install scispacy==0.3.0
```
- SpaCy 2.3.2
```
pip install spacy==2.3.2
```
- En_core_sci_lg Model
```
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.3.0/en_core_sci_lg-0.3.0.tar.gz
```


## Instructions - How to use the scripts

All the three tagger scripts requires a TSV file as argument. Such TSV file consists of a dataset of tweets with a specific structure. Some examples can be found [here](https://github.com/thepanacealab/covid19_twitter "here"). It is important that the TSV file **should not** include any headers.

### MedaCy - Using the *medacy_tagger.py* script

The way to use the script is as follows (in which the *filename.tsv*  is the TSV file mentioned before):
```
python medacy_tagger.py "filename.tsv"
```
This will generate two files as output:

- *filename_medacy_annotations.tsv* : A TSV files with the following columns:
	- **Tweet Id**
	- **Text_section: ** Part of the tweet's text in which a match was found.
	- **Span_start: ** Start position in which the match was found in the tweet's text.
	- **Span_end: ** End position in which the match was found in the tweet's text.
	- **Annotation_type: ** Matched concept extracted from the model.
	- **Extras: ** Only used if additional information is provided.

- *filename_medacy_tweets_tagged_tsv*:  A TSV file including only those tweets in which at least one match was found. The TSV file includes the following columns: **Tweet_id** and **Tweet_full_text**.


### MedsPaCy - Using the *medspacy_tagger.py* script

The way to use the script is as follows (in which the *filename.tsv*  is the TSV file mentioned before):
```
python medspacy_tagger.py "filename.tsv"
```
This will generate two files as output:

- *filename_medacy_annotations.tsv* : A TSV files with the following columns:
	- **Tweet Id**
	- **Text_section: ** Part of the tweet's text in which a match was found.
	- **Span_start: ** Start position in which the match was found in the tweet's text.
	- **Span_end: ** End position in which the match was found in the tweet's text.
	- **Annotation_type: ** Matched concept extracted from the model provided to medSpaCy.
	- **Extras: ** Only used if additional information is provided.

- *filename_medspacy_tweets_tagged_tsv*:  A TSV file including only those tweets in which at least one match was found. The TSV file includes the following columns: **Tweet_id** and **Tweet_full_text**.

### ScisPaCy - Using the *scispacy_tagger.py* script

The way to use the script is as follows (in which the *filename.tsv*  is the TSV file mentioned before):
```
python scispacy_tagger.py "filename.tsv"
```
This will generate two files as output:

- *filename_scispacy_annotations.tsv* : A TSV files with the following columns:
	- **Tweet Id**
	- **Text_section: ** Part of the tweet's text in which a match was found.
	- **Span_start: ** Start position in which the match was found in the tweet's text.
	- **Span_end: ** End position in which the match was found in the tweet's text.
	- **Annotation_type: ** Matched concept extracted from the model provided to sciSpaCy (en_core_sci_lg Model) an linked with UMLS.
	- **Extras: ** Only used if additional information is provided.

- *filename_scispacy_tweets_tagged_tsv*:  A TSV file including only those tweets in which at least one match was found. The TSV file includes the following columns: **Tweet_id** and **Tweet_full_text**.

### Using the *annotation_evaluation.py* script

The following script will count all matches found per tweet and per tagger, also it will count all overlaps presented between these three taggers. The way to execute the code is as follows:
```
python scispacy_tagger.py "filename_medacy_annotations.tsv" "filename_medspacy_annotations.tsv" "filename_scispacy_annotations.tsv"
```
It is important that the order of the arguments should be in the following way:
- The generated annotation TSV file from **medaCy**
- The generated annotation TSV file from **medSpaCy**
- The generated annotation TSV file from **sciSpaCy**

The output will result in a single TSV file (named *annotation_evaluation.tsv*) with the following columns:
- Tweet_Id
- **Tags_medacy:** Number of matches found in a specific tweet using medaCy.
- **Tags_medspacy:** Number of matches found in a specific tweet using medSpaCy.
- **Tags_scispacy:** Number of matches found in a specific tweet using sciSpaCy.
- **Overlap_medacy_medspacy**: Number of matches in which both taggers annotated the same positions from a tweet's text in a specific tweet.
- **Overlap_medacy_scispacy**: Number of matches in which both taggers annotated the same positions from a tweet's text in a specific tweet.
- **Overlap_medspacy_scispacy**: Number of matches in which both taggers annotated the same positions from a tweet's text in a specific tweet.
