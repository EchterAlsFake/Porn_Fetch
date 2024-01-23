import sys
from cx_Freeze import setup, Executable

# Replace 'your_script.py' with the name of your Python script
script_name = 'Porn_Fetch_CLI.py'

# Define the base options for cx_Freeze
base = None

# Create an Executable object
executables = [
    Executable(script_name, base=base, target_name="Porn_Fetch")
]

# Define setup parameters
options = {
    'build_exe': {
        'includes': ["src.backend.shared_functions"],  # List any additional modules or packages to include
        'excludes': [],  # List any modules or packages to exclude
    }
}

# Call cx_Freeze setup with the executable and options
setup(
    name='Porn_Fetch',  # Replace with your application name
    version='3.0',       # Replace with your application version
    description='an Open-Source PornHub Downloader',  # Replace with a description
    executables=executables,
    options=options
)
