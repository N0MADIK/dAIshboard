import pandas as pd
import os
import openai
import json
import plotly.io as pio
from uuid import uuid4
import inspect
import logging

DATA_PATH = "/home/kg2911/dev/dAIshboard/dAIshboard/api/plot_generator/data/"
META_PATH = "/home/kg2911/dev/dAIshboard/dAIshboard/api/plot_generator/meta/"


stock = pd.read_excel(DATA_PATH + "Stock_Cluster.xlsx")
product = pd.read_excel(DATA_PATH + "product.xlsx")
sales = pd.read_excel(DATA_PATH + "sales_of_product.xlsx")
googleplaystore = pd.read_csv(DATA_PATH + "googleplaystore.csv")


df_metadata = {}

with open(META_PATH + "df_metadata.json") as f:
    df_metadata = json.load(f)


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
        if df_metadata[filename]["file_type"] == "xlsx":
            filepath = data_path + filename + ".xlsx"
            df = pd.read_excel(filepath)
            selected_dfs[filename] = df
        if df_metadata[filename]["file_type"] == "csv":
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


def save_new_plot(
    user_query, plot_code, plot_json, file_path=META_PATH + "plot_metadata.json"
):
    plot_dict = json.loads(plot_json)
    plot_title = plot_dict["layout"]["title"]["text"]

    with open(file_path, "r") as f:
        plots = json.load(f)

        new_plot = {
            "plot_id": str(uuid4()),
            "plot_title": plot_title,
            "user_query": user_query,
            "plot_code": plot_code,
            "plot_json": plot_json,
        }

        plots.append(new_plot)

    # Save the file
    with open(file_path, "w") as f:
        json.dump(plots, f, indent=4)


def generate_new_plot(
    selected_metadata,
    user_query,
    file_path=META_PATH + "plot_metadata.json",
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
            save_new_plot(user_query, code, plot_json, file_path)

            return {"code": code, "plot_json": plot_json}

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
    file_path=META_PATH + "plot_metadata.json",
    error_message_create=None,
    error_code_create=None,
):
    try:
        selected_metadata = select_dataframe(df_metadata, user_query)
        result = generate_new_plot(
            selected_metadata,
            user_query,
            file_path,
            error_message_create,
            error_code_create,
        )
        # plot_json = result["plot_json"]
        # show_plot(plot_json)
        return result
    except Exception as e:
        error_message = str(e)
        return {"error": "Failed to create a plot.", "error_message": error_message}


def generate_from_user_query(user_query: str):
    return create_new_plot(df_metadata, user_query)
