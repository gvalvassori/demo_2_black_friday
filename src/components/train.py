from kfp.dsl import Dataset, Output, component, Model, Metrics, Input

@component(
    packages_to_install=[
        "pandas==2.2.2",        
        "scikit-learn==1.4.2",
        "scipy==1.13.0",
        "xgboost==2.0.3"
    ],
    base_image="python:3.10"
)
def train_model(
    dataset_train: Input[Dataset],
    model: Output[Model],
    metrics: Output[Metrics],
):
    """Training XGBoost Regressor model for demo-2-black-friday.

    Args:
        dataset_train: The training dataset.

    Returns:
        model: The model artifact stores the model.joblib file.
        metrics: The metrics of the trained model.
    """
    
    import pandas as pd
    import numpy as np
    import time, os, joblib
    from sklearn.model_selection import RandomizedSearchCV, train_test_split
    from sklearn.metrics import r2_score, mean_squared_error
    from sklearn.preprocessing import OrdinalEncoder, StandardScaler
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from xgboost import XGBRegressor
    
    with open(dataset_train.path + '.csv', "r") as train_data:
        dataset = pd.read_csv(train_data)
        
    X = dataset.drop("Purchase", axis = 1)
    Y = dataset["Purchase"]
    
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42)
    
    preprocessor = ColumnTransformer(transformers=[
        ('cat', OrdinalEncoder(), ['Age'])],
    )
    
    max_depth = [int(x) for x in np.linspace(start = 5, stop = 20, num = 15)]
    learning_rate = ['0.01', '0.05', '0.1', '0.25', '0.5', '0.75', '1.0']
    min_child_weight = [int(x) for x in np.linspace(start = 45, stop = 70, num = 15)]
    
    params = {
     "regressor__learning_rate"    : learning_rate,
     "regressor__max_depth"        : max_depth,
     "regressor__min_child_weight" : min_child_weight,
     "regressor__gamma"            : [0.0, 0.1, 0.2 , 0.3, 0.4],
     "regressor__colsample_bytree" : [0.3, 0.4, 0.5 , 0.7]
    }
    
    xgb = XGBRegressor(verbosity = 0, random_state = 42)
       
    regr = Pipeline([
        ('preprocessor', preprocessor),
        ('standard-scaler', StandardScaler()),
        ('regressor', xgb)
    ])
    
    xgb_cv = RandomizedSearchCV(regr, param_distributions = params, cv = 5, random_state = 42)
    
    xgb_cv.fit(X_train, Y_train)
      
    xgb_best = xgb_cv.best_estimator_
    
    Y_pred_xgb_best = xgb_best.predict(X_test)
    
    r2 = r2_score(Y_test, Y_pred_xgb_best)
    rmse = np.sqrt(mean_squared_error(Y_test, Y_pred_xgb_best))
    
    metrics.log_metric("Framework", "XGBoost")
    metrics.log_metric("Train_samples_size", len(X_train))
    metrics.log_metric("Validation_samples_size", len(X_test))
    metrics.log_metric("RMSE", round(rmse,2))
    metrics.log_metric("R2 score", round(r2,2))
    
    print("XGB regression:")
    print("RMSE:",rmse)
    print("R2 score:", r2)
    
    # Export the model to a file
    os.makedirs(model.path, exist_ok=True)
    joblib.dump(regr, os.path.join(model.path, "model.joblib"))
    