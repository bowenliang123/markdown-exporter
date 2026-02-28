from .mimetype_utils import MimeType


def get_meta_data(mime_type: MimeType, output_filename: str | None) -> dict[str, str]:
    if not mime_type:
        raise ValueError("Failed to generate meta data, mime_type is not defined")

    # normalize the filename
    result_filename: str | None = None
    temp_filename = output_filename.strip() if output_filename else None
    if temp_filename:
        # ensure extension name
        extension = MimeType.get_extension(mime_type)
        if not temp_filename.lower().endswith(extension):
            temp_filename = f"{temp_filename}{extension}"
        result_filename = temp_filename

    return {
        "mime_type": mime_type,
        "filename": result_filename,
    }
