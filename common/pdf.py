from pypdf import PdfReader, mult
from openai import OpenAI
import io
import os
import json
from models import *

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

def parts_to_raw(input_parts):
    if input_parts is None:
        return None
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
            "role": "system",
            "content": "You're an assistant who analyzes PDFs. You get the raw text pieces and their coordinates (0;0 is in the bottom left corner), and answer with a JSON list of key-value pairs based on the document's content. These documents usually contain a lot of keys and values, try to find whichever belongs to which. Try to use every piece of information from the text, and also try not to invent new, nonexistent values. Follow the base template below, and don't use any quotation marks or markdown around the JSON.\n\n{\n  \"Név\": \"Example Name\",\n  \"Lakcím\": \"some address\",\n}\n\netc."
            },
            {
            "role": "user",
            "content": str(input_parts)
            }
        ],
        temperature=0,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    try:
        resp_dict = json.loads(response.choices[0].message.content)
        return resp_dict
    except:
        return None
    