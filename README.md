# pyvidesk

Biblioteca Python para uso da API do Movidesk.

## Informações Gerais

Atualmente, esta biblioteca suporta apenas consultas as entidades [Tickets](https://atendimento.movidesk.com/kb/pt-br/article/256/movidesk-ticket-api), [Persons](https://atendimento.movidesk.com/kb/pt-br/article/189/movidesk-person-api) e [Services](https://atendimento.movidesk.com/kb/pt-br/article/7440/api-servicos) por meio da API do Movidesk.

## Uso

```python
from pyvidesk import Pyvidesk

persons = Pyvidesk(token="Meu_token_secreto").persons
person_id_1 = persons.get_by_id(1)
# person_id_1 contém o JSON retornado pelo Movidesk.
```

Você pode usara lógica acima para consultar qualquer propriedade da entidade e ainda setar as opções da query:

```python
from pyvidesk import Pyvidesk

persons = Pyvidesk(token="Meu_token_secreto").persons
my_query = persons.get_by_isActive(True, select=("id", "businessName"), top=10)
# my_query contém uma lista, apenas com as informações "id" e "businessName", 
# das 10 primeiras pessoas ativas.
```

Para consultas mais complexas recomenda-se o uso do método `query` e das propriedades específicas da entidade, obtidas por meio de `get_properties`:

```python
from datetime import date, timedelta

from pyvidesk import Pyvidesk

tickets = Pyvidesk(token="Meu_token_secreto").tickets
tickets_properties = tickets.get_properties()
my_query = (
    tickets.query()
    .filter(tickets_properties["owner"].businessName == "Murilo Scarpa Sitonio")
    .filter(tickets_properties["createdDate"] >= date.today() - timedelta(days=1))
    .expand(tickets_properties["clients"])
    .select(tickets_properties["id"])
)
print(my_query.url())
# https://api.movidesk.com/public/v1/tickets?token=Meu_token_secreto&$select=id&$filter=owner/businessName 
# eq 'Murilo Scarpa Sitonio' and createdDate ge 2020-10-01&$expand=clients
```

Para acessar os resultados da consulta deve-se seguir uma das três abordagens:

- Iterar sobre o objeto:
```python
for data in my_query:
    print(data)
```

- Agrupar todos os resultados numa lista:
```python
data = my_query.all()
```

- Obter apenas o primeiro resultado:
```python
data = my_query.first()
```

### Exemplos de consulta mais complexa

```python
from pyvidesk import Pyvidesk
from pyvidesk.utils import AnyAny

# AnyAny implementa dois operadores lambdas concatenados.

tickets = Pyvidesk(token="Meu_token_secreto").tickets
tickets_properties = tickets.get_properties()

my_query = (
    tickets.query()
    .filter(
        AnyAny(
            tickets_properties["customFieldValues"].items.customFieldItem
            == "Equipamento XYZ"
        )
    )
    .expand(
        tickets_properties["customFieldValues"],
        inner={
            "expand": tickets_properties["customFieldValues"].items,
            "select": tickets_properties["customFieldValues"].items.customFieldItem,
        },
        select=tickets_properties["customFieldValues"].items,
    )
    .select(tickets_properties["id"])
    .order_by(tickets_properties["id"].desc())
    .top(5)
    .skip(200)
)

print(my_query.as_url())
# https://api.movidesk.com/public/v1/tickets?token=Meu_token_secreto&$top=5&$skip=200&$select=id
# &$filter=customFieldValues/any(x: x/items/any(y: y/customFieldItem eq 'Equipamento XYZ'))
# &$expand=customFieldValues($expand=items($select=customFieldItem);$select=items)&$orderby=id desc

for data in my_query:
    print(data)

# {'id': 1003, 'customFieldValues': [{'items': [{'customFieldItem': 'Falha em equipamento'}]}, 
# {'items': [{'customFieldItem': 'Equipamento XYZ'}]}]}
# {'id': 1002, 'customFieldValues': [{'items': [{'customFieldItem': 'Falha em equipamento'}]}, 
# {'items': [{'customFieldItem': 'Equipamento XYZ'}]}]}
# {'id': 1001, 'customFieldValues': [{'items': [{'customFieldItem': 'Falha em equipamento'}]}, 
# {'items': [{'customFieldItem': 'Equipamento XYZ'}]}]}
# {'id': 987, 'customFieldValues': [{'items': [{'customFieldItem': 'Falha em equipamento'}]}, 
# {'items': [{'customFieldItem': 'Equipamento XYZ'}]}]}
# {'id': 984, 'customFieldValues': [{'items': [{'customFieldItem': 'Falha em equipamento'}]}, 
# {'items': [{'customFieldItem': 'Equipamento XYZ'}]}]}
```
