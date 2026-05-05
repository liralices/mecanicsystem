# 🔧 MecanicSystem

Sistema web voltado para a gestão de uma oficina mecânica. 

## 🚀 Funcionalidades

- Cadastro de clientes
- Cadastro de peças
- Criação de ordens de serviço
- Cálculo métricas
- Controle de status da ordem

## 🛠️ Tecnologias utilizadas

- Python
- Django
- SQLite
- HTML/CSS

## 📊 Objetivo do projeto

Este projeto foi desenvolvido com foco em aprendizado prático de desenvolvimento web com Django, aplicando conceitos de organização de dados, regras de negócio e estruturação de sistemas.

## 🎯 Problemas atendidos

Oficinas mecânicas de pequeno e médio porte gerenciam seus processos operacionais com atendimento, ordens de serviço, estoque de peças e controle financeiro, de forma manual ou com planilhas descentralizadas, o que resulta em perda de informações, dificuldade de rastreamento de histórico dos veículos, controle de estoque ineficiente e falhas no registro financeiro.

## ⚙️ Como rodar o projeto

```bash
git clone https://github.com/liralices/mecanicsystem.git
cd mecanicsystem

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
