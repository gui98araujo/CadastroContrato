import streamlit as st
import pandas as pd

# Verificar se o arquivo CSV já existe, se não, criar um DataFrame vazio
try:
    df = pd.read_csv('contratos.csv')
except FileNotFoundError:
    df = pd.DataFrame(columns=['Comprador', 'Contrato', 'QTD. VENDIDA', 'Mês de Fixação', 'Quantidade Fixada', 'S. E. O', 'Prêmio / Desc.', 'Período de Embarque', 'Cessão'])
    st.write('Criado DataFrame vazio')

# Página de cadastro de contrato
st.title('Cadastro de Contrato')

comprador = st.text_input('Comprador')
contrato = st.text_input('Contrato')
qtd_vendida = st.number_input('Quantidade Vendida (tm)', min_value=0.0)
mes_fixacao = st.text_input('Mês de Fixação')
quantidade_fixada = st.number_input('Quantidade Fixada (tm)', min_value=0.0)
seo = st.number_input('S. E. O', min_value=0.0)
premio_desc = st.number_input('Prêmio / Desc.', min_value=0.0)
periodo_embarque = st.date_input('Período de Embarque', (pd.to_datetime('today'), pd.to_datetime('today')))
cessao = st.text_input('Cessão (opcional)')

if st.button('Concluir Cadastro'):
    novo_contrato = pd.DataFrame({'Comprador': [comprador], 'Contrato': [contrato], 'QTD. VENDIDA': [qtd_vendida], 'Mês de Fixação': [mes_fixacao], 'Quantidade Fixada': [quantidade_fixada], 'S. E. O': [seo], 'Prêmio / Desc.': [premio_desc], 'Período de Embarque': [periodo_embarque], 'Cessão': [cessao]})
    df = pd.concat([df, novo_contrato], ignore_index=True)
    st.success('Contrato cadastrado com sucesso!')

# Página de mudança de contrato
st.title('Mudança de Contrato')

contrato_selecionado = st.text_input('Digite o contrato a ser alterado')
st.write('Colunas presentes no DataFrame:', df.columns)  # Mensagem de depuração
if 'Contrato' in df.columns:  # Verifica se a coluna 'Contrato' está presente
    contrato_info = df[df['Contrato'] == contrato_selecionado]
else:
    contrato_info = pd.DataFrame()
    st.write('A coluna "Contrato" não está presente no DataFrame.')  # Mensagem de depuração

if not contrato_info.empty:
    st.write('Informações do contrato selecionado:')
    st.write(contrato_info)

    colunas_para_alterar = st.multiselect('Selecione as colunas para alterar', contrato_info.columns)

    if st.button('Alterar'):
        for coluna in colunas_para_alterar:
            novo_valor = st.text_input(f'Novo valor para {coluna}')
            contrato_info[coluna] = novo_valor

        df[df['Contrato'] == contrato_selecionado] = contrato_info
        df.to_csv('contratos.csv', index=False)
        st.success('Contrato alterado com sucesso!')

else:
    st.warning('Contrato não encontrado ou a coluna "Contrato" não está presente.')

# Página de visualização e download de arquivos
st.title('Visualização e Download de Arquivos')

st.write(df)

st.write('Para fazer o download do arquivo CSV, clique no link abaixo:')
st.markdown('[Download CSV](contratos.csv)')
