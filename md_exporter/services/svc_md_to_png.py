#!/usr/bin/env python3
"""
MdToPng service
"""

import io
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile

import pymupdf
from PIL import Image
from xhtml2pdf import pisa

from ..utils.logger_utils import get_logger
from ..utils.markdown_utils import convert_markdown_to_html, get_md_text
from ..utils.text_utils import contains_chinese, contains_japanese

logger = get_logger(__name__)


def convert_to_html_with_font_support(md_text: str) -> str:
    """Convert Markdown to HTML with Chinese font support"""

    html_str = convert_markdown_to_html(md_text)

    if not contains_chinese(md_text) and not contains_japanese(md_text):
        return html_str

    # Add Chinese font CSS
    font_families = ",".join(
        [
            "Sans-serif",
            "STSong-Light",
            "MSung-Light",
            "HeiseiMin-W3",
        ]
    )
    css_style = f"""
    <style>
        html {{
            -pdf-word-wrap: CJK;
            font-family: "{font_families}"; 
        }}
    </style>
    """

    result = f"""
    {css_style}
    {html_str}
    """
    return result


def convert_md_to_png(
    md_text: str, output_path: Path, compress: bool = False, is_strip_wrapper: bool = False
) -> list[Path]:
    """
    Convert Markdown text to PNG images
    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output PNG files or ZIP file
        compress: Whether to compress all PNG images into a ZIP file
        is_strip_wrapper: Whether to remove code block wrapper if present
    Returns:
        List of paths to the created files
    Raises:
        ValueError: If input processing fails
        Exception: If conversion fails
    """
    # Process Markdown text
    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)

    output_filename = output_path.stem if output_path.suffix else "output"
    created_files = []
    images_for_zip = []

    try:
        # Convert to HTML
        html_str = convert_to_html_with_font_support(processed_md)

        # Convert to PDF
        result_file_bytes = pisa.CreatePDF(
            src=html_str,
            dest_bytes=True,
            encoding="utf-8",
            capacity=500 * 1024 * 1024,
        )

        # Open PDF and convert to PNG
        doc = pymupdf.open(stream=result_file_bytes)
        total_page_count = doc.page_count
        zoom = 2

        for page_num in range(total_page_count):
            page = doc.load_page(page_num)
            mat = pymupdf.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            # Convert to PIL Image
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

            # Save to memory
            img_buffer = io.BytesIO()
            img.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            # Create file name
            if total_page_count > 1:
                image_filename = f"{output_filename}_page{page_num + 1}.png"
            else:
                image_filename = f"{output_filename}.png"

            image_bytes = img_buffer.getvalue()

            if not compress:
                # Save PNG file directly
                if output_path.suffix and total_page_count == 1:
                    output_file = output_path
                else:
                    output_file = (
                        output_path.parent / image_filename if output_path.suffix else output_path / image_filename
                    )

                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_bytes(image_bytes)
                created_files.append(output_file)
                logger.info(f"Successfully converted to {output_file}")
            else:
                # Add to ZIP list
                images_for_zip.append({"blob": image_bytes, "suffix": ".png"})

        # If compression to ZIP is needed
        if compress and images_for_zip:
            with (
                NamedTemporaryFile(suffix=".zip", delete=True) as temp_zip_file,
                zipfile.ZipFile(temp_zip_file.name, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file,
            ):
                for idx, image_data in enumerate(images_for_zip, 1):
                    with NamedTemporaryFile(delete=True) as temp_file:
                        temp_file.write(image_data["blob"])
                        temp_file.flush()
                        zip_file.write(temp_file.name, arcname=f"image_{idx}{image_data['suffix']}")
                zip_file.close()

                output_path.write_bytes(Path(zip_file.filename).read_bytes())
                created_files.append(output_path)
                logger.info(f"Successfully created ZIP file with {len(images_for_zip)} PNG images: {output_path}")

    except Exception as e:
        raise Exception(f"Failed to convert to PNG: {e}")

    return created_files
