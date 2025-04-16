# Delivery Guard

Sistema inteligente de detecção de fraudes em transações online com análise automatizada por IA e painel de verificação manual.

## 📐 Arquitetura

- **API**: Recebe transações e insere na fila
- **Fila (ex: RabbitMQ)**: Armazena mensagens para processamento assíncrono
- **Processador com IA**: Analisa comportamento e classifica transações
- **Banco de Dados**: Armazena os dados e resultados
- **BFF**: Intermediário entre banco e frontend
- **Frontend Admin**: Operador visualiza transações e toma decisões

Diagrama da arquitetura disponível em [`docs/`](./docs).

## 🛠️ Tecnologias

- Node.js / Express (API)
- Python (IA)
- PostgreSQL
- RabbitMQ
- React (Frontend)
- Docker / Docker Compose

## 🚀 Rodando o projeto

```bash
docker-compose up --build
