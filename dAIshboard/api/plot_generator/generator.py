import pandas as pd
import openai
import json
from uuid import uuid4
import inspect

from .. import DATA_PATH
from ..database.utils import (
    retrive_project_metadata,
    add_plot_metadata,
    get_existing_plots,
    get_latest_user_info_for_plot,
)


# select the appropriate dataframe to use
def select_dataframe(df_metadata, user_query):
    # create prompt
    prompt = f"""User_query: {user_query}. 
    
    Here are the metadata for the datasets available: {df_metadata}
    
    Based on this, please follow user request to choose the most appropriate dataset or datasets for code generation.

    You output should only be the list of the dataset(s)'s name. For example, ["dataset_1", "dataset_2", ...]
    """

    # generate code
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in selecting the most appropriate dataset(s) for analysis",
            },
            {"role": "user", "content": prompt},
        ],
    )
    result = completion.choices[0].message.content

    for attempt in range(3):
        try:
            df_to_use = eval(result)
            selected_metadata = {key: df_metadata[key] for key in df_to_use}
            return selected_metadata

        except Exception as e:
            error_message = str(e)

            # fix the output format if wrong
            correction_prompt = f"""The output generated casued an error when evaluating. You need to correct the output format. 
            
            The output should only be a list of the dataset(s)'s name. For example, ["dataset_1", "dataset_2", ...]. 
            No extra explanation is needed so that there is no error when the output is passed to python function `eval()`.
            
            Output: {result}
    
            Error: {error_message}
    
            """

            correction_completion = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in fixing errors based on requirements.",
                    },
                    {"role": "user", "content": correction_prompt},
                ],
            )
            result = completion.choices[0].message.content

    return {
        "error": "Failed to obtain a list of dataframes to use.",
        "error_message": error_message,
    }


# xls, xlsx, xlsm etc. Specify in frontend
def read_selected_dfs(selected_metadata):
    selected_dfs = {}
    data_path = DATA_PATH
    for filename in selected_metadata.keys():
        if selected_metadata[filename]["file_type"] == "xlsx":
            filepath = data_path + filename + ".xlsx"
            df = pd.read_excel(filepath)
            selected_dfs[filename] = df
        if selected_metadata[filename]["file_type"] == "csv":
            filepath = data_path + filename + ".csv"
            df = pd.read_csv(filepath)
            selected_dfs[filename] = df
    return selected_dfs


def generate_new_code(
    selected_metadata, user_query, error_message_create=None, error_code_create=None
):
    # create prompt
    prompt = f"""User_query: {user_query}. 
    
    Here are the metadata for the datasets for you to use: {selected_metadata}
    
    Based on this, please follow user request to choose the appropriate dataset or datasets and then generate the Python code to create plot using Plotly.
    If no specific request is provided, generate the most appropriate plot(s) using the appropraite columns. 
    Each plot should have a plot tile. 
    Make sure is plot is easy to read and understand.

    Assume the relevant DataFrame(s) will be passed to the function as an argument. 
    You must name the function "code_generation_llm" and use the key in the metadata as the argument name. 
    The return statement is the plot in json format.

    Check if the code is error free in your code before outputing it.
    
    The output should be code ONLY that can be direcly used without any processing. """

    if error_message_create and error_code_create:
        prompt += f"""This is the error code: \n{error_code_create} \nThe following error occurred when running the code: {error_message_create}. 
        Please modify the code to fix the issue. If it's an issue with the dataset ifself, try a different approach."""

    # generate code
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in code generation particularly generating plots in Python",
            },
            {"role": "user", "content": prompt},
        ],
    )
    code = completion.choices[0].message.content
    return code


def save_new_plot(user_query, plot_code, plot_json, user_id: str, project_id: str):
    plot_dict = json.loads(plot_json)
    plot_title = plot_dict["layout"]["title"]["text"]
    new_plot_id = str(uuid4())[:5]
    add_plot_metadata(
        new_plot_id, plot_title, user_query, plot_code, plot_json, user_id, project_id
    )
    return new_plot_id


def generate_new_plot(
    selected_metadata,
    user_query,
    user_id: str,
    project_id: str,
    error_message_create=None,
    error_code_create=None,
):
    # First attempt
    selected_dfs = read_selected_dfs(selected_metadata)

    raw_code = generate_new_code(
        selected_metadata, user_query, error_message_create, error_code_create
    )

    # Retry up to 3 times
    for attempt in range(3):
        try:
            if raw_code.startswith("```") and raw_code.endswith("```"):
                code = raw_code[len("```python") :].strip()[:-3].strip()
            else:
                code = raw_code.split("```python")[1].split("```")[0]

            # execute the code
            exec(code, globals())

            # Inspect parameters of the function generated
            parameters = inspect.signature(code_generation_llm).parameters

            matched_args = []

            for param in parameters:
                if param in selected_dfs.keys():
                    matched_args.append(selected_dfs[param])

            # convert to json
            plot_json = code_generation_llm(*matched_args)

            # save plot
            new_plot_id = save_new_plot(
                user_query, code, plot_json, user_id, project_id
            )

            return {"code": code, "plot_json": plot_json, "plot_id": new_plot_id}

        except Exception as e:
            error_message_new = str(e)
            code = generate_new_code(
                selected_metadata, user_query, error_message_new, code
            )

    return {
        "error": "Failed to generate a valid plot after multiple attempts.",
        "error_message": error_message_new,
    }


