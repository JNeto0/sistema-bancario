# Sistema Bancário

Sistema bancário desenvolvido em Python para gerenciar operações bancárias básicas.

## 📋 Descrição

Este projeto é um sistema bancário que permite a realização de operações como criação de contas, depósitos, saques e transferências entre contas.

## 🚀 Funcionalidades

- Criação de contas correntes
- Depósito de valores
- Saque de valores
- Transferência entre contas
- Histórico de transações
- Consulta de saldo

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Versionamento:** Git & GitHub

## 👥 Integrantes

- João Batista da Fonseca Neto – JNeto0
- Iadson Vinicius da Silva – iadsonv1n1

## ▶️ Como executar o sistema

### Pré-requisitos

Antes de executar o sistema, é necessário ter o Python instalado na máquina.

- Versão recomendada: **Python 3.12** (ou superior)

Download oficial do Python:  
https://www.python.org/downloads/

> Durante a instalação no Windows, marque a opção **"Add Python to PATH"**.

---

### Clonando o repositório

```bash
git clone https://github.com/JNeto0/sistema-bancario.git
```

### Executar o sistema
- Acesse a pasta raiz do projeto

  ```bash
    cd sistema-bancario
  ```

- Execute o seguinte comando para iniciar a interface de console.

  ```bash
    python -m src.main
  ```

---

## API REST

A base da API REST usa apenas a biblioteca padrao do Python.

### Executar a API

```bash
python -m src.api
```

Por padrao, o servidor sobe em `http://127.0.0.1:8000`.

### Endpoints disponiveis

- `POST /banco/conta/`
- `GET /banco/conta/<id>`
- `GET /banco/conta/<id>/saldo`
- `PUT /banco/conta/<id>/credito`
- `PUT /banco/conta/<id>/debito`
- `PUT /banco/conta/transferencia`
- `PUT /banco/conta/rendimento`

### Exemplo de cadastro

```bash
curl -X POST http://127.0.0.1:8000/banco/conta/ ^
  -H "Content-Type: application/json" ^
  -d "{\"numero\":\"12345678\",\"tipo\":\"simples\",\"saldo_inicial\":100}"
```

### Exemplo de credito

```bash
curl -X PUT http://127.0.0.1:8000/banco/conta/12345678/credito ^
  -H "Content-Type: application/json" ^
  -d "{\"valor\":50}"
```
