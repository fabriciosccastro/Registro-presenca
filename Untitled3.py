#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
from datetime import datetime

# Caminho dos arquivos
caminho_base = 'C:/Users/USUARIO/Downloads/'

# Carregar os dados
@st.cache_data
def carregar_dados():
    estrutura_df = pd.read_excel(caminho_base + 'Estrutura.xlsx', engine='openpyxl')
    usuarios_df = pd.read_excel(caminho_base + 'Usuarios.xlsx', engine='openpyxl')
    return estrutura_df, usuarios_df

estrutura_df, usuarios_df = carregar_dados()

# Interface do Streamlit
st.title("Registro de Presença")

# Seleção de Unidade
unidade = st.selectbox("Unidade:", estrutura_df['unidade'].unique())

# Filtragem de Produto
produtos_filtrados = estrutura_df[estrutura_df['unidade'] == unidade]['produto'].unique()
produto = st.selectbox("Produto:", produtos_filtrados)

# Filtragem de Atividade
atividades_filtradas = estrutura_df[(estrutura_df['unidade'] == unidade) & 
                                    (estrutura_df['produto'] == produto)]['atividade'].unique()
atividade = st.selectbox("Atividade:", atividades_filtradas)

# Filtragem de Turma
turmas_filtradas = estrutura_df[(estrutura_df['unidade'] == unidade) & 
                                (estrutura_df['produto'] == produto) & 
                                (estrutura_df['atividade'] == atividade)]['turma'].unique()
turma = st.selectbox("Turma:", turmas_filtradas)

# Filtragem de Usuários
usuarios_filtrados = usuarios_df[usuarios_df['turma'] == turma]['nome_cliente'].unique()
usuarios_selecionados = st.multiselect("Usuários:", usuarios_filtrados)

# Função para registrar presença
def registrar_presenca(novo_usuario=None, novo_cpf=None):
    data_hora_atual = datetime.now()
    data_atual = data_hora_atual.strftime("%Y-%m-%d")
    hora_atual = data_hora_atual.strftime("%H:%M:%S")
    
    registros = []
    
    # Se houver um novo usuário manual
    if novo_usuario:
        registros.append({
            'Unidade': unidade,
            'Produto': produto,
            'Atividade': atividade,
            'Turma': turma,
            'Usuário': novo_usuario,
            'CPF': novo_cpf,
            'Data': data_atual,
            'Hora': hora_atual
        })
    
    # Se houver usuários selecionados na lista
    for usuario in usuarios_selecionados:
        registros.append({
            'Unidade': unidade,
            'Produto': produto,
            'Atividade': atividade,
            'Turma': turma,
            'Usuário': usuario,
            'CPF': '',  # Usuários da lista não têm CPF informado
            'Data': data_atual,
            'Hora': hora_atual
        })
    
    # Carregar o arquivo existente ou criar um novo
    try:
        registros_df = pd.read_excel(caminho_base + 'Bd_registros.xlsx', engine='openpyxl')
    except FileNotFoundError:
        registros_df = pd.DataFrame(columns=['Unidade', 'Produto', 'Atividade', 'Turma', 'Usuário', 'CPF', 'Data', 'Hora'])
    
    # Adicionar os novos registros
    registros_df = pd.concat([registros_df, pd.DataFrame(registros)], ignore_index=True)
    registros_df.to_excel(caminho_base + 'Bd_registros.xlsx', index=False, engine='openpyxl')
    
    st.success("Presença registrada com sucesso!")

# Botão de registro
if st.button("Registrar Presença"):
    if usuarios_selecionados:
        registrar_presenca()
    else:
        st.warning("Selecione pelo menos um usuário para registrar presença.")

# Botão para adicionar novo usuário manualmente
with st.expander("Adicionar Usuário Manualmente"):
    novo_usuario = st.text_input("Nome do Usuário:")
    novo_cpf = st.text_input("CPF do Usuário:")
    
    if st.button("Adicionar Usuário e Registrar Presença"):
        if novo_usuario and novo_cpf:
            registrar_presenca(novo_usuario, novo_cpf)
        else:
            st.warning("Por favor, preencha todos os campos.")


