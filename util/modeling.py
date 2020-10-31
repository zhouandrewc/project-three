'''
# Helper functions for data preprocessing and modeling.
#
# Andrew Zhou
'''

import pandas as pd
import numpy as np
import sklearn
import pickle
import seaborn as sns
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import accuracy_score, f1_score, fbeta_score, precision_score, recall_score
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
from imblearn.over_sampling import SMOTE


def prepro_help(X, cont_transformer, cat_transformer, is_test=False):
    '''
    Helper function for preprocessing. Called twice in prepro, once to fit and
    transform the training data using the transformers, and again to transform
    the test data without fitting.
    '''
    if type(X) != pd.DataFrame:
        return None

    cont_feats = X.select_dtypes(include=['int64', 'float64']).columns
    cat_feats = X.select_dtypes(include=['object']).columns

    X_cont = X[cont_feats]
    X_cat = X[cat_feats]

    if not is_test:
        cont_transformer.fit(X_cont)
        cat_transformer.fit(X_cat)

    X_cont_transf = pd.DataFrame(cont_transformer.transform(X_cont), columns = X_cont.columns, index = X.index)
    X_cat_transf = pd.DataFrame(cat_transformer.transform(X_cat), columns = cat_transformer.named_steps["onehot"].get_feature_names(X_cat.columns), index = X_cat.index)

    X_prepro = pd.concat([X_cont_transf, X_cat_transf], axis=1)

    return X_prepro

def prepro(X_train, X_test=None, scale=False):
    '''
    Helper function for preprocessing. Imputes empty values, one hot encodes
    categorical variables, and optionally scales. If passed only a training set,
    fits and transforms the training set. If passed a test set as well, fits
    and transforms the training set and transforms the testing set based on the fit.
    '''
    cont_feats = X_train.select_dtypes(include=['int64', 'float64']).columns
    cat_feats = X_train.select_dtypes(include=['object']).columns

    cont_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])

    cat_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value=None)), ('onehot', OneHotEncoder(sparse=False, handle_unknown="ignore"))])
    cat_transformer = cat_transformer[0:2]

    if not scale:
        cont_transformer = cont_transformer[0]

    X_train_prepro = prepro_help(X_train, cont_transformer, cat_transformer)
    X_test_prepro = prepro_help(X_test, cont_transformer, cat_transformer, True)

    return X_train_prepro, X_test_prepro

def cross_val(model, X, y, weights, scale=False, sampler=None, cv=None):
    '''
    Cross validates a model. Returns a dictionary of accuracy, f1, f0.5 ("fp5"),
    precision, and recall scores.

    By default uses 5-fold stratified cross-validation.
    '''
    if not cv:
        cv =  StratifiedKFold(n_splits = 5, shuffle=True, random_state=0)

    acc_scores = []
    f1_scores = []
    fp5_scores = []
    pre_scores = []
    rec_scores = []

    scores = {}

    for train_idx, val_idx, in cv.split(X, y):

        X_tr, y_tr = X.iloc[train_idx,:], y.iloc[train_idx]

        X_v, y_v = X.iloc[val_idx,:], y.iloc[val_idx]

        acc, f1, fp5, pre, rec = single_val(model, X_tr, y_tr, X_v, y_v, weights, scale, sampler)

        acc_scores.append(acc)
        f1_scores.append(f1)
        fp5_scores.append(fp5)
        pre_scores.append(pre)
        rec_scores.append(rec)

    scores["acc"] = np.mean(acc_scores)
    scores["f1"] = np.mean(f1_scores)
    scores["fp5"] = np.mean(fp5_scores)
    scores["pre"] = np.mean(pre_scores)
    scores["rec"] = np.mean(rec_scores)

    return scores

def single_val(model, X_tr, y_tr, X_v, y_v, weights, scale=False, sampler=None):
    '''
    Helper function to validate a single time on a train and validation set.
    '''
    X_train_prepro, X_val_prepro = prepro(X_tr, X_v, scale=scale)

    sample_weights = weights[X_train_prepro.index]

    if sampler:
        X_and_weights_train_prepro = pd.concat([X_train_prepro, sample_weights], axis=1)
        X_and_weights_train_prepro, y_tr = sampler.fit_sample(X_and_weights_train_prepro, y_tr)
        X_train_prepro = X_and_weights_train_prepro.drop(labels="survey_weight", axis=1)
        sample_weights = X_and_weights_train_prepro["survey_weight"]

    if type(model) != KNeighborsClassifier:
        model.fit(X_train_prepro, y_tr, sample_weight=weights[X_train_prepro.index])
    else:
        model.fit(X_train_prepro, y_tr)
    y_pred = model.predict(X_val_prepro)

    return get_scores(y_v, y_pred, weights)


