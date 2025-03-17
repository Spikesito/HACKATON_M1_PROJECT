from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def Preprocess(features_model, X, fit=True, preprocessor=None):
    categorical_features = ['Education', 'Marital_Status']
    numeric_features = list(set(features_model) - set(categorical_features))

    if fit:
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(), categorical_features)
            ])
        X_preprocessed = preprocessor.fit_transform(X)
    else:
        X_preprocessed = preprocessor.transform(X)

    return X_preprocessed, preprocessor
