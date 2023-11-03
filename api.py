from flask import Flask, request, jsonify
from CrawlerTJAL import CrawlerTJAL
from CrawlerTJCE import CrawlerTJCE
import json
from selenium.common.exceptions import NoSuchElementException

app = Flask(__name__)

@app.route('/coletar_processo', methods=['GET'])
def coletar_processo():
    try:
        numero_processo = request.json['numero_processo']
        print(numero_processo)
        if not numero_processo:
            return jsonify({'error': 'Número do processo não especificado'})
        
        if '8.02' in numero_processo:
            try:
                driver = CrawlerTJAL.acessar_site(numero_processo) 
                dados = CrawlerTJAL.coletar_dados_do_processo(driver)
                driver = CrawlerTJAL.acessar_site_segundo_grau(numero_processo)
                dados2grau = CrawlerTJAL.coletar_dados_segundo_grau(driver)
                dados_json = {
                    'Dados do Processo 1º Grau': dados,
                    'Dados do Processo 2º Grau': dados2grau
                }
                return jsonify(dados_json)
            except NoSuchElementException:
                return jsonify({'error': 'Processo incorreto, tente novamente'})
            
        elif '8.06' in numero_processo:
            try:
                driver = CrawlerTJCE.acessar_site(numero_processo) 
                dados = CrawlerTJCE.coletar_dados_do_processo(driver)
                driver = CrawlerTJCE.acessar_site_segundo_grau(numero_processo)
                dados2grau = CrawlerTJCE.coletar_dados_segundo_grau(driver)
                dados_json = {
                    'Dados do Processo 1º Grau': dados,
                    'Dados do Processo 2º Grau': dados2grau
                }
                return jsonify(dados_json)
            except NoSuchElementException:
                return jsonify({'error': 'Número do processo incorreto, tente novamente'})
        else:
            return jsonify({'error': 'Número de processo não corresponde a nenhuma rota'})
        
    except Exception as e:
        return jsonify({'error': str(e)})

app.run()
