import csv
from docx import Document
import re
def remove_symbol(text):
    if text is not None:
        cleaned_text = re.sub('[^a-zA-Zа-яА-ЯәғқңөұүhіӘҒҚҢӨҰҮҺІ0-9,.()-/@:;!№#$%&?*=_«» ]', '', text)
        return cleaned_text
    else:
        return None
def read_docx_tables(file_path):
    doc = Document(file_path)
    tables = []
    for table in doc.tables:
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                row_data.append(cell.text)
            tables.append(row_data)
    return tables

file_path = r'output_files\0a068e1ab84a1f1ac7a2039510f3f707_original.53642.docx'
tables = read_docx_tables(file_path)

with open("output.csv", 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(tables)








