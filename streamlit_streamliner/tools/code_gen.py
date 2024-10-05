def generate_code(widgets, columns_config):
    code_lines = [
        "import streamlit as st",
        "",
        "st.set_page_config(page_title='Generated App')",
        "",
        "# Column Configuration",
        f"column_widths = {columns_config['widths']}",
        "columns = st.columns(column_widths)",
        "",
        "# Start of your app",
        "",
    ]
    for widget in widgets:
        params = widget["params"]
        code = widget["config"]["code"]
        # Prepare parameters for code
        param_strs = []
        for k, v in params.items():
            if v == "" or v is None:
                continue
            if isinstance(v, str):
                param_strs.append(f'{k}="{v}"')
            elif isinstance(v, list):
                options = ", ".join([f'"{item}"' for item in v])
                param_strs.append(f"{k}=[{options}]")
            else:
                param_strs.append(f"{k}={v}")
        params_code = ", ".join(param_strs)
        column_index = int(widget["column"].split()[-1]) - 1
        code_line = f"with columns[{column_index}]:\n    {code}({params_code})"
        code_lines.append(code_line)
    return "\n".join(code_lines)
