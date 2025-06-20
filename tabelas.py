import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)


def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

n_clientes = 1000
start_date = datetime.now() - timedelta(days=3*365)
end_date = datetime.now()

clientes = pd.DataFrame({
    'id_cliente': range(1, n_clientes + 1),
    'nome_cliente': [f'Cliente_{i}' for i in range(1, n_clientes + 1)],
    'data_cadastro': [random_date(start_date, end_date).date() for _ in range(n_clientes)]
})

n_produtos = 500
categorias = ['Eletrônicos', 'Livros', 'Casa', 'Moda', 'Esportes']
produtos = pd.DataFrame({
    'id_produto': range(1, n_produtos + 1),
    'nome_produto': [f'Produto_{i}' for i in range(1, n_produtos + 1)],
    'categoria': [random.choice(categorias) for _ in range(n_produtos)],
    'preco_custo': np.round(np.random.uniform(10, 500, n_produtos), 2)
})

n_pedidos = 5000
pedidos_data_cliente = np.random.choice(clientes['id_cliente'], n_pedidos)

pedidos = pd.DataFrame({
    'id_pedido': range(1, n_pedidos + 1),
    'id_cliente': pedidos_data_cliente,
    'data_pedido': [
        random_date(
            datetime.combine(clientes.loc[clientes['id_cliente'] == cid, 'data_cadastro'].values[0], datetime.min.time()),
            end_date
        ).date()
        for cid in pedidos_data_cliente
    ]
})

pedidos['valor_total'] = 0.0

items = []
item_id = 1
for pedido_id in pedidos['id_pedido']:
    n_itens = random.randint(1, 5)
    produtos_pedido = np.random.choice(produtos['id_produto'], n_itens, replace=False)
    for prod_id in produtos_pedido:
        quantidade = random.randint(1, 10)
        preco_unitario = produtos.loc[produtos['id_produto'] == prod_id, 'preco_custo'].values[0] * random.uniform(1.2, 2.0)
        preco_unitario = round(preco_unitario, 2)
        items.append({
            'id_item': item_id,
            'id_pedido': pedido_id,
            'id_produto': prod_id,
            'quantidade': quantidade,
            'preco_unitario': preco_unitario
        })
        item_id += 1

itens_pedido = pd.DataFrame(items)

valor_totais = itens_pedido.groupby('id_pedido').apply(lambda x: (x['quantidade'] * x['preco_unitario']).sum())
pedidos.set_index('id_pedido', inplace=True)
pedidos.loc[valor_totais.index, 'valor_total'] = valor_totais
pedidos.reset_index(inplace=True)

clientes.to_csv('clientes.csv', index=False)
produtos.to_csv('produtos.csv', index=False)
pedidos.to_csv('pedidos.csv', index=False)
itens_pedido.to_csv('itens_pedido.csv', index=False)

print("Arquivos CSV criados com sucesso.")
