from flask import Flask, request, render_template, redirect, url_for
import random

app = Flask(__name__)

# Participantes y restricciones
participantes = [
    "Maxi", "Fabri", "Tenshi", "Luci", "Alejo","Sofi","Rodri","Luaty","Lucho","Benjiwis","Eliseo","Sol","Naty","Kati"
]

restricciones = {
    "Maxi":["Maxi", "Luci","Sofi","Rodri","Lucho","Benjiwis","Sol","Naty","Kati"],
    "Fabri":["Fabri"],
    "Tenshi":["Tenshi", "Alejo","Eliseo","Sol","Naty","Kati"],
    "Lucí":["Maxi","Luci","Eliseo","Sol","Naty","Kati"],
    "Alejo":["Maxi","Alejo","Sol","Naty","Kati"],
    "Sofi":["Maxi", "Sofi"],
    "Rodri":["Maxi", "Tenshi","Rodri","Sol","Naty","Kati"],
    "Luaty":["Lauty","Sol","Naty","Kati"],
    "Lucho":["Maxi","Lucho","Sol","Naty","Kati"],
    "Benjiwis":["Maxi","Tenshi","Lucho","Eliseo","Sol","Naty","Kati"],
    "Eliseo":["Luci","Sofi","Rodri","Lucho","Benjiwis","Eliseo","Sol","Naty","Kati"],
    "Sol":["Tenshi", "Luci", "Alejo","Sofi","Rodri","Lucho","Benjiwis","Eliseo","Sol"],
    "Naty":["Maxi", "Tenshi", "Luci", "Alejo","Sofi","Rodri","Lucho","Lauy","Benjiwis","Eliseo","Naty"],
    "Kati":["Maxi", "Tenshi", "Luci", "Alejo","Sofi","Rodri","Lucho","Lauty","Benjiwis","Eliseo","Kati"],
}

resultado = {}

def sortear_amigo_invisible():
    global resultado
    for _ in range(10000):
        asignados = random.sample(participantes, len(participantes))
        valido = True
        temp = {}
        for quien, a_quien in zip(participantes, asignados):
            if a_quien in restricciones.get(quien, []):
                valido = False
                break
            temp[quien] = a_quien
        if valido:
            resultado = temp
            return True
    return False

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sortear', methods=["POST"])
def sortear():
    ok = sortear_amigo_invisible()
    if ok:
        return redirect(url_for('ver'))
    return "No se pudo hacer el sorteo. Revisá las restricciones."

@app.route('/ver')
def ver():
    return render_template("ver.html", participantes=participantes)

@app.route('/resultado', methods=["POST"])
def resultado_individual():
    nombre = request.form["nombre"]
    asignado = resultado.get(nombre, "No encontrado")
    return render_template("resultado.html", nombre=nombre, asignado=asignado)

@app.route('/admin')
def ver_todos():
    html = "<h1>Asignaciones internas (Admin)</h1><ul>"
    for quien, a_quien in resultado.items():
        html += f"<li>{quien} → {a_quien}</li>"
    html += "</ul>"
    return html


if __name__ == '__main__':
    app.run(debug=True)