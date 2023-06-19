import datetime
import pandas as pd
from pydantic import BaseModel

from .schema import EmployeeCSV

def convert_row_to_object(filepath, schema: BaseModel):
    df = pd.read_csv(filepath)
    map_list = [
        schema(**{
            key: df.loc[i][ii]
            for ii, key in enumerate(df.columns)
        })
        for i in range(len(df))
    ]

    return map_list
