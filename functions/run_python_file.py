import os
import subprocess
from config import FILE_FORMAT


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_dir) and file_path:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(FILE_FORMAT):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]

        if args:
            command.extend(args)

        process = subprocess.run(
            command, capture_output=True, text=True, timeout=30)

        output_string = ""

        if process.returncode != 0:
            output_string += "Process exited with code X\n"

        if not process.stderr and not process.stdout:
            output_string += "No output produced\n"
        else:
            output_string += f"STDOUT: {process.stdout}\n"
            output_string += f"STDERR: {process.stderr}\n"

        return output_string
    except Exception as e:
        raise f"Error: executing Python file: {e}"
