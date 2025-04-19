#!/usr/bin/env python3
import sys
import pandas as pd
import os
import json
from datetime import datetime

# Función para buscar estudiantes por nombre parcial
def buscar_estudiantes(nombre_parcial, df):
    # Convertir a minúsculas para búsqueda no sensible a mayúsculas
    nombre_parcial = nombre_parcial.lower()
    # Filtrar estudiantes cuyo nombre contiene la cadena buscada
    resultados = df[df["Nombre"].str.lower().str.contains(nombre_parcial)]
    
    # Convertir a lista de diccionarios para JSON
    estudiantes = []
    for _, row in resultados.iterrows():
        estudiantes.append({
            "numero": int(row["Numero"]),
            "nombre": row["Nombre"]
        })
    
    return estudiantes

# Función para marcar asistencia por número de lista
def marcar_asistencia(numero_lista, df, archivo_excel):
    # Buscar el estudiante por número de lista
    estudiante = df[df["Numero"] == int(numero_lista)]
    
    if estudiante.empty:
        return {
            "success": False,
            "message": f"No se encontró ningún estudiante con el número {numero_lista}"
        }
    
    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    
    # Verificar si ya existe la columna para la fecha actual
    if fecha_actual not in df.columns:
        df[fecha_actual] = ""
    
    # Verificar si ya tiene asistencia marcada
    asistencia_actual = estudiante[fecha_actual].values[0]
    if asistencia_actual == "✓":
        return {
            "success": True,
            "message": "Ya tienes asistencia registrada para hoy",
            "nombre": estudiante["Nombre"].values[0],
            "numero": int(numero_lista),
            "fecha": fecha_actual,
            "ya_registrado": True
        }
    
    # Marcar asistencia
    df.loc[df["Numero"] == int(numero_lista), fecha_actual] = "✓"
    
    # Guardar el archivo
    df.to_excel(archivo_excel, index=False)
    
    # Obtener el nombre del estudiante
    nombre_estudiante = estudiante["Nombre"].values[0]
    
    return {
        "success": True,
        "message": f"Asistencia registrada para {nombre_estudiante}",
        "nombre": nombre_estudiante,
        "numero": int(numero_lista),
        "fecha": fecha_actual,
        "ya_registrado": False
    }

# Función principal
def main():
    # Verificar el modo de operación
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "message": "Error: Operación no especificada"}))
        sys.exit(1)
    
    modo = sys.argv[1]
    
    try:
        # Ruta del archivo Excel (ajusta según tu ubicación)
        archivo_excel = os.path.expanduser("~/asistencia.xlsx")
        
        # Cargar el archivo Excel
        try:
            df = pd.read_excel(archivo_excel)
        except FileNotFoundError:
            print(json.dumps({"success": False, "message": "Error: El archivo de asistencia no existe"}))
            sys.exit(1)
        
        # Modo de búsqueda de estudiantes
        if modo == "buscar" and len(sys.argv) >= 3:
            nombre_parcial = sys.argv[2]
            estudiantes = buscar_estudiantes(nombre_parcial, df)
            print(json.dumps({"success": True, "estudiantes": estudiantes}))
        
        # Modo de marcar asistencia
        elif modo == "marcar" and len(sys.argv) >= 3:
            numero_lista = sys.argv[2]
            resultado = marcar_asistencia(numero_lista, df, archivo_excel)
            print(json.dumps(resultado))
        
        else:
            print(json.dumps({"success": False, "message": "Error: Operación no válida o parámetros insuficientes"}))
            sys.exit(1)
        
    except Exception as e:
        print(json.dumps({"success": False, "message": f"Error inesperado: {str(e)}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()