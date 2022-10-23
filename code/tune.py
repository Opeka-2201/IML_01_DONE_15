"""
University of Liege
ELEN0062 - Introduction to machine learning
Project 1 - Classification algorithms
"""
#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from data import make_dataset2
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

def tune_knn(X_train, y_train):
    """
    Tune the hyperparameters of the KNN classifier
    """

    param_grid = {'n_neighbors': [1, 5, 25, 125, 625]}
    knn = KNeighborsClassifier()
    grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_, grid_search.best_params_

def tune_decision_tree(X_train, y_train):
    """
    Tune the hyperparameters of the decision tree classifier
    """

    param_grid = {'max_depth': [1, 2, 4, 8, None]}
    tree = DecisionTreeClassifier()
    grid_search = GridSearchCV(tree, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_, grid_search.best_params_


if __name__ == '__main__':
    n_samples = 1500
    n_fit = 1200
    n_tests = 5
    results = np.zeros((n_tests, 2))

    for i in range(n_tests):
        n_samples = 1500
        n_fit = 1200
        X, y = make_dataset2(n_samples)
        X_train, y_train = X[:n_fit], y[:n_fit]
        X_test, y_test = X[n_fit:], y[n_fit:]

        knn, params = tune_knn(X_train, y_train)
        results[i, 0] = params['n_neighbors']

        tree, params = tune_decision_tree(X_train, y_train)
        results[i, 1] = params['max_depth']

    best_knn = np.bincount(results[:, 0].astype(int)).argmax()
    best_tree = np.bincount(results[:, 1].astype(int)).argmax()

    print('Best hyperparameters:')
    print('KNN: {}'.format(best_knn))
    print('Decision tree: {}'.format(best_tree))

    results = np.zeros((n_tests, 2))

    for i in range(n_tests):
        X, y = make_dataset2(n_samples)
        X_train, y_train = X[:n_fit], y[:n_fit]
        X_test, y_test = X[n_fit:], y[n_fit:]

        knn = KNeighborsClassifier(n_neighbors=best_knn)
        knn.fit(X_train, y_train)
        results[i, 0] = knn.score(X_test, y_test)

        tree = DecisionTreeClassifier(max_depth=best_tree)
        tree.fit(X_train, y_train)
        results[i, 1] = tree.score(X_test, y_test)

    print("Accuracy with best hyperparameters:")
    print('    KNN: {}'.format(results[:, 0].mean()))
    print('    Decision tree: {}'.format(results[:, 1].mean()))
    print("Standard deviation with best hyperparameters:")
    print('    KNN: {}'.format(results[:, 0].std()))
    print('    Decision tree: {}'.format(results[:, 1].std()))
    
