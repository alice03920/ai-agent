import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_working_directory = os.path.abspath(working_directory)

        target_directory = os.path.abspath(
            os.path.join(working_directory, directory)
        )

        if (
            os.path.commonpath(
                [absolute_working_directory, target_directory]
            )
            != absolute_working_directory
        ):
            return (
                f'Error: Cannot list "{directory}" as it is outside '
                "the permitted working directory"
            )

        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        contents = []

        for item in os.listdir(target_directory):
            item_path = os.path.join(target_directory, item)

            contents.append(
                f"- {item}: "
                f"file_size={os.path.getsize(item_path)} bytes, "
                f"is_dir={os.path.isdir(item_path)}"
            )

        return "\n".join(contents)

    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
