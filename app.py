# Copyright (c) 2023, Francisco Ruiz
#
# This code is copyrighted and may not be redistributed or used without
# the express written permission of the author.

import os
import dotenv
import openai
import streamlit as st

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Comparador de Contratos")
st.write('''A continuación introduzca el texto de los contratos que desee comparar,
          cada uno en su respectivo campo, luego presione el botón "Comparar" y 
         aguarde por la respuesta de la IA. Este proceso podría demorar unos minutos''')

text1 = st.text_area("Exclusiones del 1er Contrato", height=200)
text2 = st.text_area("Exclusiones del 2do Contrato", height=200)
compare = st.button("Comparar")

def comparar_contratos(text1, text2):
    response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "system", "content": "You are a helpfull insurance underwriter."},
              {"role": "user", "content": """
                Compara los textos que están entre comillas: "{text1}" y "{text2}".
                Teniendo en cuenta de que son contratos y pueden tener terminos que
                se escriban diferente pero expresen lo mismo. Señálame las diferencias
                y similitudes entre las expresiones que se escriben diferente pero
                significan lo mismo. Explica porque son diferentes o iguales en cada caso.
                Indicame si en general los textos son diferentes o si expresan lo mismo
              """.format(text1=text1, text2=text2)}
          ]
      )
    return response["choices"][0]["message"]["content"] + "Total de Tokens utilizados en esta consulta: " +  str(response["usage"]["total_tokens"])


if compare:
    st.write(comparar_contratos(text1, text2))
else:
    st.write('Aquí se mostrará la respuesta de la IA')