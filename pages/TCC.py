import streamlit as st
from docx import Document
from openai import OpenAI
from io import BytesIO

# 2. Configuração da API do OpenAI
chave = st.secrets["KEY"]
client = OpenAI(api_key=chave)

# Configuração da chave API da OpenAI
#openai.api_key = st.secrets["KEY"]


def extract_text_from_docx(uploaded_file):
    try:
        # Use BytesIO para abrir o arquivo como um documento do Word
        doc = Document(BytesIO(uploaded_file.getvalue()))
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return e

def retrieve_information(documents, query):
    # Implementação de uma busca simples nos documentos
    return "Informação relevante extraída dos documentos"

def generate_text_with_context(context, prompt):
    full_prompt = f"{context}\n\n{prompt}"
    try:
        # Uso correto da API de chat completions
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",  
            messages=[
                {"role": "system", "content": "Você será um especialista em criar artefatos de licitação Documento de Formalização da Demanda (DFD),Estudo Técnico Preliminar (ETP) e Termo de Referência (TR) "},
                {"role": "user", "content": full_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro ao gerar texto com o chat: {e}")
        return e


# Configuração da Interface Streamlit
st.title('Sistema de Automatização do Artefatos de contratação com RAG')

# Carregamento de Modelos de Documentos
st.header("Carregue seus modelos de documentos")
model_files = st.file_uploader("Escolha os modelos (arquivos Word)", accept_multiple_files=True, type='docx', key='models')

# Carregamento de Documentos de Conhecimento Adicional
st.header("Carregue documentos para a base de conhecimento adicional")
knowledge_files = st.file_uploader("Escolha documentos de conhecimento (arquivos Word, PDF, etc.)", accept_multiple_files=True, type=['docx', 'pdf'], key='knowledge')

# Entrada de prompt do usuário
st.header("Digite seu prompt")
user_query = st.text_input("Digite sua consulta")

if st.button('Gerar Resposta'):
    if model_files and user_query:
        # Processamento dos modelos de documentos
        model_content = [extract_text_from_docx(file) for file in model_files]
        # Processamento dos documentos de conhecimento adicional
        knowledge_content = [extract_text_from_docx(file) for file in knowledge_files] if knowledge_files else []

        # Combinação de conteúdos dos modelos e conhecimento adicional
        combined_content = "\n".join(model_content + knowledge_content)

        # Recuperação de informações baseada em todos os documentos carregados
        relevant_info = retrieve_information(combined_content, user_query)

        # Geração de texto com o prompt enriquecido
        answer = generate_text_with_context(relevant_info, user_query)
        st.write("Resposta:", answer)
    else:
        st.write("Por favor, carregue pelo menos um modelo de documento e digite uma consulta.")

