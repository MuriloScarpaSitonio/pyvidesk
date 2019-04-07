# pyvidesk

Biblioteca Python para uso da API do Movidesk.

## Estado de implementação das APIs

Clique no nome para ler a documentação.

- ❌ [Serviços](https://atendimento.movidesk.com/kb/pt-br/article/7440/api-servicos)
- ❌ [Pessoas](https://atendimento.movidesk.com/kb/pt-br/article/189/movidesk-person-api)
- ❌ [Tickets](https://atendimento.movidesk.com/kb/pt-br/article/256/movidesk-ticket-api)

## Uso

**Esta biblioteca está em estágio bastante inicial.**

A intenção é torná-la usável desta maneira:

```python

import Pyvidesk

pyvidesk = Pyvidesk('api_token_super_secreto')

exclusao_servico_9 = pyvidesk.services.delete(9)
# MoviResponse(data=None, is_ok=False, error=...)

servico_172 = pyvidesk.services.get_by_id(172).data
# Service(id=172, name="Servicinho" ...)

agentes = pyvidesk.persons.get({ filter = "profileType eq 1" }).data
# [ Person(id=2, name="Josefino Alves" ...), Person(id=42, name="Paolo Damião" ...) ]

```

## Desenvolvimento

Quaisquer contribuições ou comentários são muito bem-vindos.

### Lista não-extensiva de coisas a fazer:
- Modelagem das APIs (Service, Person, Ticket, etc.) e seus métodos
- Implementar uso do [protocolo OData](https://www.odata.org/)
- Verificar se é possível usar uma base própria para testes, ou fazer mocking neles
- Adicionar package ao [pip](pypi.org) e acompanhar uso pelos clientes/funcionários
- Usar [virtual environments](https://docs.python.org/3/tutorial/venv.html) de maneira adequada
- Tipagem?

### Executando testes

`python -m unittest discover test`