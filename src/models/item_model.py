from pydantic import BaseModel


class Item(BaseModel):
    CRIM: float
    ZN: float
    INDUS: float
    CHAS: int
    NOX: float
    RM: float
    AGE: float
    DIS: float
    RAD: int
    TAX: float
    PTRATIO: float
    B: float
    LSTAT: float

    class Config:
        schema_extra = {
            'example': {
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
        }
