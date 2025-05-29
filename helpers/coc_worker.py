import unicodedata
import pandas as pd
from .data_wrestler import highlight_total_row_leadsByUser, highlight_total_row_leadsByStore, highlight_total_row
import streamlit as st
from datetime import time

def normalize_name(name: str) -> str:
    """Normaliza nomes: remove espaços extras, acentos e capitaliza."""
    if not isinstance(name, str):
        return ""
    name = name.strip()                       # remove espaços extras
    name = " ".join(name.split())             # remove espaços duplos internos
    name = unicodedata.normalize('NFKD', name)
    name = name.encode('ASCII', 'ignore').decode('utf-8')  # remove acentos
    name = name.title()                       # capitaliza cada palavra
    return name

def apply_formatting_leadsByUser(df, hora_atual):
    def get_threshold(hora):
        if time(8, 0, 0) <= hora <= time(11, 59, 0):
            return 50
        elif time(12, 0, 0) <= hora <= time(13, 59, 0):
            return 100
        elif time(14, 0, 0) <= hora <= time(16, 59, 0):
            return 150
        elif time(17, 0, 0) <= hora <= time(20, 30, 0):
            return 200
        else:
            return None  # Fora dos intervalos definidos

    threshold = get_threshold(hora_atual)
    styles = df.style.apply(highlight_total_row_leadsByUser, axis=1)
    if 'Leads Puxados' in df.columns and threshold is not None:
        styles = styles.applymap(
            lambda v: 'color: red' if isinstance(v, (int, float)) and v < threshold else (
                'color: green' if isinstance(v, (int, float)) and v >= threshold else ''
            ),
            subset=['Leads Puxados']
        )
    return styles.format({
        'Leads Puxados': '{:.0f}',
        'Leads Puxados (únicos)': '{:.0f}',
        'Agendamentos por lead': '{:.0f}',
        'Agendamentos na Agenda': '{:.0f}'
    })

def apply_formatting_followUpReport(df):
    # Define formatos esperados
    all_formats = {
        'Valor líquido': '{:.2f}',
        'Novos Pós-Vendas': '{:.0f}',
        'Comentários de Pós-Vendas': '{:.0f}',
        'Pedidos': '{:.0f}'
    }
    
    # Filtra os que existem no DataFrame
    existing_formats = {col: fmt for col, fmt in all_formats.items() if col in df.columns}
    
    return df.style.apply(highlight_total_row, axis=1).format(existing_formats)

def apply_formatting_leadsByStore(df):
    return df.style.apply(highlight_total_row_leadsByStore, axis=1).format({
                        'Leads Puxados': '{:.0f}',
                        'Agendamentos por lead': '{:.0f}',
                        'Agendamentos na Agenda': '{:.0f}'
                    })