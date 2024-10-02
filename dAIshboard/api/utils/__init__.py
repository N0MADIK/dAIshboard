import json
import pandas as pd
from io import BytesIO
from .. import DATA_PATH
from ..database.utils import add_data_metadata, retrive_project_metadata


def get_project_metadata(project_id: str, user_id: str):
    project_metadata = retrive_project_metadata(project_id, user_id)
    data = []
    for pmd in project_metadata:
        file_data = {
            "name": pmd.name,
            "type": "folder",
        }
        children = [
            {
                "name": "type",
                "type": "folder",
                "children": [{"name": pmd.file_type, "type": "file"}],
            }
        ]
        columns = []
        file_types = json.loads(pmd.types)
        for col in json.loads(pmd.columns):
            columns.append(
                {
                    "name": col,
                    "type": "folder",
                    "children": [
                        {
                            "name": "type",
                            "type": "folder",
                            "children": [
                                {
                                    "name": file_types.get(col, "unkown"),
                                    "type": "file",
                                }
                            ],
                        }
                    ],
                }
            )
        children.append({"name": "columns", "type": "folder", "children": columns})
        file_data["children"] = children
        data.append(file_data)
    return data


def add_project_data(file: object, user_id: str, project_id: str):
    fname = file.filename
    df, dtype = None, ""
    tokens = fname.split(".")
    dtype = tokens.pop(-1)
    name = ".".join(tokens)
    if ".xlsx" in fname:
        df = pd.read_excel(BytesIO(file.read()))
        dtype = "xlsx"
        df.to_excel(DATA_PATH + fname, index=False)
    elif ".csv" in fname:
        df = pd.read_csv(BytesIO(file.read()))
        dtype = "csv"
        df.to_csv(DATA_PATH + fname, index=False)
    if df is None:
        return False
    add_data_metadata(df, name, dtype, user_id, project_id)
    return True