def create_new_plot(
    df_metadata,
    user_query,
    user_id: str,
    project_id: str,
    error_message_create=None,
    error_code_create=None,
):
    try:
        selected_metadata = select_dataframe(df_metadata, user_query)
        result = generate_new_plot(
            selected_metadata,
            user_query,
            user_id,
            project_id,
            error_message_create,
            error_code_create,
        )
        # plot_json = result["plot_json"]
        # show_plot(plot_json)
        return result
    except Exception as e:
        error_message = str(e)
        return {"error": "Failed to create a plot.", "error_message": error_message}


def check_existing_plot(user_query, user_id: str, project_id: str):

    all_project_plots = get_existing_plots(user_id, project_id)
    available_plot = [
        {"plot_id": pmd.plot_id, "plot_title": pmd.plot_title}
        for pmd in all_project_plots
    ]
    # create prompt
    prompt = f"""User_request: {user_query}. 
    
    Here are the available plots: {available_plot}
    
    Please read through the user request to determine if the user is asking for an update on an existing plot. 

    If the user tells you to modify/change/update a plot AND provides you with the plot tile, identify the plot title from the user request. 
    Then, find and return the corresponding id in a list. For exmaple, ['c2b9dfh-57sd-48gh-854c-43f56e556012']
    Otherwise, return an empty list if no plot title is specified. For example, [].
    You should only return the list.
    
    """

    # generate code
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in understanding user request",
            },
            {"role": "user", "content": prompt},
        ],
    )
    result = completion.choices[0].message.content
    # return result
    for attempt in range(3):
        try:
            id_list = eval(result)
            return id_list

        except Exception as e:
            error_message = str(e)

            # fix the output format if wrong
            correction_prompt = f"""The output generated casued an error when evaluating. You need to correct it. 
            
            The output format should follow the rules: 
                - If the user tells you to modify/change/update a plot AND provides you with the plot tile, identify the plot title from the user request. 
    Then, find and return the corresponding id in a list. For exmaple, ['c2b9dfh-57sd-48gh-854c-43f56e556012']
                - Return an empty list if no plot title is specified. For example, [].
            No extra explanation is needed so that there is no error when the output is passed to python function `eval()`.
            
            Output: {result}
    
            Error: {error_message}
            """

            correction_completion = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in fixing errors based on requirements.",
                    },
                    {"role": "user", "content": correction_prompt},
                ],
            )
            result = completion.choices[0].message.content

    return {
        "error": "Failed to obtain the id of the plot that needs to update.",
        "error_message": error_message,
    }


# select the appropriate dataframe to use
def update_dataframe(df_metadata, old_user_query, new_user_query):
    # create prompt
    prompt = f"""
    User old query: {old_user_query}. 

    User feedback: {new_user_query}.
    
    Here are the metadata for the datasets available: {df_metadata}
    
    Based on this, please carefully read through user's feedback to choose the most appropriate dataset or datasets for code generation.

    You output should only be the list of the dataset(s)'s name. For example, ["dataset_1", "dataset_2", ...]
    """

    # generate code
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in selecting the most appropriate dataset(s) for analysis",
            },
            {"role": "user", "content": prompt},
        ],
    )
    result = completion.choices[0].message.content

    for attempt in range(3):
        try:
            df_to_use = eval(result)
            selected_metadata = {key: df_metadata[key] for key in df_to_use}
            return selected_metadata

        except Exception as e:
            error_message = str(e)

            # fix the output format if wrong
            correction_prompt = f"""The output generated casued an error when evaluating. You need to correct the output format. 
            
            The output should only be a list of the dataset(s)'s name. For example, ["dataset_1", "dataset_2", ...]. 
            No extra explanation is needed so that there is no error when the output is passed to python function `eval()`.
            
            Output: {result}
    
            Error: {error_message}
    
            """

            correction_completion = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in fixing errors based on requirements.",
                    },
                    {"role": "user", "content": correction_prompt},
                ],
            )
            result = completion.choices[0].message.content

    return {
        "error": "Failed to obtain a list of dataframes to use for the updated plot.",
        "error_message": error_message,
    }


