# Delivery Guard

![aa](docs/imgs/c4diagram.svg)

Trata-se de um sistema inteligente desenvolvido para identificar possíveis fraudes em transações de compras online. Utilizando técnicas de Inteligência Artificial (IA), o sistema analisa padrões de comportamento e sinaliza automaticamente atividades suspeitas. As transações identificadas como potencialmente fraudulentas são listadas em um painel administrativo, acessível por meio de um frontend, onde podem ser verificadas manualmente por um operador humano para validação e tomada de decisão.

Diagrama da arquitetura disponível em [`docs/`](./docs).

## 🛠️ Tecnologias

- Python
- FastAPI
- PostgreSQL
- RabbitMQ
- Typescript
- React
- Docker

### Diagrama de classe

```mermaid
classDiagram
    class Customer {
        +String customer_id (PK)
        +String email
        +String phone
        +String first_name
        +String last_name
        +String device_id
        +String ip_address
        +Boolean is_verified
        +Integer risk_score
        +Timestamp last_activity
        +List~Transaction~ transactions()
    }

    class Transaction {
        +Integer id (PK)
        +String transaction_id
        +Numeric amount
        +String status
        +String payment_method
        +DateTime created_at
        +Customer customer
        +User operator
        +List~TransactionItem~ items()
    }

    class TransactionItem {
        +Integer id (PK)
        +String product_name
        +Numeric unit_price
        +Integer quantity
        +Transaction transaction
    }

    class User {
        +Integer id (PK)
        +String username
        +String role
        +List~Transaction~ reviewed_transactions()
    }

    Customer "1" --> "*" Transaction
    User "1" --> "*" Transaction
    Transaction "1" --> "*" TransactionItem
```
