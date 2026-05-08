from google import genai
from google.genai import types
import os, subprocess

def run_python_file(working_directory, file_path, args= []):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))




        # If the file_path is outside the working_directory,
        # return the error string below. (Hopefully this part is easy by now!)
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Make sure that file_path exists and points to a regular file (rather than, e.g., a directory).
        # os.path.isfile() answers both questions at once. If this check fails, return an error string:
        # f'Error: "{file_path}" does not exist or is not a regular file'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # If the file name doesn't end with .py, return an error string:
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'


        final_args = ["python3", file_path]
        if args:
            final_args.extend(args)

        result = subprocess.run(
            final_args,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file within the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python script",
            ),
        },
        required=["file_path"]
    ),
)
