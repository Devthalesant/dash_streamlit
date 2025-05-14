import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime, timedelta
import asyncio
from frontend.marketing.leads_cleaner import (
                    paid_sources, 
                    organic_sources, 
                    stores_to_remove_leads)
                    
#from components.headers import header_leads
#from frontend.leads.lead_category import process_lead_categories

from apiCrm.resolvers.dashboard.fetch_leadReport import fetch_and_process_lead_report
from components.date_input import date_input
from helpers.discord import send_discord_message

def load_data(start_date=None, end_date=None, use_api=False):
    """
    Load and preprocess leads data.
    
    Args:
        start_date (str, optional): Start date in YYYY-MM-DD format for API fetch
        end_date (str, optional): End date in YYYY-MM-DD format for API fetch
        use_api (bool): Whether to use the API or local Excel file
        
    Returns:
        DataFrame: Processed leads dataframe
    """
    if start_date and end_date:
        try:
            # Run the async function using asyncio
            leads_data = asyncio.run(fetch_and_process_lead_report(start_date, end_date))
            
            if not leads_data:
                st.error("Não foi possível obter dados da API. Usando dados locais.")
                return load_data(start_date, end_date, use_api=False)
            
            # Convert the API data to a DataFrame
            df = pd.DataFrame(leads_data)
            
            # Map API field names to match the excel structure
            df = df.rename(columns={
                'id': 'ID do lead',
                'name': 'Nome',
                'email': 'Email',
                'telephone': 'Telefone',
                'message': 'Mensagem',
                'createdAt': 'Dia da entrada',
                'store': 'Unidade',
                'source': 'Fonte',
                'status': 'Status',
                'utmSource': 'utmSource',
                'utmMedium': 'utmMedium',
                'utmTerm': 'utmTerm',
                'utmContent': 'Content',
                'utmCampaign': 'utmCampaign',
                'searchTerm': 'searchTerm'
            })
            
            # Convert createdAt to datetime
            df['Dia da entrada'] = pd.to_datetime(df['Dia da entrada'])
            
            # Format the date for 'Dia' column (single step)
            df['Dia'] = df['Dia da entrada'].dt.strftime('%d-%m-%Y')
            
            st.success(f"Dados obtidos com sucesso via API: {len(df)} leads carregados.")
            
        except Exception as e:
            st.error(f"Erro ao buscar dados da API: {str(e)}")
            return load_data(use_api=False)
    else:
        st.warning("Por favor, selecione um intervalo de datas.")
        return pd.DataFrame()
        
    # Apply common transformations
    df = df.loc[~df['Unidade'].isin(stores_to_remove_leads)]
    
    return df

def create_time_filtered_df(df, days=None):
    """Create a time-filtered dataframe."""
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        return df[df['Dia da entrada'] >= cutoff_date]
    return df

def load_page_funil():
    """Main function to display leads data."""    

    st.title("📊 1 - Funil")
    st.markdown("---")
    st.subheader("Selecione o intervalo de datas para o relatório:")
    
    start_date, end_date = date_input()
    
    if st.button("Carregar"):
        send_discord_message(f"Loading data in page funil")
        with st.spinner("Carregando dados..."):
            df_leads = load_data(start_date, end_date)
            st.dataframe(df_leads)