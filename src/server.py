import os
import logging.config
from joblib import load
from typing import Dict, Any

from fastapi import FastAPI, status, Response
from fastapi.responses import JSONResponse

from utils.helpers import get_latest_ml_pipeline_version, convert_item_to_df, save_prediction, check_db_availability
from models.item_model import Item
from scripts.training import ML_PIPELINES_PATH


logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logger.propagate = False

ENV_LOCAL = 'local'
ENV_LIVE = 'live'

CACHE: Dict[str, Any] = {}

# enable documentation for specific environment only
docs_url = '/docs' if os.getenv('ENV') == ENV_LOCAL else None
app = FastAPI(docs_url=docs_url)


@app.get('/health')
async def health_check():
    content = {'Server status': 'Ok', 'DB connection': 'Ok'}

    # check DB connection
    try:
        is_db_available = await check_db_availability()
        if len(is_db_available) == 0:
            content['DB connection'] = 'DB unavailable'
    except Exception:
        content['DB connection'] = 'DB unavailable'
        return JSONResponse(content=content)

    # check the latest ML pipeline version
    try:
        ml_pipeline_version = get_latest_ml_pipeline_version()

        # check if the ML pipeline exists
        if os.path.isfile(os.path.join(ML_PIPELINES_PATH, f'pipeline_{ml_pipeline_version}.pickle')):
            content['ML pipeline'] = 'Ok' if os.getenv('ENV') == ENV_LIVE else ml_pipeline_version
        else:
            content['ML pipeline'] = 'ML pipeline unavailable'
    except Exception:
        content['ML pipeline'] = 'ML pipeline unavailable'

    return JSONResponse(content=content)


@app.post('/predict')
async def predict(item: Item, response: Response):
    pipeline_version = get_latest_ml_pipeline_version()

    # check if we have the latest ml pipeline in the cache. Otherwise, load and cache the newest.
    if CACHE.get('ml_pipeline_version', None) != pipeline_version:
        try:
            ml_pipeline = load(os.path.join(ML_PIPELINES_PATH, f'pipeline_{pipeline_version}.pickle'))

            # cache new ml pipeline and ml pipeline version.
            CACHE['ml_pipeline'] = ml_pipeline
            CACHE['ml_pipeline_version'] = pipeline_version
        except FileNotFoundError:
            logger.error(f'The ML pipeline version "{pipeline_version}" does not exist.')

            response.status_code = status.HTTP_404_NOT_FOUND
            return JSONResponse(content={'Status': 'The model was not found.'},
                                status_code=status.HTTP_404_NOT_FOUND)

    # make prediction
    df = await convert_item_to_df(item)
    prediction = CACHE['ml_pipeline'].predict(df)[0]

    # save features + prediction + pipeline version
    await save_prediction(df.values.tolist()[0] + [prediction, pipeline_version])

    return JSONResponse(content={'prediction': prediction})
