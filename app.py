# Copyright (c) 2023, Francisco Ruiz
#
# This code is copyrighted and may not be redistributed or used without
# the express written permission of the author.

import os
import dotenv
import openai
import streamlit as st

dotenv.load_dotenv()
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Comparador de Contratos")
st.write('''A continuación introduzca el texto de los contratos que desee comparar,
          cada uno en su respectivo campo, luego presione el botón "Comparar" y 
         aguarde por la respuesta de la IA. Este proceso podría demorar unos minutos.''')
st.caption('''Por el momento la aplicación se encuentra limitada a 1000 palabras en cada campo, 
           por lo que podría utilizarse para comparar las secciones de exclusión o coberturas 
           de los contratos, por secciones.''')

text1 = st.text_area("Texto del 1er Contrato", height=200)
text2 = st.text_area("Texto del 2do Contrato", height=200)
compare = st.button("Comparar")

def comparar_contratos(text1, text2):
    response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "system", "content": """You are a professional insurance underwriter, 
              always respond in spanish."""},
              {"role": "user", "content": """
                Compare and contrast two fragments of insurance contracts, highlighting their key features, 
                benefits, and limitations. Provide a comprehensive analysis of the similarities 
                and differences between the two contracts, and explain how these factors can 
                impact an individual's decision when choosing insurance coverage. Additionally, 
                discuss any specific considerations or factors that should be taken into account 
                when comparing insurance contracts in order to make an informed decision. 
                Give a short answer if the are not significant diferences:
                 '{text1}' and '{text2}'. 
              """.format(text1=text1, text2=text2)}
          ]
          temperature=0.1
      )
    return response["choices"][0]["message"]["content"] + "\n Total de Tokens utilizados en esta consulta: " +  str(response["usage"]["total_tokens"])


if compare:
    st.write(comparar_contratos(text1, text2))
else:
    st.caption('Aquí se mostrará la respuesta de la IA')