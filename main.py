from flask import Flask, request, jsonify
from config.db_config import DataBaseConexao

app = Flask(__name__)

# GET /produtos
@app.route('/produtos', methods=['GET'])
def produto():
    conexao = DataBaseConexao()

    try:
        resultado = conexao.cursor.execute('SELECT * FROM produtos;')
        dados = resultado.fetchall()
        resultado.close()

        dados_formatados = []
        
        for item in dados:
            registro = {
                "id": item[0],
                "nome": item[1],
                "preco": float(item[2]),
                "quantidade": item[3]
            }
            dados_formatados.append(registro)

        return jsonify(dados_formatados), 200
    except Exception as erro:
        return jsonify({"erro": erro}), 500

# GET /produtos/produto/id
@app.route('/produtos/produto/<int:id>', methods=['GET'])
def produto_id(id):
    conexao = DataBaseConexao()
    try:
        resultado = conexao.cursor.execute("SELECT * FROM produtos WHERE id = %s;", (id,))
        dados = resultado.fetchall()
        resultado.close()
        dados_formatados = []
        
        for item in dados:
            registro = {
                "id": item[0],
                "nome": item[1],
                "preco": float(item[2]),
                "quantidade": item[3]
            }
            dados_formatados.append(registro)
        
        return jsonify(dados_formatados), 200
    except Exception as erro:
        return jsonify({"erro": "Pessoa não encontrada", "error": erro}), 404

# POST /produtos/novo-produto
@app.route('/novo-produto', methods=['POST'])
def novo_produto():
    produto = request.json
    conexao = DataBaseConexao()
		
    try:
        conexao.cursor.execute('INSERT INTO produtos (nome, preco, estoque) VALUES (%s, %s, %s)', (produto['nome'], float(produto['preco']), int(produto['estoque'])))

        return jsonify({"mensagem": "Produto adicionado com sucesso"}), 201
    except Exception as e:
        return jsonify({"mensagem": "Erro ao adicionar produto", "erro": str(e)}), 400

# PUT /produtos/atualizar/id
@app.route('/atualizar/<int:id>', methods=['PUT'])
def atualizar(id):
    produto = request.json

    conexao = DataBaseConexao()
    cursor = conexao.cursor
    cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
    verificarId = cursor.fetchone()

    if verificarId is None:
        return jsonify({"erro": "Produto não encontrada"}), 404
    
    try:
        if 'nome' in produto:
            conexao.cursor.execute("UPDATE produtos SET nome = %s WHERE id = %s", (produto['nome'], id))

        if 'preco' in produto:
            conexao.cursor.execute("UPDATE produtos SET preco = %s WHERE id = %s", (produto['preco'], id))

        if 'estoque' in produto:
            conexao.cursor.execute("UPDATE produtos SET estoque = %s WHERE id = %s", (produto['estoque'], id))

        return jsonify({"mensagem": "Produto atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"mensagem": "Erro ao tentar atualizar", "erro": str(e)}), 400

# DELETE /produtos/deletar/id
@app.route('/produtos/deletar/<int:id>', methods=['DELETE'])
def deletar(id):
    conexao = DataBaseConexao()
    cursor = conexao.cursor
    cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
    verificarId = cursor.fetchone()

    if verificarId is None:
        return jsonify({"erro": "Produto não encontrada"}), 404
    
    try: 
        cursor.execute('DELETE FROM produtos WHERE id = %s', (id,))
        cursor.close()
        return jsonify({"mensagem": "Produto deletada com sucesso"})
    
    except Exception as erro:
        return jsonify({"mensagem": "Erro ao tentar deletar %s", "erro": erro}), 400


if __name__ == '__main__':
    app.run(debug=True)