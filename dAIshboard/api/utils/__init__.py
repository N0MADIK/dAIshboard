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
    name = ".".join(["_".join(x.split(" ")) for x in tokens])
    if ".xlsx" in fname:
        df_dict = pd.read_excel(BytesIO(file.read()), sheet_name=None)
        dtype = "xlsx"
        if len(df_dict) == 1:
            df = list(df_dict.values())[0]
            df.to_excel(DATA_PATH + name + "." + dtype, index=False)
            add_data_metadata(df, name, dtype, user_id, project_id)
        else:
            for n, ndf in df_dict.items():
                n_tokens = n.split(" ")
                n_name = "_".join(n_tokens)
                ndf.to_excel(DATA_PATH + n_name + "." + dtype, index=False)
                add_data_metadata(ndf, n_name, dtype, user_id, project_id)
        return True
    elif ".csv" in fname:
        df = pd.read_csv(BytesIO(file.read()))
        dtype = "csv"
        df.to_csv(DATA_PATH + fname, index=False)
        add_data_metadata(df, name, dtype, user_id, project_id)
        return True
    return False
