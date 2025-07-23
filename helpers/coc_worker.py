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

def apply_formatting_leadsByUser_manha(df, hora_atual):
    def get_threshold(hora):
        if time(11, 0, 0) <= hora <= time(14, 59, 0): # 11:00 até 14:59
            return 33
        elif time(15, 0, 0) <= hora <= time(18, 59, 0): # 15:00 até 18:59
            return 55
        elif time(19, 0, 0) <= hora <= time(23, 30, 0): # 19:00 até 23:30
            return 90
        else:
            return None

    threshold = get_threshold(hora_atual)
    styles = df.style.apply(highlight_total_row_leadsByUser, axis=1)

    # Aplicação condicional de cores para 'Leads Puxados'
    if 'Leads Puxados' in df.columns and threshold is not None:
        styles = styles.applymap(
            lambda v: 'color: red' if isinstance(v, (int, float)) and v < threshold else (
                'color: green' if isinstance(v, (int, float)) and v >= threshold else ''
            ),
            subset=['Leads Puxados']
        )

    # Aplicando cores para a coluna 'Conversão'
    if 'Conversão' in df.columns:
        df['Conversão'] = pd.to_numeric(df['Conversão'], errors='coerce')
        
        def color_conversion(val):
            if isinstance(val, (int, float)):
                if val < 0.05:
                    return 'color: red'
                elif val >= 0.05:
                    return 'color: green'
            return ''

        styles = styles.applymap(color_conversion, subset=['Conversão'])

    return styles.format({
        'Leads Puxados': '{:.0f}',
        'Leads Puxados (únicos)': '{:.0f}',
        'Agendamentos por lead': '{:.0f}',
        'Agendamentos na Agenda': '{:.0f}',
        'Total De Agendamentos': '{:.0f}',
        'Conversão': '{:.2%}'
    })

def apply_formatting_leadsByUser_tarde(df, hora_atual):
    def get_threshold(hora):
        if time(11, 0, 0) <= hora <= time(14, 59, 0): # 08:00 até 11:59 
            return 0
        elif time(15, 0, 0) <= hora <= time(18, 59, 0): # 12:00 até 16:00
            return 33
        elif time(19, 0, 0) <= hora <= time(23, 30, 0): # 16:00 até 20:30
            return 55
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
    # Aplicando cores para a coluna 'Conversão'
    if 'Conversão' in df.columns:
        df['Conversão'] = pd.to_numeric(df['Conversão'], errors='coerce')
        
        def color_conversion(val):
            if isinstance(val, (int, float)):
                if val < 0.05:
                    return 'color: red'
                elif val >= 0.05:
                    return 'color: green'
            return ''

        styles = styles.applymap(color_conversion, subset=['Conversão'])

    return styles.format({
        'Leads Puxados': '{:.0f}',
        'Leads Puxados (únicos)': '{:.0f}',
        'Agendamentos por lead': '{:.0f}',
        'Agendamentos na Agenda': '{:.0f}',
        'Total De Agendamentos': '{:.0f}',
        'Conversão': '{:.2%}'
    })

def apply_formatting_leadsByUser_fechamento(df, hora_atual):
    def get_threshold(hora):
        if time(11, 0, 0) <= hora <= time(14, 59, 0): # 08:00 até 11:59 
            return 90
        elif time(15, 0, 0) <= hora <= time(18, 59, 0): # 12:00 até 16:00
            return 90
        elif time(19, 0, 0) <= hora <= time(23, 30, 0): # 16:00 até 20:30
            return 90
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
    # Aplicando cores para a coluna 'Conversão'
    if 'Conversão' in df.columns:
        df['Conversão'] = pd.to_numeric(df['Conversão'], errors='coerce')
        
        def color_conversion(val):
            if isinstance(val, (int, float)):
                if val < 0.05:
                    return 'color: red'
                elif val >= 0.05:
                    return 'color: green'
            return ''

        styles = styles.applymap(color_conversion, subset=['Conversão'])

    return styles.format({
        'Leads Puxados': '{:.0f}',
        'Leads Puxados (únicos)': '{:.0f}',
        'Agendamentos por lead': '{:.0f}',
        'Agendamentos na Agenda': '{:.0f}',
        'Total De Agendamentos': '{:.0f}',
        'Conversão': '{:.2%}'
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