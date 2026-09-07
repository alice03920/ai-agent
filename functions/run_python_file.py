import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        absolute_file_path = os.path.abspath(
            os.path.join(working_directory, file_path)
        )

        # Make sure the file is inside the permitted working directory
        if (
            os.path.commonpath(
                [absolute_working_directory, absolute_file_path]
            )
            != absolute_working_directory
        ):
            return (
                f'Error: Cannot execute "{file_path}" as it is outside '
                "the permitted working directory"
            )

        # Make sure the path exists and is a regular file
        if not os.path.isfile(absolute_file_path):
            return (
                f'Error: "{file_path}" does not exist or is not a regular file'
            )

        # Make sure it is a Python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build the command
        command = ["python", absolute_file_path]

        if args:
            command.extend(args)

        # Run the Python file
        completed_process = subprocess.run(
            command,
            cwd=absolute_working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = []

        # Add stdout
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")

        # Add stderr
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")

        # Add non-zero exit code
        if completed_process.returncode != 0:
            output.append(
                f"Process exited with code {completed_process.returncode}"
            )

        # Handle programs that produced nothing
        if not completed_process.stdout and not completed_process.stderr:
            output.append("No output produced")

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file in the specified directory, with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "Directory to run the Python file in, relative to the working directory",
                },
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional arguments to pass to the Python file",
                },
            },
            "required": ["working_directory", "file_path"],
        },
    },
}
