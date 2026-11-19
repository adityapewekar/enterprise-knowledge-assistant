from io import BytesIO
import struct
from zipfile import BadZipFile

import fitz
import olefile
from olefile.olefile import OleFileError
from docx import Document
from PIL import Image, UnidentifiedImageError
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
import pytesseract
from pytesseract import TesseractError, TesseractNotFoundError

from domain.document_errors import DocumentExtractionError, MalformedDocumentError, UnsupportedDocumentTypeError


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".ppt",
    ".pptx",
    ".bmp",
    ".gif",
    ".jpeg",
    ".jpg",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
}


def parse_doc(file_path):
    with fitz.open(file_path) as document:
        return "".join(page.get_text() for page in document)


class MultiFormatDocumentParser:
    def parse(self, filename: str, content: bytes) -> str:
        extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if not extension:
            raise UnsupportedDocumentTypeError("The uploaded file must have a supported filename extension.")

        extension = f".{extension}"
        if extension not in SUPPORTED_EXTENSIONS:
            raise UnsupportedDocumentTypeError(f"Unsupported file extension: {extension}")
        if not content:
            raise MalformedDocumentError("The uploaded file is empty.")

        try:
            if extension == ".pdf":
                return self._parse_pdf(content)
            if extension == ".docx":
                return self._parse_docx(content)
            if extension == ".txt":
                return content.decode("utf-8-sig")
            if extension == ".pptx":
                return self._parse_pptx(content)
            if extension == ".ppt":
                return self._parse_ppt(content)
            return self._parse_image(content)
        except (UnsupportedDocumentTypeError, MalformedDocumentError, DocumentExtractionError):
            raise
        except (UnicodeDecodeError, fitz.FileDataError, BadZipFile, ValueError, struct.error) as exc:
            raise MalformedDocumentError("The uploaded file is not a valid document of the declared type.") from exc

    @staticmethod
    def _parse_pdf(content: bytes) -> str:
        try:
            with fitz.open(stream=content, filetype="pdf") as document:
                return "".join(page.get_text() for page in document)
        except Exception as exc:
            raise MalformedDocumentError("The uploaded file is not a valid PDF.") from exc

    @staticmethod
    def _parse_docx(content: bytes) -> str:
        try:
            document = Document(BytesIO(content))
            parts = [paragraph.text for paragraph in document.paragraphs if paragraph.text]
            for table in document.tables:
                parts.extend(
                    cell.text
                    for row in table.rows
                    for cell in row.cells
                    if cell.text
                )
            return "\n".join(parts)
        except Exception as exc:
            raise MalformedDocumentError("The uploaded file is not a valid DOCX document.") from exc

    @staticmethod
    def _parse_pptx(content: bytes) -> str:
        try:
            presentation = Presentation(BytesIO(content))
            parts = []

            def collect_shapes(shapes):
                for shape in shapes:
                    if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
                        collect_shapes(shape.shapes)
                    if shape.has_text_frame and shape.text:
                        parts.append(shape.text)
                    if shape.has_table:
                        parts.extend(
                            cell.text
                            for row in shape.table.rows
                            for cell in row.cells
                            if cell.text
                        )

            for slide in presentation.slides:
                collect_shapes(slide.shapes)
            return "\n".join(parts)
        except Exception as exc:
            raise MalformedDocumentError("The uploaded file is not a valid PPTX presentation.") from exc

    @staticmethod
    def _parse_ppt(content: bytes) -> str:
        if not olefile.isOleFile(BytesIO(content)):
            raise MalformedDocumentError("The uploaded file is not a valid legacy PowerPoint document.")

        try:
            with olefile.OleFileIO(BytesIO(content)) as presentation:
                stream_path = ["PowerPoint Document"]
                if not presentation.exists(stream_path):
                    raise MalformedDocumentError("The PowerPoint document stream is missing.")
                data = presentation.openstream(stream_path).read()
        except OleFileError as exc:
            raise MalformedDocumentError("The legacy PowerPoint document is invalid.") from exc

        if not data:
            raise MalformedDocumentError("The legacy PowerPoint document stream is empty.")
        texts = []

        def read_records(start: int, end: int) -> None:
            offset = start
            while offset < end:
                if end - offset < 8:
                    raise MalformedDocumentError("The legacy PowerPoint record stream is truncated.")

                version_instance, record_type, length = struct.unpack_from("<HHI", data, offset)
                payload_start = offset + 8
                payload_end = payload_start + length
                if payload_end > end:
                    raise MalformedDocumentError("The legacy PowerPoint record exceeds its stream bounds.")

                version = version_instance & 0x000F
                if record_type == 4000:
                    if length % 2:
                        raise MalformedDocumentError("A legacy PowerPoint text record is malformed.")
                    text = data[payload_start:payload_end].decode("utf-16le")
                    if text:
                        texts.append(text)
                elif record_type == 4008:
                    text = data[payload_start:payload_end].decode("cp1252")
                    if text:
                        texts.append(text)
                elif version == 0x000F:
                    read_records(payload_start, payload_end)

                offset = payload_end

        read_records(0, len(data))
        return "\n".join(texts)

    @staticmethod
    def _parse_image(content: bytes) -> str:
        try:
            with Image.open(BytesIO(content)) as image:
                image.load()
                return pytesseract.image_to_string(image)
        except (TesseractNotFoundError, TesseractError) as exc:
            raise DocumentExtractionError("Tesseract OCR is unavailable or failed to process the image.") from exc
        except (UnidentifiedImageError, Image.DecompressionBombError, OSError, ValueError) as exc:
            raise MalformedDocumentError("The uploaded image is invalid or unreadable.") from exc


class PyMuPDFDocumentParser(MultiFormatDocumentParser):
    """Compatibility name for the parser configured by the API."""