def update_code(
    new_user_query,
    old_code,
    updated_metadata,
    error_message_update=None,
    error_code_update=None,
):
    prompt = f"""User feedback: {new_user_query}. 
    
    Old code: {old_code}

    Updated metadata {updated_metadata}
    
    Please use the updated metadata as the input(s) and then update your code based on the user feedback. The return statement must be the plot in json format.

    Check if the code is error free in your code before outputing it.
    
    The output should be code ONLY that can be direcly used without any processing. """

    if error_message_update and error_code_update:
        prompt += f"""This is the error code: \n{error_code_update} \nThe following error occurred when running the code: {error_message_update}. \nPlease modify the code to fix the issue."""

    # generate code
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in code generation particularly modifying code based on user feedback in Python",
            },
            {"role": "user", "content": prompt},
        ],
    )
    code = completion.choices[0].message.content
    return code


def save_updated_plot(
    new_user_query,
    update_id,
    updated_code,
    updated_plot_json,
    old_plot,
):
    try:
        add_plot_metadata(
            update_id,
            old_plot.plot_title,
            new_user_query,
            updated_code,
            updated_plot_json,
            old_plot.user_id,
            old_plot.project_id,
        )
    except Exception as e:
        return {
            "error": "Failed to save the updated plot info to metadata.",
            "error_message": str(e),
        }


def generate_updated_plot(
    updated_metadata,
    new_user_query,
    old_code,
    update_id,
    old_plot,
    error_message_update=None,
    error_code_update=None,
):
    # First attempt
    updated_selected_dfs = read_selected_dfs(updated_metadata)
    updated_raw_code = update_code(
        new_user_query, old_code, error_message_update, error_code_update
    )

    # Retry up to 3 times
    for attempt in range(3):
        try:
            if updated_raw_code.startswith("```") and updated_raw_code.endswith("```"):
                updated_code = updated_raw_code[len("```python") :].strip()[:-3].strip()
            else:
                updated_code = updated_raw_code.split("```python")[1].split("```")[0]

            # execute the code
            exec(updated_code, globals())

            # # Inspect parameters of the function generated
            parameters = inspect.signature(code_generation_llm).parameters

            matched_args = []

            for param in parameters:
                if param in updated_selected_dfs.keys():
                    matched_args.append(updated_selected_dfs[param])

            # convert to json
            updated_plot_json = code_generation_llm(*matched_args)

            # save plot
            save_updated_plot(
                new_user_query, update_id, updated_code, updated_plot_json, old_plot
            )

            return {
                "code": updated_code,
                "plot_json": updated_plot_json,
                "plot_id": update_id,
            }

        except Exception as e:
            error_message_update = str(e)
            code = update_code(
                new_user_query, old_code, error_message_update, updated_code
            )

    return {
        "error": "Failed to generate a valid updated plot after multiple attempts.",
        "error_message": error_message_update,
    }


def update_existing_plot(
    df_metadata,
    new_user_query,
    update_id,
    user_id,
    project_id,
    error_message_update=None,
    error_code_update=None,
):

    try:
        old_plot = get_latest_user_info_for_plot(update_id, user_id, project_id)
        old_user_query, old_code = old_plot.user_query, old_plot.plot_code
        updated_metadata = update_dataframe(df_metadata, old_user_query, new_user_query)
        updated_result = generate_updated_plot(
            updated_metadata,
            new_user_query,
            old_code,
            update_id,
            old_plot,
            error_message_update,
            error_code_update,
        )

        # updated_plot_json = updated_result['plot_json']
        # show_plot(updated_plot_json)

        return updated_result
    except Exception as e:
        error_message = str(e)
        return {"error": "Failed to update a plot.", "error_message": error_message}


def daishboard(
    user_query,
    project_id,
    user_id,
    error_message_create=None,
    error_code_create=None,
    error_message_update=None,
    error_code_update=None,
):
    df_metadata = get_df_metadata(user_id, project_id)
    if_existing = check_existing_plot(user_query, user_id, project_id)
    if not if_existing:
        print("Creating new plot")
        result = create_new_plot(
            df_metadata,
            user_query,
            user_id,
            project_id,
            error_message_create,
            error_code_create,
        )
        return result

    else:
        print("Updating a plot")
        id_to_update = if_existing[0]
        print(id_to_update)
        updated_result = update_existing_plot(
            df_metadata,
            user_query,
            id_to_update,
            user_id,
            project_id,
            error_message_update,
            error_code_update,
        )
        return updated_result


def get_df_metadata(user_id: str, project_id: str):
    metadata = retrive_project_metadata(project_id, user_id)
    print("HERER!!!", metadata, project_id, user_id)
    df_metadata = {}
    for md in metadata:
        k = md.name
        v = {
            "file_type": md.file_type,
            "columns": json.loads(md.columns),
            "types": json.loads(md.types),
            "sample_data": json.loads(md.sample_data),
        }
        df_metadata.setdefault(k, v)
    return df_metadata


def generate_from_user_query(user_query: str, user_id: str, project_id: str):
    result = daishboard(user_query, project_id, user_id)
    return result
