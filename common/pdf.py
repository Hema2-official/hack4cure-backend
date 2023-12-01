from pypdf import PdfReader, mult
from openai import OpenAI
import io
import os

client = OpenAI()

def visitor_body(text, user_matrix, tm_matrix, font_dictionary, font_size):
    if text is None or text.strip() == '':
        return
    matrix = mult(user_matrix, tm_matrix)
    parts.append({
        "text": text,
        "x": matrix[4],
        "y": matrix[5],
        })
    
def pdf_to_parts(pdf: bytes):
    reader = PdfReader(io.BytesIO(pdf))
    final_parts = {}
    global parts
    for i, page in enumerate(reader.pages):
        parts = []
        page.extract_text(visitor_text=visitor_body)
            
        y_min = min([part["y"] for part in parts])
        if y_min < 0:
            for part in parts:
                part["y"] -= y_min
        
        x_min = min([part["x"] for part in parts])
        if x_min < 0:
            for part in parts:
                part["x"] -= x_min

        parts.sort(key=lambda part: part["x"])
        parts.sort(key=lambda part: part["y"], reverse=True)

        final_parts[f"page{i}"] = parts

    return final_parts


