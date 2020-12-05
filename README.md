## Biomedically oriented automatically annotated Twitter COVID-19 Dataset

![TwitterDataset](http://www.panacealab.org/covid19/tweets_plot.png)

Taking advantage of having in-house [one of the largest Twitter COVID-19 chatter datasets](https://doi.org/10.5281/zenodo.3723939), in this project we will incorporate current best-practices and novel approaches to:
1. Tweet attribution.
2. Bot and Spam removal.
3. Misspelling and colloquialism handling.

Thus cleaning Twitter data, in order to potentially identify Tweets with self-reported symptoms/drug usage with clinical characterization relevance. Some of the components of this project have been worked on during the [COVID-19 Biohackathon](https://github.com/thepanacealab/covid19_biohackathon) and published at the [EMNLP NLP COVID-19 Workshop - Part 2](http://dx.doi.org/10.18653/v1/2020.nlpcovid19-2.25).

Deliverables:

The product of this project would be an automatically annotated dataset on all English Tweets. We are looking for additional participans if they want to provide software to automatically annotate any other language tweets, as the dataset has [68 other languages available](http://www.panacealab.org/covid19/). We try evaluate multiple annotation strategies, from basic text tagging to using NER systems with specialized models trained for the identification of biomedical/medical entities like: [medaCy](https://github.com/NLPatVCU/medaCy), [medSpacy](https://github.com/medspacy/medspacy) and [SciSpacy](https://allenai.github.io/scispacy/). 
We will release all tweet identifiers with all annotations made for the languages generated. We will use and expand the tools available in the Social Media Mining Toolkit (SMMT) developed during BLAH6 for this task, and will provide all annotations in brat and PubAnnotation formats.

For evaluation, we have a manually annotated set that we will be using for a SMM4H 2021  shared task that we can use for evaluation of the proposed approach.

Bigger picture:
Our aim with this project is to create build additional pieces to create a framework to pre-process Twitter data to extract clinical insights in a, preferably, automated way. This will add in generating larges annotated datasets, ideally not only for COVID-19 applications in the future.  

Team Members: [Juan M. Banda](http://www.jmbanda.com/) and [Tiffany Callahan](http://tiffanycallahan.com/)
