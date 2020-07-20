import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ipywidgets import widgets, fixed

def plot_scores(df, scores, std_scores):
    data = pd.DataFrame({
        'Supplier': ['S_{}'.format(supplier) for supplier in list(df['supplier'])],
        'Score': scores
    })
    
    std_data = pd.DataFrame({
        'Supplier': ['S_{}'.format(supplier) for supplier in list(df['supplier'])],
        'Standarized Score': std_scores
    })
    
    
    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, figsize=(20, 6))
    sns.barplot(x='Supplier', y='Score', data=data, color='royalblue', saturation=.5, ax=ax1).set_title("Supplier Score")
    sns.barplot(x='Supplier', y='Standarized Score', data=std_data, color='lightcoral', saturation=.5, ax=ax2).set_title("Standarized Supplier Score")
    
def get_kwargs(df):
    performance_cols = df.columns.to_list()
    performance_cols.remove('supplier')
    dict_sliders = {}
    for col in performance_cols:
            dict_sliders[col] = widgets.FloatSlider(min=0.0, max=100.0, step=1.0, value=50.0, description=col.upper().replace('_', ' '))
    
    kwargs = {'{}'.format(key):dict_sliders[key] for key in dict_sliders.keys()}

    kwargs['data'] = fixed(df)
   
    return kwargs

def benchmark_suppliers(**kwargs):
    suppliers = kwargs['data']
    del kwargs['data']

    performance_cols = suppliers.columns.to_list()
    performance_cols.remove('supplier')
    stats = suppliers[performance_cols].describe().loc[['mean', 'std'],:]

    weights = [value for arg, value in enumerate(kwargs.values())]
    relative_importance = weights / np.sum(weights)

    scores = []
    std_scores = []
    for row in range(len(suppliers)):
        row_score = []
        std_row_score = []
        for col in performance_cols:
            # Score calculation
            row_col_score = suppliers.loc[row, col] / stats.loc['mean', col] * relative_importance[performance_cols.index(col)]
            row_score.append(row_col_score)
            # Standarized score calculation
            std_row_col_score = (suppliers.loc[row, col] - stats.loc['mean', col]) / stats.loc['std', col] * relative_importance[performance_cols.index(col)]
            std_row_score.append(std_row_col_score)
        
        scores.append(np.sum(row_score))
        std_scores.append(np.sum(std_row_score))

    plot_scores(suppliers, scores, std_scores)  