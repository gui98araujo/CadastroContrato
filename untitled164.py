import streamlit as st
import pandas as pd
from datetime import datetime
import base64

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

# Carregar dados do arquivo CSV se existir
try:
    df_contrato = pd.read_csv('contratos.csv')
except FileNotFoundError:
    df_contrato = pd.DataFrame(columns=['Comprador', 'Contrato', 'Quantidade Vendida (tm)', 'Mês de fixação', 'Quantidade Fixada (tm)',
                                         'S.E.O', 'Prêmio / Desc.', 'Período de Embarque', 'Cessão'])

# Verificando se o DataFrame já existe na sessão
if 'Contrato' not in st.session_state:
    st.session_state['Contrato'] = df_contrato

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
if 'Contrato' in st.session_state:
    contratos_para_excluir = st.multiselect('Selecione contratos para excluir:', df_atualizado['Contrato'].tolist())

    # Obter índices correspondentes aos contratos selecionados
    indices_para_excluir = df_atualizado[df_atualizado['Contrato'].isin(contratos_para_excluir)].index.tolist()

    # Botão para excluir contratos selecionados
    if st.button('Excluir Contratos'):
        df_atualizado = df_atualizado.drop(indices_para_excluir, axis=0)
        st.session_state['Contrato'] = df_atualizado

# Salvar DataFrame no arquivo CSV
if 'Contrato' in st.session_state:
    st.session_state['Contrato'].to_csv('contratos.csv', index=False)

# Botão para baixar DataFrame em Excel
if 'Contrato' in st.session_state:
    def download_excel(df):
        df.to_excel('contratos.xlsx', index=False)
        with open('contratos.xlsx', 'rb') as f:
            data = f.read()
        return data

    excel_data = download_excel(df_atualizado)
    b64 = base64.b64encode(excel_data).decode('utf-8')
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="contratos.xlsx">Baixar DataFrame em Excel</a>'
    st.markdown(href, unsafe_allow_html=True)
