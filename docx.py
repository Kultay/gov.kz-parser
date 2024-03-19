import csv
from docx import Document

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

file_path = r'C:\Users\Danik\Downloads\16984.docx'
tables = read_docx_tables(file_path)

with open("output.csv", 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(tables)








