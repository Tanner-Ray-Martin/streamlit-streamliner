# Available widgets
WIDGETS = {
    "Text Input": {
        "code": "st.text_input",
        "params": {"label": "Enter your text", "value": "", "key": ""},
    },
    "Number Input": {
        "code": "st.number_input",
        "params": {
            "label": "Enter a number",
            "value": 0,
            "min_value": None,
            "max_value": None,
            "step": None,
            "format": None,
            "key": "",
        },
    },
    "Text Area": {
        "code": "st.text_area",
        "params": {
            "label": "Enter text",
            "value": "",
            "height": None,
            "max_chars": None,
            "key": "",
        },
    },
    "Select Box": {
        "code": "st.selectbox",
        "params": {
            "label": "Choose an option",
            "options": ["Option 1", "Option 2", "Option 3"],
            "index": 0,
            "key": "",
        },
    },
    "Multi Select": {
        "code": "st.multiselect",
        "params": {
            "label": "Choose options",
            "options": ["Option 1", "Option 2", "Option 3"],
            "default": None,
            "key": "",
        },
    },
    "Slider": {
        "code": "st.slider",
        "params": {
            "label": "Slide to select",
            "min_value": 0,
            "max_value": 100,
            "value": None,
            "step": 1,
            "format": None,
            "key": "",
        },
    },
    "Checkbox": {
        "code": "st.checkbox",
        "params": {"label": "Check me", "value": False, "key": ""},
    },
    "Radio Buttons": {
        "code": "st.radio",
        "params": {
            "label": "Choose one",
            "options": ["Option 1", "Option 2", "Option 3"],
            "index": 0,
            "key": "",
        },
    },
    "Date Input": {
        "code": "st.date_input",
        "params": {"label": "Select a date", "value": None, "key": ""},
    },
    "Time Input": {
        "code": "st.time_input",
        "params": {"label": "Select time", "value": None, "key": ""},
    },
    "File Uploader": {
        "code": "st.file_uploader",
        "params": {
            "label": "Upload a file",
            "type": None,
            "accept_multiple_files": False,
            "key": "",
        },
    },
    "Color Picker": {
        "code": "st.color_picker",
        "params": {"label": "Pick a color", "value": None, "key": ""},
    },
    "Button": {"code": "st.button", "params": {"label": "Click me", "key": ""}},
    # Add more widgets as needed
}
