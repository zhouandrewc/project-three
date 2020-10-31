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

We do not include the data in this repository due to its size. We include one example within the [```data/processing```](data/processing) folder at [```data/processing/wlth2001```](data/processing/wlth2001).

Note that the data acquisition, parsing, and cleaning processing is rather complicated given the nature of the survey and datasets. Find a detailed documentation of the workflow in the [```data/processing``` README](data/processing/README.md)



## Contents

* [Data](data)



* [Utilities](util)

Utility functions for Jupyter notebooks. Includes separate files for parsing and cleaning data, model selection, and model evaluation.

* [Notebooks](notebooks)

Notebooks for inserting data into sql, cleaning data, and our final modeling and evaluation.

* [Site](site)

The Streamlit/Flask/d3 app I created to demonstrate predictions and allow data exploration.

* [Presentation](project-three-slides.pdf)

The presentation I gave on my work.

## Acknowledgments

Thanks to the awesome staff and students at Metis who were a huge help during this project.