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

### Techniques Used

* Logistic Regression
* Random Forest
* k Nearest Neighbors
* Support Vector Classifier
* AdaBoost
* Oversampling, SMOTE

### Data

Our data are from the [Panel Study of Income Dynamics](https://psidonline.isr.umich.edu/). We use data concerning individuals aged 6-17 in 2001 and attempt to predict whether they will have graduated with a bachelor's degree by 2017.

## Contents

* [Utilities](util)

Utility functions

* [Notebooks]

Notebooks for inserting data into sql, cleaning data, and modeling.

* [Presentation](project-three-slides.pdf)

The presentation I gave on my work.

## Acknowledgments

Thanks to the awesome staff and students at Metis who were a huge help during this project.