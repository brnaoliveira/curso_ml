# Construir a API --> Flask
from flask import Flask, Request
import joblib
import sqlite3
# Biblioteca para data
from datetime import datetime


# Instanciar o aplicativo
aplicativo = Flask(__name__)

# Carregar Modelo
modelo = joblib.load('Modelo_Floresta_Aleatoria_v1.pkl')



# Função para receber API
@aplicativo.route('/API_Preditivo/<area>;<rooms>;<bathroom>;<parking_spaces>;<floor>;<animal>;<furniture>;<hoa>;<property_tax>', methods=['GET'])
def funcao_01( area, rooms, bathroom, parking_spaces, floor, animal, furniture, hoa, property_tax):

    # Data e Hora de inicio
    data_inicio = datetime.now()

    # Recebendo os inputs da API
    lista = [
        float(area), float(rooms), float(bathroom), float(parking_spaces), 
        float(floor), float(animal), float(furniture), float(hoa), float(property_tax)
    ]


    # Previsão
    try:
        previsao = modelo.predict([lista])

        # Inserir o valor da Previsão
        lista.append(str(previsao))
        
        # Transformando lista em string
        input = ''
        for valor in lista:
            input = input + ';' + str(valor)


        # Data e Hora do fim
        data_fim= datetime.now()
        processamento = data_fim - data_inicio
        

        # Criar a conexão com o banco de dados
        conexao_bd = sqlite3.connect('bd_api.db')
        cursor = conexao_bd.cursor()
        
        # Query
        query_inserir_dados = f'''
            INSERT INTO log_api(inputs, inicio, fim, processamento)
            VALUES('{input}', '{data_inicio}', '{data_fim}', '{processamento}')
        '''
        # Executar a query
        cursor.execute(query_inserir_dados)
        conexao_bd.commit()

        # Fechar a conexão
        cursor.close()

        # Retornar o modelo
        return{'valor_aluguel': str(previsao)}
    
    except:
        return{'aviso': 'Deu algum erro!'}


if __name__ == '__main__':
    aplicativo.run(debug=True)


