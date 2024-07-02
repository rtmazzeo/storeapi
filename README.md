## API de Gerenciamento de Produtos com Tratamento de Erros e Filtros Avançados

Esta API RESTful, desenvolvida com FastAPI e MongoDB, oferece uma solução robusta para gerenciamento de produtos, com foco em tratamento de erros, filtros avançados e atualização de dados com timestamps.

## Funcionalidades Principais:

* **Criação e Atualização de Produtos:** Cadastre e modifique produtos, com atualização automática do campo `updated_at`.
* **Tratamento de Erros Personalizado:** Exceções customizadas para erros de inserção e dados não encontrados, com mensagens claras para o usuário.
* **Filtros de Preço Avançados:** Filtre produtos por faixas de preço, utilizando operadores lógicos (AND, OR).
* **Estrutura Modular:** Organização em módulos para facilitar a manutenção e o desenvolvimento futuro.
* **Testes Unitários:** Testes para garantir a qualidade e o funcionamento correto da API.

## Estrutura do Projeto:

* `controllers`: Controladores da API.
* `core`: Configurações, exceções e conexão com o MongoDB.
* `models`: Modelos de dados dos produtos (Pydantic).
* `schemas`: Esquemas de serialização (entrada/saída).
* `usecases`: Lógica de negócio (criação, atualização, busca).
* `tests`: Testes unitários.

## Desafio Final
- Create
    - Mapear uma exceção, caso dê algum erro de inserção e capturar na controller
- Update
    - Modifique o método de patch para retornar uma exceção de Not Found, quando o dado não for encontrado
    - a exceção deve ser tratada na controller, pra ser retornada uma mensagem amigável pro usuário
    - ao alterar um dado, a data de updated_at deve corresponder ao time atual, permitir modificar updated_at também
- Filtros
    - cadastre produtos com preços diferentes
    - aplique um filtro de preço, assim: (price > 5000 and price < 8000)


