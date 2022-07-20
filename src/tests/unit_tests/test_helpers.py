import pytest
import pandas as pd
from utils.helpers import convert_item_to_df
from models.item_model import Item

@pytest.mark.asyncio
async def test_convert_item_to_df():
    item = Item(
        CRIM=0.00632, ZN=18.0, INDUS=2.31, CHAS=0, NOX=0.538, RM=6.575, AGE=65.2, 
        DIS=4.09, RAD=1, TAX=296.0, PTRATIO=15.3, B=396.9, LSTAT=4.98
    )

    converted_item = await convert_item_to_df(item)
    expected = {
        'CRIM': 0.00632,
        'ZN': 18.0,
        'INDUS': 2.31,
        'CHAS': 0,
        'NOX': 0.538,
        'RM': 6.575,
        'AGE': 65.2,
        'DIS': 4.09,
        'RAD': 1,
        'TAX': 296.0,
        'PTRATIO': 15.3,
        'B': 396.9,
        'LSTAT': 4.98
    }

    assert type(converted_item) == pd.DataFrame

    for key, val in expected.items():
        assert converted_item[key][0] == val
