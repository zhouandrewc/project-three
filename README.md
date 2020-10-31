# Metis Data Science Bootcamp Fall 2020 Project 3: Bachelor's Degree Prediction

This repository contains code, data, and documentation for Andrew Zhou's Bachelor's Degree Prediction project for the Metis Data Science Bootcamp.

## Problem Statement

We attempt to predict whether a person will graduate with a college degree given data from their youth.

## Methods

We train classification models, using the f<sub>0.5</sub>-score metric to evaluate performance for hyperparameter tuning and model selection.

### Tools Used

* pandas
* numpy
* sklearn
* imblearn
* Streamlit
* Flask
* d3
* PostgreSQL

### Techniques Used

* Logistic Regression
* Random Forest
* k Nearest Neighbors
* Support Vector Classifier
* AdaBoost
* Oversampling, SMOTE

### Data

Our data are from the [Panel Study of Income Dynamics](https://psidonline.isr.umich.edu/). We use data concerning individuals aged 6-17 in 2001 and attempt to predict whether they will have graduated with a bachelor's degree by 2017.

The data were originally formatted as ```.sps``` and ```.txt``` file pairs, meant for use with the [SPSS Statistics](https://en.wikipedia.org/wiki/SPSS) software.

We do not include the original data in this repository due to its size. The original data comprise 9 ```.sps``` and ```.txt``` pairs, each stored in the PSID data packages.

We include one example within the [```data/processing```](data/processing/) folder at [```data/processing/wlth2001```](data/processing/wlth2001/). The ```.sps``` file is left as is but the ```.txt``` file is blank.

Note that the data acquisition, parsing, and cleaning processing is rather complicated given the nature of the survey and datasets. Find a detailed documentation of the workflow in the [README](data/processing/README.md) in the [data/processing/](data/processing) folder.

Thank you to [hanjae112](https://github.com/hanjae1122) for the [PSID ASCII reader](https://github.com/hanjae1122/PSID), which I used to convert the PSID data into a pandas-readable format.

## Contents

* [Data and Data Processing Routines](data)
    * [```processing```](data/processing):
    The routines to convert the original PSID data into pandas-readable format.
    * [```csv```](data/csv):
    The ```.csv``` files that correspond to the original ```.sps``` files. Nine were created in total. One file, [```DEMOG.csv```](data/csv/DEMOG.csv), is left as an example, while others are omitted due to excessive size.
    * [```data.csv```](data/data.csv):
    The fully-processed data used for modeling and training.

* [Utilities](util)

Utility functions for Jupyter notebooks. Includes separate routines for parsing and cleaning data, model selection, and model evaluation.

* [Notebooks](notebooks)

Notebooks for inserting data into sql, cleaning data, and our final modeling and evaluation.

* [Application](site)

The Streamlit/Flask/d3 app I created to demonstrate predictions and allow data exploration.

* [Presentation](presentation)

Contains the [presentation](presentation/project-three-slides.pdf) I gave on my work.

## Acknowledgments

Thanks to the awesome staff and students at Metis who were a huge help during this project.