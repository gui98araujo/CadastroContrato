import streamlit as st
import pandas as pd
from datetime import datetime

# Função para calcular as colunas adicionais no DataFrame
def calcular_colunas(df):
    df['Preço Total'] = df.apply(lambda row: row['S.E.O'] + row['Prêmio / Desc.'] if row['Quantidade Fixada (tm)'] > 0 else 0, axis=1)
    df['Saldo a Fixar'] = df['Quantidade Vendida (tm)'] - df['Quantidade Fixada (tm)']
    df['Lotes a fixar'] = df['Saldo a Fixar'] / 50.8
    df['SEO x Quant. Fixadas'] = df['S.E.O'] * df['Quantidade Fixada (tm)']
    df['Prêmio x Quant. Fixadas'] = df['Prêmio / Desc.'] * df['Quantidade Fixada (tm)']
    df['Preço x Quant. Fixadas'] = df['Preço Total'] * df['Quantidade Fixada (tm)']
    df['Prêmio x Quant. Vendidas'] = df['Prêmio / Desc.'] * df['Quantidade Vendida (tm)']
    return df

# Função para exibir o DataFrame
def mostrar_dataframe(df):
    st.write(df)

# Cabeçalho do aplicativo
st.title('Cadastro de Contratos')

# Verificando se o DataFrame já existe na sessão
if 'Contrato' not in st.session_state:
    st.session_state['Contrato'] = pd.DataFrame(columns=['Comprador', 'Contrato', 'Quantidade Vendida (tm)', 'Mês de fixação', 'Quantidade Fixada (tm)',
                                                         'S.E.O', 'Prêmio / Desc.', 'Período de Embarque', 'Cessão'])

# Criando o formulário para capturar as informações
comprador = st.text_input('Comprador')
contrato = st.text_input('Contrato')
quantidade_vendida = st.number_input('Quantidade Vendida (tm)', step=0.1)
mes_fixacao = st.text_input('Mês de fixação')
quantidade_fixada = st.number_input('Quantidade Fixada (tm)', step=0.1)
seo = st.number_input('S.E.O', step=0.01)
premio_desc = st.number_input('Prêmio / Desc.', step=0.01)
periodo_embarque = st.date_input('Período de Embarque', (datetime.today(), datetime.today()))
cessao = st.text_input('Cessão (Opcional)')

# Botão para adicionar o contrato ao DataFrame
if st.button('Adicionar Contrato'):
    novo_contrato = pd.DataFrame({
        'Comprador': [comprador],
        'Contrato': [contrato],
        'Quantidade Vendida (tm)': [quantidade_vendida],
        'Mês de fixação': [mes_fixacao],
        'Quantidade Fixada (tm)': [quantidade_fixada],
        'S.E.O': [seo],
        'Prêmio / Desc.': [premio_desc],
        'Período de Embarque': [periodo_embarque],
        'Cessão': [cessao]
    })
    st.session_state['Contrato'] = pd.concat([st.session_state['Contrato'], novo_contrato], ignore_index=True)

# Exibindo o DataFrame atualizado
if 'Contrato' in st.session_state:
    st.write('DataFrame Atualizado:')
    df_atualizado = calcular_colunas(st.session_state['Contrato'].copy())
    mostrar_dataframe(df_atualizado)

# Selecionar contrato para exclusão
contratos_para_excluir = st.multiselect('Selecione contratos para excluir:', df_atualizado['Contrato'].unique())

# Botão para excluir contratos selecionados
if st.button('Excluir Contratos'):
    df_atualizado = df_atualizado[~df_atualizado['Contrato'].isin(contratos_para_excluir)]
    st.session_state['Contrato'] = df_atualizado

# Selecionar contrato para edição
contrato_para_editar = st.selectbox('Selecione contrato para editar:', df_atualizado['Contrato'].unique())

# Permitir edição das informações do contrato selecionado
if contrato_para_editar:
    st.write('Edite as informações do contrato selecionado:')
    contrato_index = df_atualizado[df_atualizado['Contrato'] == contrato_para_editar].index[0]
    contrato_selecionado = df_atualizado.iloc[contrato_index]
    contrato_selecionado['Comprador'] = st.text_input('Comprador', value=contrato_selecionado['Comprador'])
    contrato_selecionado['Quantidade Vendida (tm)'] = st.number_input('Quantidade Vendida (tm)', value=contrato_selecionado['Quantidade Vendida (tm)'], step=0.1)
    contrato_selecionado['Mês de fixação'] = st.text_input('Mês de fixação', value=contrato_selecionado['Mês de fixação'])
    contrato_selecionado['Quantidade Fixada (tm)'] = st.number_input('Quantidade Fixada (tm)', value=contrato_selecionado['Quantidade Fixada (tm)'], step=0.1)
    st.session_state['Contrato'].iloc[contrato_index] = contrato_selecionado
