#!/usr/bin/env python3
import sys
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

ARCHIVO_EXCEL = Path.home() / "asistencia.xlsx"

def cargar_datos():
    if not ARCHIVO_EXCEL.exists():
        sys.exit(json.dumps({"success": False, "message": "El archivo de asistencia no existe"}))
    return pd.read_excel(ARCHIVO_EXCEL)

def buscar(nombre, df):
    coincidencias = df[df["Nombre"].str.contains(nombre, case=False, na=False)]
    estudiantes = [{"nombre": row["Nombre"]} for _, row in coincidencias.iterrows()]
    print(json.dumps({"success": True, "estudiantes": estudiantes}))

def marcar(nombre, df):
    fila = df[df["Nombre"].str.lower() == nombre.lower()]
    if fila.empty:
        print(json.dumps({"success": False, "message": f"No se encontró a '{nombre}'"}))
        return

    fecha = datetime.now().strftime("%Y-%m-%d")
    if fecha not in df.columns:
        df[fecha] = ""

    if fila.iloc[0][fecha] == "✓":
        print(json.dumps({
            "success": True,
            "message": "Asistencia ya registrada",
            "nombre": fila.iloc[0]["Nombre"],
            "fecha": fecha,
            "ya_registrado": True
        }))
        return

    df.loc[fila.index, fecha] = "✓"
    df.to_excel(ARCHIVO_EXCEL, index=False)

    print(json.dumps({
        "success": True,
        "message": f"Asistencia registrada para {fila.iloc[0]['Nombre']}",
        "nombre": fila.iloc[0]["Nombre"],
        "fecha": fecha,
        "ya_registrado": False
    }))

def main():
    if len(sys.argv) < 3:
        sys.exit(json.dumps({"success": False, "message": "Uso: script.py [buscar|marcar] 'Nombre del Alumno'"}))

    modo, nombre = sys.argv[1], sys.argv[2]
    df = cargar_datos()

    if modo == "buscar":
        buscar(nombre, df)
    elif modo == "marcar":
        marcar(nombre, df)
    else:
        print(json.dumps({"success": False, "message": "Operación no válida"}))

if __name__ == "__main__":
    main()
