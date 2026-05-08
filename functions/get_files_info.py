from google import genai
from google.genai import types
import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # If the directory argument is not a directory, again, return an error string
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # Will be True or False if target_dir falls within abs working_directory path
        # # common path should be same as abs working dir path if target dir is valid
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        file_info = []

        for item in os.listdir(target_dir):
            full_path = os.path.join(target_dir, item)
            if os.path.isdir(full_path):
                # it's a directory
                item_type = "directory"
            else:
                # it's a file
                item_type = "file"
            file_info.append({
                "name": item,
                "file_size": os.path.getsize(full_path),
                "is_dir":  item_type == "directory"
            })

        result_lines = []

        for info in file_info:
            result_lines.append(f"- {info['name']}: file_size={info['file_size']} bytes, is_dir={info['is_dir']}")

        return "\n".join(result_lines)
    except Exception as e:
        return f"Error: {str(e)}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
