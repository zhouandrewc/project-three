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
    cont_feats = X_train.select_dtypes(include=['int64', 'float64']).columns
    cat_feats = X_train.select_dtypes(include=['object']).columns

    cont_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])

    cat_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value=None)), ('onehot', OneHotEncoder(sparse=False, handle_unknown="ignore"))])#, ('scaler', StandardScaler())])
    cat_transformer = cat_transformer[0:2]
    if not scale:
        cont_transformer = cont_transformer[0]

    X_train_prepro = prepro_help(X_train, cont_transformer, cat_transformer)
    X_test_prepro = prepro_help(X_test, cont_transformer, cat_transformer, True)

    return X_train_prepro, X_test_prepro

# take out a single loop into a score function? for RF where cv isn't necessary
# pass in a dict key

def cross_val(model, X, y, weights, scale=False, sampler=None, cv=None):
    if not cv:
        cv =  StratifiedKFold(n_splits = 5, shuffle=True, random_state=0)

    acc_scores = []
    f1_scores = []
    fp5_scores = []
    pre_scores = []
    rec_scores = []

    scores = {}

    # oversample?
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

    X_train_prepro, X_val_prepro = prepro(X_tr, X_v, scale=scale)

    sample_weights = weights[X_train_prepro.index]
    # get weights working with this
    if sampler:
        X_and_weights_train_prepro = pd.concat([X_train_prepro, sample_weights], axis=1)
        X_and_weights_train_prepro, y_tr = sampler.fit_sample(X_and_weights_train_prepro, y_tr)
        X_train_prepro = X_and_weights_train_prepro.drop(labels="survey_weight", axis=1)
        sample_weights = X_and_weights_train_prepro["survey_weight"]

    if type(model) == XGBClassifier:
        eval_set = [(X_train_prepro, y_tr), (X_val_prepro, y_v)]
        model.fit(X_train_prepro, y_tr, eval_set=eval_set, early_stopping_rounds=10, verbose=False)
    else:

        if type(model) != KNeighborsClassifier:
            model.fit(X_train_prepro, y_tr, sample_weight=weights[X_train_prepro.index])
        else:
            model.fit(X_train_prepro, y_tr)
    y_pred = model.predict(X_val_prepro)

    return get_scores(y_v, y_pred, weights)

# want to weight the scores too probably
def get_scores(y_true, y_pred, weights):
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, zero_division=0, sample_weight=weights[y_true.index])
    fp5 = fbeta_score(y_true, y_pred, beta=0.5, zero_division=0, sample_weight=weights[y_true.index])
    pre = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)

    return acc, f1, fp5, pre, rec

def tune_hyper(X_tr, y_tr, model_class, keywords, param_grid, weights, randomized=True, scaling=[False], samplers=[None], print_prog=(0,0)):
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
    return sort_scores_by_metric(scores, metric)[0]

def get_scores_by_metric(scores, metric):
    params = scores.keys()
    metric_scores = map(lambda x: x[metric], scores.values())
    return list(zip(params, metric_scores))

def sort_scores_by_metric(scores, metric):
    return sorted(get_scores_by_metric(scores, metric), key=lambda x: -x[1])

# refactor to make train its separate function
def train_best_model(X_tr, y_tr, model_class, keywords, scores, metric, weights, randomized=True):
    best_params = get_best_params(scores, metric)
    clf_params, sampler, scale = best_params[0]

    return train_model(X_tr, y_tr, model_class, keywords, clf_params, sampler, scale, weights=weights, randomized=randomized)

def train_model(X_tr, y_tr, model_class, keywords, params, sampler, scale, weights, randomized=True):
    X_tr, _ = prepro(X_tr, scale=scale)
    if sampler:
        X_tr, y_tr = sampler.fit_sample(X_tr, y_tr)

    kwargs = dict(zip(keywords, params))
    if randomized:
        kwargs["random_state"] = 0
    model = model_class(**kwargs)
    if model_class == XGBClassifier:
        model.fit(X_tr, y_tr, verbose=False)#, eval_set=[(X_tr, y_tr)], early_stopping_rounds=10, verbose=False)
    elif model_class == KNeighborsClassifier:
        model.fit(X_tr, y_tr)
    else:
        model.fit(X_tr, y_tr, sample_weight=weights[X_tr.index])


    return model
