# Sistema de Gestão de Tarefas - Arquitetura de Microsserviços

Este projeto implementa um sistema completo de gestão de tarefas utilizando arquitetura de microsserviços com Python/FastAPI no backend e React no frontend, totalmente dockerizado.

## 🏗️ Arquitetura do Sistema

### Backend (Microsserviços)
- **API Gateway** (Porta 8000): Ponto de entrada único, roteamento de requisições
- **Users Service** (Porta 8002): Gerenciamento de usuários e autenticação
- **Tasks Service** (Porta 8001): CRUD de tarefas e lógica de negócio
- **Notifications Service** (Porta 8003): Sistema de notificações

### Frontend
- **React App** (Porta 3000): Interface do usuário moderna e responsiva

## 📁 Estrutura de Pastas

```
/
├── docker-compose.yml          # Orquestração dos containers
├── README.md                   # Documentação do projeto
├── frontend/                   # Aplicação React
│   ├── src/
│   │   ├── components/         # Componentes React
│   │   │   ├── Header.tsx
│   │   │   ├── Login.tsx
│   │   │   ├── TaskDashboard.tsx
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskCard.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── NotificationPanel.tsx
│   │   ├── App.tsx            # Componente principal
│   │   ├── api.ts             # Configuração da API
│   │   ├── types.ts           # Definições TypeScript
│   │   └── main.tsx           # Entry point
│   ├── package.json
│   ├── Dockerfile
│   └── ...
├── backend/                    # Microsserviços Python
│   ├── shared/                 # Código compartilhado
│   │   ├── models.py          # Modelos Pydantic
│   │   ├── database.py        # Configuração do banco
│   │   └── auth.py            # Autenticação JWT
│   ├── api-gateway/           # Gateway de API
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── users-service/         # Serviço de usuários
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── tasks-service/         # Serviço de tarefas
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── notifications-service/ # Serviço de notificações
│       ├── main.py
│       ├── requirements.txt
│       └── Dockerfile
```

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Docker
- Docker Compose

### Passo a Passo

1. **Clone o repositório e navegue até a pasta do projeto**

2. **Execute o sistema completo com Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Aguarde todos os serviços iniciarem** (pode levar alguns minutos na primeira execução)

4. **Acesse a aplicação:**
   - Frontend: http://localhost:3000
   - API Gateway: http://localhost:8000

## 🔧 Desenvolvimento

### Backend (Python/FastAPI)

Cada microsserviço é independente e possui:
- **FastAPI**: Framework web moderno e rápido
- **SQLite3**: Banco de dados local para cada serviço
- **JWT**: Autenticação segura
- **Uvicorn**: Servidor ASGI de alta performance

#### Serviços:

1. **Users Service**: 
   - Registro e login de usuários
   - Autenticação JWT
   - Gestão de perfis

2. **Tasks Service**:
   - CRUD completo de tarefas
   - Atribuição de tarefas
   - Controle de status e prioridades

3. **Notifications Service**:
   - Criação de notificações
   - Marcação como lida
   - Listagem personalizada

4. **API Gateway**:
   - Roteamento inteligente
   - Proxy para os microsserviços
   - CORS configurado

### Frontend (React/TypeScript)

- **React 18**: Biblioteca moderna para UI
- **TypeScript**: Tipagem estática
- **Tailwind CSS**: Estilização utilitária
- **Axios**: Cliente HTTP
- **Lucide React**: Ícones modernos

#### Componentes Principais:

- **Login**: Autenticação de usuários
- **TaskDashboard**: Dashboard principal
- **TaskList**: Lista de tarefas por status
- **TaskCard**: Card individual de tarefa
- **TaskForm**: Formulário de criação/edição
- **NotificationPanel**: Painel de notificações

## 🎯 Funcionalidades

### ✅ Gestão de Usuários
- Registro de novos usuários
- Login seguro com JWT
- Perfil do usuário

### ✅ Gestão de Tarefas
- Criar, editar e excluir tarefas
- Atribuir tarefas para usuários
- Definir prioridades (Baixa, Média, Alta, Urgente)
- Controlar status (Pendente, Em Progresso, Concluída, Cancelada)
- Data de vencimento
- Descrições detalhadas

### ✅ Sistema de Notificações
- Notificações automáticas para atribuições
- Notificações de mudança de status
- Marcar como lida
- Painel de notificações

### ✅ Interface Moderna
- Design responsivo
- Drag and drop visual
- Filtros por status
- Indicadores visuais
- Tema claro e profissional

## 🛡️ Segurança

- **JWT Authentication**: Tokens seguros para autenticação
- **Password Hashing**: Senhas criptografadas com bcrypt
- **CORS Configurado**: Proteção contra requisições maliciosas
- **Input Validation**: Validação de dados com Pydantic

## 📊 Banco de Dados

Cada microsserviço possui seu próprio banco SQLite:
- `users-service/data/users.db`: Dados dos usuários
- `tasks-service/data/tasks.db`: Dados das tarefas
- `notifications-service/data/notifications.db`: Notificações

## 🐳 Docker

O projeto está completamente dockerizado:
- Cada serviço possui seu próprio Dockerfile
- docker-compose.yml orquestra todos os containers
- Rede isolada para comunicação entre serviços
- Volumes persistentes para dados

## 🔄 Comunicação Entre Serviços

- **API Gateway**: Centraliza todas as requisições
- **HTTP/REST**: Comunicação síncrona entre serviços
- **Service Discovery**: URLs configuradas via environment variables

## 📝 Próximos Passos

- [ ] WebSockets para notificações em tempo real
- [ ] Cache com Redis
- [ ] Métricas e monitoring
- [ ] Testes automatizados
- [ ] CI/CD pipeline
- [ ] Deploy em cloud

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.