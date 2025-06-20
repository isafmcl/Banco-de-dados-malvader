﻿# Sistema Bancário - Banco Malvader

## Descrição
API REST em Flask para um sistema bancário com interface web, oferecendo funcionalidades para clientes e funcionários.

## Requisitos do Sistema
- Python 3.x
- Flask
- Flask-CORS

## Instalação
1. Clone o repositório
2. Crie um ambiente virtual:
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. Instale as dependências:
```powershell
pip install flask flask-cors
```

## Estrutura do Projeto
```bash
Banco/
├── .git/
├── backend/
│   ├── src/
│   │   ├── services/
│   │   ├── database/
│   │   └── utils/
│   └── app.py
├── frontend/
│   ├── assets/
│   │   ├── images/
│   ├── css/
|   |   ├── style.css
│   ├── js/
│   │   ├── views/
│   │   ├── controllers/
│   │   ├── models/
│   └── templates/
|       ├── arquivos html
├── venv/
└── README.md
```


## Funcionalidades

### Clientes
- Login/Autenticação
- Consulta de saldo
- Depósitos
- Saques
- Transferências
- Consulta de extrato
- Investimentos

### Funcionários
- Login com OTP (One-Time Password)
- Criação de contas de clientes
- Consulta de clientes
- Visualização de estatísticas
- Consulta de inadimplentes
- Encerramento de contas

## Endpoints da API

### Autenticação
- `POST /login` - Login de clientes e funcionários

### Operações Financeiras
- `GET /saldo/<cpf>` - Consulta saldo
- `POST /deposito` - Realiza depósito
- `POST /saque` - Realiza saque
- `POST /transferencia` - Realiza transferência
- `GET /consultar-transacoes/<numero_conta>` - Consulta transações

### Gestão de Contas
- `POST /criar-cliente` - Cria nova conta de cliente
- `POST /criar-funcionario` - Cria nova conta de funcionário
- `GET /consultar-cliente/<cpf>` - Consulta informações do cliente
- `POST /encerrar-conta` - Encerra conta de cliente

### Funcionalidades Administrativas
- `GET /estatisticas` - Obtém estatísticas do banco
- `GET /clientes-inadimplentes` - Lista clientes inadimplentes
- `GET /consultar_otp/<cpf>` - Consulta OTP do funcionário

## Segurança
- Autenticação de dois fatores para funcionários (OTP)
- Validação de dados de entrada
- Tratamento de erros padronizado

## Executando a Aplicação
```powershell
python app.py
```
O servidor será iniciado em `http://localhost:5000`

## Frontend
O frontend está disponível em `templates/` e pode ser acessado através de um servidor web local.

## Observações
- O sistema usa CORS configurado para desenvolvimento local
- Modo debug ativado para ambiente de desenvolvimento
