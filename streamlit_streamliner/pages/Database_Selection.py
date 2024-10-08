import streamlit as st
import os

models_dir = "models"


def get_databases():
    database_list = {}
    for file in os.listdir(models_dir):
        if file.endswith("_db.py"):
            database_name = file.replace(".py", "")
            database_path = os.path.join(models_dir, file)
            model_name = database_name + "_model"
            database_list[database_name] = {
                "database_path": database_path,
                "model_name": model_name,
            }
    return database_list


if __name__ == "__main__":
    st.write(get_databases())
