# Projeto de Qualidade e Testes de Software - Tarefa 2

Este repositório foi criado para a entrega da Tarefa 2 da nossa disciplina. O objetivo foi pegar uma API em Flask e adicionar novas funcionalidades usando TDD, além de garantir que tudo estivesse bem testado e dentro dos padrões de qualidade.

---

## Como o projeto está organizado

Separei o código para ficar mais fácil de testar:

```text
.github/workflows/      # Onde fica a automação dos testes no GitHub
app/                    # Pasta com o código principal
  routes/               # Onde definimos os caminhos (endpoints) da API
  services/             # Onde fica a lógica das funções e validações
  templates/            # A parte visual simples do sistema
tests/                  # Todos os testes que eu criei
  unit/                 # Testes de funções isoladas
  integration/          # Testes ligando a API com os serviços
  functional/           # Testes de fluxos reais do usuário
  e2e/                  # Testes automatizados simulando o navegador
run.py                  # Arquivo que liga o servidor
```

---

## O que eu fiz nesta tarefa

Nesta entrega eu foquei em duas coisas principais:

1.  **Validação de Idade**: Agora o sistema pede a idade e só aceita se for entre 1 e 120 anos. Se colocar algo diferente, ele avisa que deu erro.
2.  **Busca por Nome**: Adicionei um filtro na listagem. Dá para buscar usuários específicos pelo nome direto na URL.

---

## Como usei o TDD

Para a validação de idade, usei o processo de TDD conforme pedido:

- Primeiro criei os testes que falhavam (mostrando que a idade ainda não era validada).
- Depois escrevi o código necessário para fazer esses testes passarem.
- Por fim, dei uma limpada no código para deixar as funções mais organizadas.

---

## Os Testes que eu criei

Para bater a meta da tarefa, adicionei:
- **10 testes unitários** para cobrir as regras da idade e da busca.
- **5 testes de integração** para garantir que os endpoints da API respondem certo.
- **3 testes funcionais** testando o caminho completo de criar e atualizar usuários.
- **2 testes de ponta a ponta (E2E)** onde o Selenium abre o navegador e testa a tela de verdade.

---

## Qualidade do Código

Para deixar o código padronizado e limpo, usei o **Black** para formatação e o **Flake8** para conferir se não tinha nada sobrando ou errado no estilo. Também deixei configurado o GitHub Actions para rodar esses testes sozinho sempre que eu subir uma alteração.

---

## Como rodar na sua máquina

### 1. Preparar o ambiente
Eu recomendo usar um ambiente virtual:

```bash
python -m venv venv
# No Windows use: venv\Scripts\activate
# No Linux/Mac use: source venv/bin/activate

pip install -r requirements.txt
```

### 2. Ligar o sistema
```bash
python run.py
```
Aí é só abrir no navegador: `http://localhost:5000`

### 3. Rodar os testes
```bash
# Para rodar a maioria dos testes:
python -m pytest tests/unit tests/integration tests/functional

# Obs: Para rodar os testes de navegador (E2E), o sistema precisa estar ligado em outro terminal.
```
