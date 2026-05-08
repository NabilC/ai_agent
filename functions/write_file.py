from google import genai
from google.genai import types
import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

    if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        parent_dir = os.path.dirname(abs_file_path)
        try:
            os.makedirs(parent_dir, exist_ok=True)
        except Exception as e:
            return f'Could not create parent dirs: {parent_dir} = {e}'
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f'Failed to write to file: {file_path}, {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to the python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Gets file path for the file to run",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Optional arguments to pass to the Python file",
            ),
        },
        required=["file_path", "content"]
    ),
)
