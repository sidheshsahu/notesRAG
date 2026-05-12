from docling.document_converter import DocumentConverter

source = r"D:\notesRAG\notesRAG\EVM Syllabus.pdf"  
converter = DocumentConverter()
doc = converter.convert(source).document

print(doc.export_to_markdown())  