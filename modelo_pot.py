#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 16:23:32 2022

@author: cristhiamdaniel
adiciones Daniel Nino
"""
from flask import Flask, render_template, request
import numpy as np
import pandas as pd

app = Flask(__name__)


@app.route('/')
def principal():
    return render_template('index.html')


@app.route("/result", methods=['POST', "GET"])
def result():
    output = request.form.to_dict()
    temperature = output["temperatura"]
    irradiancia = output["irradiancia"]

    #Cambiar la direccion a donde quede despues de descargar
    path = 'Data_pot.csv'

    if temperature == '' or irradiancia == '':
        return render_template("index.html")

    data = pd.read_csv(path)

    G = int(irradiancia)
    T = int(temperature)

    entrada = np.array([[G, T]], dtype='float')

    w1 = np.array([[0.67033446, -0.2966106, -0.01998537, -0.38660145, 1.0487925],
                   [-1.075884, -0.20943986, -3.1135402, 0.02758573, -1.84972]],
                  dtype='float')
    b1 = np.array([18.468002, 1.2586317, 27.301346, -10.97803, 20.440323],
                  dtype='float')
    w2 = np.array([[-0.17117049, -1.2795218],
                   [-0.31654954, -0.09632481],
                   [-0.6963905, -0.80916595],
                   [0.03652098, 0.593637],
                   [-0.32155666, -1.7501591]], dtype='float')
    b2 = np.array([-2.9189575, -16.129646], dtype='float')
    w3 = np.array([[-0.08504742],
                   [-1.3637999]], dtype='float')
    b3 = np.array([15.210299], dtype='float')

    x1 = entrada.dot(w1) + b1
    x2 = x1.dot(w2) + b2
    x3 = x2.dot(w3) + b3

    resultado = data.loc[(data['G'] == G) & (data['T'] == T)]

    """
    print()
    print("Potencia predecida: ", round(float(x3), 2))
    print("Potencia real: ", round(float(resultado['Pmax']), 2))
    """
    ans = round(float(x3), 2)

    return render_template("index.html", ans=ans)


if __name__ == '__main__':
    app.run(debug=True)
