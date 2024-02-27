import streamlit as st
import pandas as pd

# Função para calcular os campos derivados
def calcular_campos(df):
    df['Preço Total'] = df.apply(lambda row: row['S. E. O'] + row['Prêmio / Desc.'] if row['Quantidade Fixada'] > 0 else 0, axis=1)
    df['Saldo a Fixar'] = df['QTD. VENDIDA'] - df['Quantidade Fixada']
    df['Lotes a fixar'] = df['Saldo a Fixar'] / 50.8
    df['SEO x Quant. Fixadas'] = df['S. E. O'] * df['Quantidade Fixada']
    df['Prêmio x Quant. Fixadas'] = df['Prêmio / Desc.'] * df['Quantidade Fixada']
    df['Preço x Quant. Fixadas'] = df['Preço Total'] * df['Quantidade Fixada']
    df['Prêmio x Quant. Vendidas'] = df['Prêmio / Desc.'] * df['QTD. VENDIDA']
    return df

# Verificar se o arquivo CSV já existe, se não, criar um DataFrame vazio
try:
    df = pd.read_csv('contratos.csv')
except FileNotFoundError:
    df = pd.DataFrame(columns=['COMPRADOR', 'CONTRATO', 'QTD. VENDIDA', 'MÊS DE FIXAÇÃO', 'Quantidade Fixada', 'S. E. O', 'Prêmio / Desc.', 'PERÍODO DE EMBARQUE', 'Cessão', 'Preço Total', 'Saldo a Fixar', 'Lotes a fixar', 'SEO x Quant. Fixadas', 'Prêmio x Quant. Fixadas', 'Preço x Quant. Fixadas', 'Prêmio x Quant. Vendidas'])

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
    novo_contrato = pd.DataFrame({'COMPRADOR': [comprador], 'CONTRATO': [contrato], 'QTD. VENDIDA': [qtd_vendida], 'MÊS DE FIXAÇÃO': [mes_fixacao], 'Quantidade Fixada': [quantidade_fixada], 'S. E. O': [seo], 'Prêmio / Desc.': [premio_desc], 'PERÍODO DE EMBARQUE': [periodo_embarque], 'Cessão': [cessao], 'Preço Total': [0], 'Saldo a Fixar': [0], 'Lotes a fixar': [0], 'SEO x Quant. Fixadas': [0], 'Prêmio x Quant. Fixadas': [0], 'Preço x Quant. Fixadas': [0], 'Prêmio x Quant. Vendidas': [0]})
    df = pd.concat([df, novo_contrato], ignore_index=True)
    df = calcular_campos(df)
    df.to_csv('contratos.csv', index=False)
    st.success('Contrato cadastrado com sucesso!')

# Página de mudança de contrato
st.title('Mudança de Contrato')

contrato_selecionado = st.text_input('Digite o contrato a ser alterado')
contrato_info = df[df['CONTRATO'] == contrato_selecionado]

if not contrato_info.empty:
    st.write('Informações do contrato selecionado:')
    st.write(contrato_info)

    colunas_para_alterar = st.multiselect('Selecione as colunas para alterar', contrato_info.columns)

    if st.button('Alterar'):
        for coluna in colunas_para_alterar:
            novo_valor = st.text_input(f'Novo valor para {coluna}')
            contrato_info[coluna] = novo_valor

        df[df['CONTRATO'] == contrato_selecionado] = contrato_info
        df = calcular_campos(df)
        df.to_csv('contratos.csv', index=False)
        st.success('Contrato alterado com sucesso!')

else:
    st.warning('Contrato não encontrado.')

# Página de visualização e download de arquivos
st.title('Visualização e Download de Arquivos')

st.write(df)

st.write('Para fazer o download do arquivo CSV, clique no link abaixo:')
st.markdown('[Download CSV](contratos.csv)')
