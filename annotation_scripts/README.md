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
### MedaCy - Using the *medacy_tagger.py* script


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
### MedSpaCy - Using the *medspacy_tagger.py* script


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

### SciSpacy - Using the *scispacy_tagger.py* script


### SciSpacy - Using the *annotation_evaluation.py* script
