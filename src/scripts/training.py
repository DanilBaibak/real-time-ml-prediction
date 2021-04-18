import numpy as np
import pandas as pd
from os import path
import logging.config
from datetime import datetime
from joblib import dump

from sklearn.datasets import load_boston
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import Ridge

from utils.helpers import save_ml_pipeline_version

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


SEED = 42
np.random.seed(SEED)

ML_PIPELINES_PATH = 'ml_pipelines/'


def train() -> Pipeline:
    """An example of a training part for a ML pipeline."""
    # get data
    df, y = get_data()
    features_categorical = ['CHAS', 'RAD']
    features_numerical = ['INDUS', 'TAX', 'RM', 'CRIM', 'DIS', 'PTRATIO', 'LSTAT', 'AGE', 'ZN', 'B', 'NOX']
    logger.info(f'Training data: {df.shape}.')

    # build pipeline
    pipeline = build_pipeline(features_numerical, features_categorical)
    logger.info('The ML pipeline was built.')

    # train pipeline
    pipeline.fit(df, y)
    logger.info('New model trained.')

    return pipeline


def get_data():
    """Load training data."""
    boston = load_boston()
    X, y, features = boston.data, boston.target, boston.feature_names
    df = pd.DataFrame(data=X, columns=features)

    return df, y


def build_pipeline(features_numerical: list, features_categorical: list) -> Pipeline:
    """Build a ML pipeline."""
    transformer_numerical = StandardScaler()
    transformer_categorical = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(transformers=[('scaler', transformer_numerical, features_numerical),
                                                   ('ohe', transformer_categorical, features_categorical)])

    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('regressor', Ridge(random_state=SEED))])

    return pipeline


if __name__ == '__main__':
    pipeline = train()

    new_version = datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
    dump(pipeline, path.join(ML_PIPELINES_PATH, f'pipeline_{new_version}.pickle'))
    logger.info(f'The new pipeline "{new_version}" was successfully saved.')

    save_ml_pipeline_version(new_version)
