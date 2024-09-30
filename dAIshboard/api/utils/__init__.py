import json
from .. import META_PATH


def get_project_metadata(project_id: str, user_id: str):

    meta_path = META_PATH + "df_metadata.json"
    with open(meta_path, "r") as fp:
        meta_json = json.load(fp)
        data = []
        for file_name, file_dict in meta_json.items():
            file_data = {
                "name": file_name,
                "type": "folder",
            }
            children = [
                {
                    "name": "type",
                    "type": "folder",
                    "children": [
                        {"name": file_dict.get("file_type", ""), "type": "file"}
                    ],
                }
            ]
            columns = []
            for col in file_dict.get("columns", []):
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
                                        "name": file_dict.get("types", {}).get(
                                            col, "unkown"
                                        ),
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
