def detect_file_format(file_path):
    """
    Detect the file format based on the file extension.
    """
    extension = file_path.split(".")[-1].lower()
    return extension
