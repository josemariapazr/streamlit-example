import textwrap
import numpy as np
import pandas as pd
import time

import google.generativeai as genai
import google.ai.generativelanguage as glm

from IPython.display import Markdown
from docx import Document
import ast

API_KEY = 'AIzaSyBqoe55dpaKzIu-dVhVc004JDsbXqWgFbY'
genai.configure(api_key=API_KEY)

model = 'models/embedding-001'

df_loaded = pd.read_pickle('docs_embeddings.pkl')

def find_best_passage(query, dataframe):
  """
  Compute the distances between the query and each document in the dataframe
  using the dot product.
  """
  query_embedding = genai.embed_content(model=model,
                                        content=query,
                                        task_type="retrieval_query")
  dot_products = np.dot(np.stack(dataframe['Embeddings']), query_embedding["embedding"])
  idx = np.argmax(dot_products)
  return dataframe.iloc[idx]['Text'] # Return text from index with max value


def make_prompt(query, relevant_passage):
  escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
  prompt = textwrap.dedent("""Como un bot altamente capacitado y especializado en las políticas y reglamentaciones de DATEC Ltda., tu misión es ofrecer respuestas claras y precisas basadas en el pasaje de referencia suministrado. Utiliza el texto provisto para construir un párrafo explicativo completo, asegurándote de incorporar todos los detalles pertinentes que puedan ayudar a esclarecer la consulta. Es crucial que tu respuesta:\Sea exhaustiva y abarque todos los aspectos relevantes.\Esté redactada en español, con claridad y precisión lingüística.\Evalúe la pertinencia del pasaje dado y, en caso de ser irrelevante, ajuste la respuesta de manera acorde.

  La pregunta a resolver es la siguiente:
  PREGUNTA: '{query}'
  
  El pasaje de referencia proporcionado es:
  PASAJE: '{relevant_passage}'
  
  Con base en este contexto, por favor, elabora tu respuesta a continuación:
  
  RESPUESTA:
  """).format(query=query, relevant_passage=escaped)

  return prompt

import traceback

def generar_respuesta(query, intentos=3):
    for intento in range(intentos):
        try:
            # Aquí realizamos la operación que podría fallar.
            passage = find_best_passage(query, df_loaded)
            prompt = make_prompt(query, passage)
            
            model = genai.GenerativeModel('gemini-pro')
            answer = model.generate_content(prompt,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=2048,
                    temperature=0.5,
                    top_p=1)
            )
            return answer.text
        
        except Exception as e:
            print(f"Error al generar la respuesta, intento {intento + 1} de {intentos}. Error: {e}")
            traceback.print_exc()
            time.sleep(2)  # Espera 2 segundos antes de reintentar

            if intento == intentos - 1:
                return "Lo siento, ocurrió un error al procesar tu solicitud. Por favor, inténtalo de nuevo más tarde."

#def generar_respuesta(query):

    #model = 'models/embedding-001'

    #request = genai.embed_content(model=model,
     #                             content=query,
      #                            task_type="retrieval_query")

    #passage = find_best_passage(query, df_loaded)
    #prompt = make_prompt(query, passage)

    #model = genai.GenerativeModel('gemini-pro')

    #answer = model.generate_content(prompt,
     #   generation_config=genai.types.GenerationConfig(
            # Only one candidate for now.
      #      candidate_count=1,
            #stop_sequences=['x'],
       #     max_output_tokens=2048,
        #    temperature=0.5,
         #   top_p=1)
    #)

    return answer.text

#Markdown(answer.text)

