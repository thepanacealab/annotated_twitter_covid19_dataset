## A biomedically oriented automatically annotated Twitter COVID-19 Dataset

![TwitterDataset](http://www.panacealab.org/covid19/tweets_plot.png)

### Authors: [Luis Alberto Robles Hernandez](https://github.com/LuisRobles18), [Tiffany Callahan](http://tiffanycallahan.com/) and [Juan M. Banda](http://www.jmbanda.com/)

The use of social media data, like Twitter, for biomedical research has been gradually increasing over the years. With the COVID-19 pandemic, researchers have turned to more non-traditional sources of clinical data to characterize the disease in near-real time, study the societal implications of interventions, as well as the sequelae that recovered COVID-19 cases present (Long-). However, manually curated social media datasets are difficult to come by due to the expensive costs of manual annotation and the efforts needed to identify the correct texts. When datasets are available, they are usually very small and their annotations don’t generalize well over time or to larger sets of documents. As part of the 2021 Biomedical Linked Annotation Hackathon, we release our dataset of over 120 million automatically annotated tweets for biomedical research purposes. Incorporating best-practices, we identify tweets with potentially high clinical relevance. We evaluated our work by comparing several SpaCy-based annotation frameworks against a manually annotated gold-standard dataset. Selecting the best method to use for automatic annotation, we then annotated 120 million tweets and released them publicly for future downstream usage within the biomedical domain.

Some of the components of this project have been worked on during the [COVID-19 Biohackathon](https://github.com/thepanacealab/covid19_biohackathon) and published at the [EMNLP NLP COVID-19 Workshop - Part 2](http://dx.doi.org/10.18653/v1/2020.nlpcovid19-2.25).

Dataset details:

The file columns are: Tweet_id, annotation_concept_id, annotationStart, annotationEnd

In order to use this resource, the annotation_concept_id column needs to be joined with the The [Observational Health Data Sciences and Informatics Vocabulary](https://athena.ohdsi.org/). 

We used a subset of all available vocabularies which included (version next to the name):
- ICD9CM - ICD9CM v32 master descriptions
- ICD10PCS - ICD10PCS 2021
- CPT4 - 2020 Release
- NDFRT - RXNORM 2018-08-12
- HCPCS - 2020 Alpha Numeric HCPCS File
- MeSH - 2020 Release
- ICD10 - 2020 Release
- ICD9Proc - ICD9CM v32 master descriptions
- ICD10CM - ICD10CM FY2021 code descriptions
- RxNorm - RxNorm 20210104
- RxNorm Extension - RxNorm Extension 2021-02-12
- SNOMED - 2020-07-31 SNOMED CT International Edition; 2020-09-01 SNOMED CT US Edition; 2020-10-28 SNOMED CT UK Edition

NOTE: The full text of the tweet cannot be shared, but each individual tweet can be hydrated back to get all data elements. 

Dataset available at: https://doi.org/10.5281/zenodo.4606733

Dataset publication available at: 

