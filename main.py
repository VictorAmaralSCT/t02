from flask import Flask, jsonify, request

app = Flask(__name__)

produtos = [
    {
        "id": 1,
        "nome": "Notebook",
        "categoria": "Informática",
        "preco": 3500.00,
        "estoque": 10
    },
    {
        "id": 2,
        "nome": "Mouse",
        "categoria": "Periféricos",
        "preco": 80.00,
        "estoque": 50
    }
]


@app.route("/")
def home():
    return jsonify({
        "mensagem": "API de Produtos funcionando!"
    })


@app.route("/produtos", methods=["GET"])
def listar_produtos():
    return jsonify(produtos)


@app.route("/produtos/<int:id>", methods=["GET"])
def buscar_produto(id):
    for produto in produtos:
        if produto["id"] == id:
            return jsonify(produto)

    return jsonify({"erro": "Produto não encontrado"}), 404

@app.route("/produtos", methods=["POST"])
def cadastrar_produto():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    if "nome" not in dados or "preco" not in dados:
        return jsonify({"erro": "Campos obrigatórios: nome e preco"}), 400

    novo_produto = {
        "id": len(produtos) + 1,
        "nome": dados["nome"],
        "categoria": dados.get("categoria", "Sem categoria"),
        "preco": dados["preco"],
        "estoque": dados.get("estoque", 0)
    }

    produtos.append(novo_produto)

    return jsonify({
        "mensagem": "Produto cadastrado com sucesso",
        "produto": novo_produto
    }), 201

@app.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    dados = request.get_json()

    for produto in produtos:
        if produto["id"] == id:
            produto["nome"] = dados.get("nome", produto["nome"])
            produto["categoria"] = dados.get("categoria", produto["categoria"])
            produto["preco"] = dados.get("preco", produto["preco"])
            produto["estoque"] = dados.get("estoque", produto["estoque"])

            return jsonify({
                "mensagem": "Produto atualizado com sucesso",
                "produto": produto
            })

    return jsonify({"erro": "Produto não encontrado"}), 404

@app.route("/produtos/<int:id>", methods=["DELETE"])
def remover_produto(id):
    for produto in produtos:
        if produto["id"] == id:
            produtos.remove(produto)
            return jsonify({
                "mensagem": "Produto removido com sucesso"
            })

    return jsonify({"erro": "Produto não encontrado"}), 404


if __name__ == "__main__":
    #app.run(debug=True)if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)