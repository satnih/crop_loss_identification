#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 13:37:32 2020
@author: hiremas1
Optimize classifiers using data from year 2015
"""
import pandas as pd
import config as cfg
import utils_ml as mut
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV

result_path = cfg.result_base_path + "optimise/"
data_path = cfg.data_path + cfg.filename
x, y, _ = mut.load_ndvi_as_numpy(data_path, mut.as_list(2015), 1)
df = pd.DataFrame([])
for model_name in ['rf']:
    for imputer_name in ['meanind']:
        print()
        print([model_name, imputer_name], end=',')
        for i, random_state in enumerate(cfg.random_states):
            print(random_state, end=', ')
            sss = StratifiedShuffleSplit(n_splits=cfg.cv,
                                         train_size=cfg.train_size,
                                         random_state=random_state)

            clf = mut.build_model(model_name, imputer_name, random_state)
            param_grid = mut.create_param_grid(model_name)
            grid_results = GridSearchCV(clf,
                                        param_grid=param_grid,
                                        scoring="roc_auc",
                                        cv=sss,
                                        verbose=0)
            grid_results.fit(x, y)
            dfi = pd.DataFrame(grid_results.cv_results_)
            dfi['seed'] = random_state
            if i == 0:
                df = dfi
            else:
                df = df.append(dfi, ignore_index=True)
            print(df)
        if 0:
            csvname = f"{model_name}_{imputer_name}_10x10_auc.csv"
            df.to_csv(result_path + csvname, index=False)