def get_scores(y_true, y_pred, weights):
    '''
    Given the true y and predicted y (and sample weights), get the evaluation
    metrics for the predictions.
    '''
    acc = accuracy_score(y_true, y_pred, sample_weight=weights[y_true.index])
    f1 = f1_score(y_true, y_pred, zero_division=0, sample_weight=weights[y_true.index])
    fp5 = fbeta_score(y_true, y_pred, beta=0.5, zero_division=0, sample_weight=weights[y_true.index])
    pre = precision_score(y_true, y_pred, zero_division=0, sample_weight=weights[y_true.index])
    rec = recall_score(y_true, y_pred, zero_division=0, sample_weight=weights[y_true.index])

    return acc, f1, fp5, pre, rec

def tune_hyper(X_tr, y_tr, model_class, keywords, param_grid, weights, randomized=True, scaling=[False], samplers=[None], print_prog=(0,0)):
    '''
    Given a cartesian product of different classifier parameters (param_grid),
    tests all possible combinations of those parameters for a specific model
    class model_class. Will also include scaling and sampling strategies in
    the tuning process.

    Returns a dictionary containing 5 different evaluation scores for each
    set of hyperparameters.
    '''
    scores = {}

    count = 0
    for params in param_grid:
        for sampler in samplers:
            for scale in scaling:
                count += 1
                if print_prog[0]:
                    if count % print_prog[0] == 0:
                        print("{} out of {} done".format(count, print_prog[1]))
                        print("params:", params, sampler)
                kwargs = dict(zip(keywords, params))
                if randomized:
                    kwargs["random_state"] = 0
                model = model_class(**kwargs)
                model_score = cross_val(model, X_tr, y_tr, weights, scale=scale, sampler=sampler)

                scores[params, sampler, scale] = model_score
    print("Done tuning")
    return scores

def get_best_params(scores, metric):
    '''
    Given the score matrix from tune_hyper, gets the best set of parameters
    for a given metric, such as "fp5".
    '''
    return sort_scores_by_metric(scores, metric)[0]

def print_best_params(best_params, keywords, metric=None):
    '''
    Given a set of best params for a particular metric and the keywords to
    which they correspond, prints the score for that param. Optionally pass the
    name of the metric for printing clarity.
    '''
    params = best_params[0][0]
    sampler = best_params[0][1]
    scaling = best_params[0][2]
    score = best_params[1]

    print("Classifier Params:", list(zip(keywords, params)))
    print("Sampler:", sampler)
    print("Scaling:", scaling)
    print(metric, "Score (CV):", score)

def get_scores_by_metric(scores, metric):
    '''
    Get only the scores for a particular metric ("f1", "fp5", "acc", "pre,"
    "rec")
    '''
    params = scores.keys()
    metric_scores = map(lambda x: x[metric], scores.values())
    return list(zip(params, metric_scores))

def sort_scores_by_metric(scores, metric):
    '''
    Get the sorted scores for a particular metric.
    '''
    return sorted(get_scores_by_metric(scores, metric), key=lambda x: -x[1])

def train_best_model(X_tr, y_tr, model_class, keywords, scores, metric, weights, randomized=True):
    '''
    Given the best params found through hyperparameter tuning for a particular
    model and metric, trains the best model using those parameters.
    '''
    best_params = get_best_params(scores, metric)
    clf_params, sampler, scale = best_params[0]

    return train_model(X_tr, y_tr, model_class, keywords, clf_params, sampler, scale, weights=weights, randomized=randomized)

def train_model(X_tr, y_tr, model_class, keywords, params, sampler, scale, weights, randomized=True):
    '''
    Trains a model given a set of parameters.
    '''
    X_tr, _ = prepro(X_tr, scale=scale)
    if sampler:
        X_tr, y_tr = sampler.fit_sample(X_tr, y_tr)

    kwargs = dict(zip(keywords, params))
    if randomized:
        kwargs["random_state"] = 0
    model = model_class(**kwargs)
    if model_class == KNeighborsClassifier:
        model.fit(X_tr, y_tr)
    else:
        model.fit(X_tr, y_tr, sample_weight=weights[X_tr.index])


    return model
