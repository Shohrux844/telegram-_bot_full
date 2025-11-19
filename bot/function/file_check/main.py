# Fayl formatlarini tekshirish
SUPPORTED_EXTENSIONS = {
    'jpg': ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff'],
    'docx': ['docx', 'doc'],
    'pptx': ['pptx', 'ppt'],
    'xlsx': ['xlsx', 'xls'],
    'html': ['html', 'htm'],
    'pdf': ['pdf']
}


def get_file_extension(filename: str) -> str:
    return filename.lower().split('.')[-1] if '.' in filename else ''


def is_supported_format(filename: str, conversion_type: str) -> bool:
    ext = get_file_extension(filename)

    format_checks = {
        'jpg_pdf': ext in SUPPORTED_EXTENSIONS['jpg'],
        'word_pdf': ext in SUPPORTED_EXTENSIONS['docx'],
        'ppt_pdf': ext in SUPPORTED_EXTENSIONS['pptx'],
        'excel_pdf': ext in SUPPORTED_EXTENSIONS['xlsx'],
        'html_pdf': ext in SUPPORTED_EXTENSIONS['html'],
        'pdf_jpg': ext in SUPPORTED_EXTENSIONS['pdf'],
        'pdf_word': ext in SUPPORTED_EXTENSIONS['pdf'],
        'pdf_ppt': ext in SUPPORTED_EXTENSIONS['pdf'],
        'pdf_excel': ext in SUPPORTED_EXTENSIONS['pdf'],
        'pdf_pdfa': ext in SUPPORTED_EXTENSIONS['pdf']
    }

    return format_checks.get(conversion_type, False)
