import json
import os

from tabulate import tabulate


nombre = input("Nombre de la prenda: ")
color = input("Color de la prenda: ")
estado = input("Estado de la prenda (limpio/sucio): ")
formalidad_prenda = int(input("Formalidad de la prenda (1-10): "))
formalidad_ocasion = int(input("Formalidad de la ocasión (1-10): "))

if (
    formalidad_prenda < 1
    or formalidad_prenda > 10
    or formalidad_ocasion < 1
    or formalidad_ocasion > 10
):
    resultado = "Dato inválido"
elif estado.lower() == "sucio":
    resultado = "Rechazo 1: La prenda está sucia"
elif estado.lower() == "limpio" and abs(formalidad_prenda - formalidad_ocasion) > 2:
    resultado = "Rechazo 2: Diferencia de formalidad mayor a 2 puntos"
else:
    resultado = "Aceptado"

print(f"Decisión: {resultado}")

lista_prendas = []
if os.path.exists("datos.json"):
    with open("datos.json", "r", encoding="utf-8") as archivo:
        lista_prendas = json.load(archivo)

prenda = {
    "nombre": nombre,
    "color": color,
    "estado": estado,
    "formalidad_prenda": formalidad_prenda,
    "formalidad_ocasion": formalidad_ocasion,
    "resultado": resultado,
}
lista_prendas.append(prenda)

with open("datos.json", "w", encoding="utf-8") as archivo:
    json.dump(lista_prendas, archivo, ensure_ascii=False, indent=4)

print(tabulate(lista_prendas, headers="keys"))