# Fortuno - Sistema de Controle Financeiro Pessoal

## 📱 Sobre o Projeto

O **Fortuno** é um sistema completo de controle financeiro pessoal desenvolvido como Trabalho de Conclusão de Curso (TCC). A aplicação permite aos usuários gerenciar suas finanças de forma intuitiva, controlando receitas, despesas, cartões de crédito e contas bancárias.

## 🚀 Tecnologias Utilizadas

### Frontend
- **Vue.js 3** - Framework JavaScript 
- **Quasar Framework** - UI Components e ferramentas
- **TypeScript** - Tipagem estática
- **Pinia** - Gerenciamento de estado
- **Axios** - Cliente HTTP
- **ApexCharts** - Gráficos e visualizações

### Backend
- **Django** - Framework web Python
- **Django REST Framework** - API REST
- **PostgreSQL** - Banco de dados
- **JWT** - Autenticação
- **Gunicorn** - Servidor WSGI

### Deploy
- **Frontend**: Vercel
- **Backend**: Railway
- **Banco de Dados**: PostgreSQL (Railway)

## 🎯 Funcionalidades

### 👤 Autenticação
- [x] Cadastro de usuários
- [x] Login/Logout
- [x] Validação de senha segura
- [x] Tokens JWT

### 💳 Gestão de Contas
- [x] Cadastro de contas bancárias
- [x] Cadastro de cartões de crédito
- [x] Configuração de limites e vencimentos
- [x] Visualização de saldos

### 💰 Transações
- [x] Registro de receitas e despesas
- [x] Categorização de transações
- [x] Filtros por período e categoria
- [x] Transações parceladas (cartão de crédito)

### 📊 Relatórios e Dashboards
- [x] Gráficos de gastos por categoria
- [x] Histórico de transações
- [x] Agrupamento por data
- [x] Indicadores financeiros

### 🏷️ Categorias
- [x] Categorias pré-definidas
- [x] Criação de categorias personalizadas
- [x] Ícones e cores customizáveis
- [x] Gestão completa de categorias

## 🛠️ Instalação e Execução

### Pré-requisitos
- Node.js 18+
- Python 3.11+
- PostgreSQL (opcional para desenvolvimento)

### Frontend (Quasar/Vue.js)

```bash
# Navegar para o diretório do frontend
cd fortuno-app

# Instalar dependências
npm install

# Executar em modo de desenvolvimento
npm run dev

# Build para produção
npm run build
```

### Backend (Django)

```bash
# Navegar para o diretório do backend
cd fortuno-back

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser

# Executar servidor de desenvolvimento
python manage.py runserver
```

### Docker (Desenvolvimento)

```bash
# Backend com Docker
cd fortuno-back
docker-compose up --build
```

## 🌐 URLs de Produção

- **Frontend**: https://fortuno-app.vercel.app
- **Backend API**: https://fortuno-app-production.up.railway.app
- **Admin Django**: https://fortuno-app-production.up.railway.app/admin/

## 👨‍💻 Dados de Teste

Para testar a aplicação, utilize as credenciais:

- **Email**: `admin@gmail.com`
- **Senha**: `admin`

## 📁 Estrutura do Projeto

```
fortuno-app/
├── fortuno-app/          # Frontend (Quasar/Vue.js)
│   ├── src/
│   │   ├── components/   # Componentes Vue
│   │   ├── pages/        # Páginas da aplicação
│   │   ├── stores/       # Gerenciamento de estado (Pinia)
│   │   ├── types/        # Tipos TypeScript
│   │   └── utils/        # Utilitários e helpers
│   ├── public/           # Arquivos estáticos
│   └── package.json      # Dependências do frontend
├── fortuno-back/         # Backend (Django)
│   ├── app/              # App principal Django
│   │   ├── models/       # Modelos de dados
│   │   ├── migrations/   # Migrações do banco
│   │   └── services/     # Lógica de negócio
│   ├── api/              # API REST
│   │   ├── views/        # Views da API
│   │   └── serializers/  # Serializers DRF
│   ├── fortuno/          # Configurações Django
│   └── requirements.txt  # Dependências do backend
└── README.md             # Este arquivo
```

## 🔧 Variáveis de Ambiente

### Frontend (.env)
```env
API_URL=https://fortuno-app-production.up.railway.app
```

### Backend (.env)
```env
DEBUG=False
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=postgresql://user:pass@host:port/db
ALLOWED_HOSTS=.railway.app,.up.railway.app
```

## 👨‍🎓 Autor

**Kaique Silva**
- Projeto desenvolvido como Trabalho de Conclusão de Curso
- Sistema de Controle Financeiro Pessoal