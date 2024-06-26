# LIBRARIES
import os
import plotly.offline as pyo
import plotly.graph_objects as go
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
import plotly.io as pio
import plotly.express as px
import numpy as np

# SCRIPTS
import parameters

def getAnalysisInputs():
    df = parameters.DATASET["combined_inputs"]
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    X.head()
    df_cat = df.select_dtypes(exclude=[np.number])
    feature_names = list(X.columns)
    ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1, 2, 3])], remainder='passthrough')
    X = ct.fit_transform(X).toarray()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)
    sc = StandardScaler()
    X_train[:, 18:] = sc.fit_transform(X_train[:, 18:])
    X_test[:, 18:] = sc.transform(X_test[:, 18:])
    model_performance = pd.DataFrame(columns=['Accuracy', 'Recall', 'Precision', 'F1-Score', 'time to train', 'time to predict', 'total time'])

    return X_train, X_test, y_train, y_test, model_performance, feature_names

def getOutputName():
    return f"/{parameters.OUTPUT_FOLDER}/{parameters.OUTPUT_NAME}_{parameters.DATASET['name']}.html"

def plotFeatures(df_scores, df_col):
    
    # Configure display options
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.expand_frame_repr', False)

    # Configure plotly templates
    pio.templates["ck_template"] = go.layout.Template(
        layout_colorway=px.colors.sequential.Viridis,
        layout_autosize=False,
        layout_width=800,
        layout_height=600,
        layout_font=dict(family="Calibri Light"),
        layout_title_font=dict(family="Calibri"),
        layout_hoverlabel_font=dict(family="Calibri Light"),
    )
    pio.templates.default = 'ck_template+gridon'

    feature_score=pd.concat([df_col,df_scores],axis=1)
    feature_score.columns=['feature','score']
    feature_score.sort_values(by=['score'],ascending=True,inplace=True)

    fig = go.Figure(go.Bar(
                x=feature_score['score'][0:(parameters.SHOW_FEATURE_COUNT)],
                y=feature_score['feature'][0:(parameters.SHOW_FEATURE_COUNT)],
                orientation='h'))

    fig.update_layout(title=f"Top {parameters.SHOW_FEATURE_COUNT} Features",
                    height=1200,
                    showlegend=False,
                    )
    
    # Concatenate to form the absolute path to save the plot
    pyo.plot(fig, filename=os.getcwd()+getOutputName())
