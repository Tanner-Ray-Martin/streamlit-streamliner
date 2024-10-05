# app_generator.py

import streamlit as st
import json
from io import StringIO
import base64
from tools.widget_templates import WIDGETS
from tools.code_gen import generate_code

# Set page configuration
st.set_page_config(
    page_title="Streamlit App Generator", page_icon=":art:", layout="wide"
)

# Initialize session state
if "widgets" not in st.session_state:
    st.session_state.widgets = []

if "widget_counter" not in st.session_state:
    st.session_state.widget_counter = 0

if "columns_config" not in st.session_state:
    st.session_state.columns_config = {"num_columns": 1, "widths": [1.0]}

# Sidebar
st.sidebar.title("Layout Configuration")

# Column Configuration

with st.sidebar.expander("Column Configuration"):
    # Number of columns
    num_columns = st.selectbox(
        "Number of Columns",
        [1, 2, 3, 4],
        index=st.session_state.columns_config["num_columns"] - 1,
    )
    st.session_state.columns_config["num_columns"] = num_columns

    # Column widths
    widths = []
    total_width = 0.0
    for i in range(num_columns):
        width = st.slider(
            f"Width of Column {i+1}",
            min_value=0.0,
            max_value=1.0,
            value=(1.0 / num_columns),
            step=0.05,
            key=f"col_width_{i}",
        )
        widths.append(width)
        total_width += width

    # Normalize widths if total is not 1.0
    if total_width != 1.0:
        widths = [w / total_width for w in widths]

    st.session_state.columns_config["widths"] = widths

st.sidebar.markdown("---")


# Function to add widget
def add_widget(widget_name, target_column):
    st.session_state.widget_counter += 1
    widget_id = f"{widget_name}_{st.session_state.widget_counter}"
    widget = {
        "id": widget_id,
        "name": widget_name,
        "column": target_column,
        "config": WIDGETS[widget_name],
        "params": WIDGETS[widget_name]["params"].copy(),
    }
    # Assign a unique key
    widget["params"]["key"] = widget_id
    st.session_state.widgets.append(widget)


# Widget selection
st.sidebar.header("Add Widgets")
available_widgets = list(WIDGETS.keys())
selected_widget = st.sidebar.selectbox(
    "Select a widget to add", [""] + available_widgets
)

if selected_widget:
    # Select target column
    target_column = st.sidebar.selectbox(
        "Select Target Column",
        [f"Column {i+1}" for i in range(num_columns)],
        key="target_column",
    )
    if st.sidebar.button("Add Widget"):
        add_widget(selected_widget, target_column)
        # No need to rerun; Streamlit will update automatically

# Display widgets in sidebar for customization
if st.session_state.widgets:
    st.sidebar.markdown("---")
    st.sidebar.header("Customize Widgets")
    widgets_to_remove = []
    for idx, widget in enumerate(st.session_state.widgets):
        with st.sidebar.expander(f"{idx + 1}. {widget['name']} in {widget['column']}"):
            # Customize parameters
            for param, value in widget["params"].items():
                if param == "key":
                    continue  # Skip the key parameter
                param_type = type(value)
                # Provide appropriate input fields based on parameter type
                if isinstance(value, str):
                    widget["params"][param] = st.text_input(
                        f"{param}", value=value, key=f"{widget['id']}_{param}"
                    )
                elif isinstance(value, int):
                    widget["params"][param] = st.number_input(
                        f"{param}", value=value, key=f"{widget['id']}_{param}"
                    )
                elif isinstance(value, float):
                    widget["params"][param] = st.number_input(
                        f"{param}",
                        value=value,
                        key=f"{widget['id']}_{param}",
                        format="%.2f",
                    )
                elif isinstance(value, bool):
                    widget["params"][param] = st.checkbox(
                        f"{param}", value=value, key=f"{widget['id']}_{param}"
                    )
                elif isinstance(value, list):
                    options_str = st.text_area(
                        f"{param} (comma-separated)",
                        value=", ".join(map(str, value)),
                        key=f"{widget['id']}_{param}",
                    )
                    widget["params"][param] = [
                        opt.strip() for opt in options_str.split(",")
                    ]
                elif value is None:
                    widget["params"][param] = st.text_input(
                        f"{param}", value="", key=f"{widget['id']}_{param}"
                    )
                # Add more types if necessary

            # Change target column
            widget["column"] = st.selectbox(
                "Change Target Column",
                [f"Column {i+1}" for i in range(num_columns)],
                index=int(widget["column"].split()[-1]) - 1,
                key=f"{widget['id']}_column",
            )

            # Remove widget
            remove = st.button("Remove Widget", key=f"remove_{widget['id']}")
            if remove:
                widgets_to_remove.append(idx)

    # Remove widgets outside the loop to avoid indexing issues
    for idx in sorted(widgets_to_remove, reverse=True):
        del st.session_state.widgets[idx]

# Main Page Preview
st.header("Preview")

# Create columns based on configuration
column_widths = st.session_state.columns_config["widths"]
columns = st.columns(column_widths)

# Place widgets in their assigned columns
for idx, widget in enumerate(st.session_state.widgets):
    params = widget["params"]
    code = widget["config"]["code"]
    # Execute the widget code in the assigned column
    column_index = int(widget["column"].split()[-1]) - 1
    with columns[column_index]:
        try:
            exec_params = {k: v for k, v in params.items() if v != "" and v is not None}
            exec(f"{code}(**exec_params)")
        except Exception as e:
            st.error(f"Error in widget {widget['name']}: {e}")

# Code Generation
st.markdown("---")
st.header("Generated Code")


generated_code = generate_code(
    st.session_state.widgets, st.session_state.columns_config
)
st.code(generated_code, language="python")


# Download Code Button
def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.
    """
    if isinstance(object_to_download, bytes):
        b64 = base64.b64encode(object_to_download).decode()
    else:
        b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


download_filename = "generated_app.py"
download_button_str = download_link(
    generated_code, download_filename, "Download Generated App"
)
st.markdown(download_button_str, unsafe_allow_html=True)

# Save & Load Configurations
st.sidebar.markdown("---")
st.sidebar.header("Save & Load Configuration")

# Save configuration
if st.sidebar.button("Save Configuration"):
    config = {
        "widgets": st.session_state.widgets,
        "widget_counter": st.session_state.widget_counter,
        "columns_config": st.session_state.columns_config,
    }
    config_str = json.dumps(config)
    b64 = base64.b64encode(config_str.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="config.json">Download Configuration</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

# Load configuration
uploaded_file = st.sidebar.file_uploader("Load Configuration", type=["json"])
if uploaded_file is not None:
    content = uploaded_file.getvalue().decode("utf-8")
    config = json.loads(content)
    st.session_state.widgets = config["widgets"]
    st.session_state.widget_counter = config["widget_counter"]
    st.session_state.columns_config = config.get(
        "columns_config", {"num_columns": 1, "widths": [1.0]}
    )
    # No need to rerun; Streamlit will update automatically
