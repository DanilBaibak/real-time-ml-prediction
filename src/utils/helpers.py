import pandas as pd

from utils.utils import execute_query
from models.item_model import Item


def get_latest_ml_pipeline_version() -> str:
    """Get the latest version of the pipeline from the DB."""

    return execute_query('''
        SELECT pipeline_version
        FROM ml_pipeline
        ORDER BY created_at DESC
        LIMIT 1
    ''')[0][0]


def save_ml_pipeline_version(model_version: str) -> None:
    """Save the new version of the pipeline to the DB."""
    execute_query('INSERT INTO ml_pipeline (pipeline_version) VALUES(%s)', (model_version,))


async def save_prediction(row: list) -> None:
    """Save features + prediction + pipeline version."""
    query = '''
INSERT INTO predictions (
crim, zn, indus, chas, nox, rm, age, dis, rad, tax, ptratio, b, lstat, prediction, pipeline_version
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    execute_query(query, row)


def convert_item_to_df(item: Item) -> pd.DataFrame:
    """Convert Item to the pandas DataFrame"""
    items = {}
    for key, value in item.dict().items():
        items[key] = [value]

    return pd.DataFrame(items)


async def check_db_availability():
    return execute_query("SELECT 1 from pg_database WHERE datname='rest_ml'")
