import pandas as pd
import google.generativeai as genai
import numpy as np
from docx import Document

API_KEY = 'AIzaSyBqoe55dpaKzIu-dVhVc004JDsbXqWgFbY'
genai.configure(api_key=API_KEY)

model = 'models/embedding-001'

def read_docx(file_path):
    """
    Lee el contenido de un archivo .docx y retorna su texto completo.
    """
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Lista de tus archivos .docx
file_paths = ['documents/Ventas.docx', 'documents/ADM-PRO-05 Adquisiciones por Administración Rev.4.docx']

# Crear un DataFrame vacío
df_docs = pd.DataFrame(columns=['Title', 'Text'])

# Leer cada archivo, extraer el contenido y añadirlo al DataFrame
for file_path in file_paths:
    text = read_docx(file_path)
    title = file_path.split('/')[-1]
    df_docs = df_docs._append({'Title': title, 'Text': text}, ignore_index=True)

df = pd.DataFrame(df_docs)

df.columns = ['Title', 'Text']

# Get the embeddings of each text and add to an embeddings column in the dataframe
def embed_fn(title, text, max_length=9000):
    # Asegúrate de que el texto no exceda el límite máximo de bytes
    if len(text.encode('utf-8')) > max_length:
        # Divide el texto en partes que estén dentro del límite
        parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        embeddings = []
        for part in parts:
            embedding = genai.embed_content(model=model,
                                             content=part,
                                             task_type="retrieval_document",
                                             title=title)["embedding"]
            embeddings.append(embedding)
            
        embeddings = np.array(embeddings)
        # Calcula el promedio a lo largo del eje 0 (columnas)
        avg_embedding = np.mean(embeddings, axis=0)
        return avg_embedding  
    else:
        return genai.embed_content(model=model,
                                   content=text,
                                   task_type="retrieval_document",
                                   title=title)["embedding"]

df['Embeddings'] = df.apply(lambda row: embed_fn(row['Title'], row['Text']), axis=1)
df.to_pickle('docs_embeddings.pkl')
