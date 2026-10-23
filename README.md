# Sistema de Controle de Patrimônio

Aplicação web em Flask + SQLite para cadastro e controle de bens patrimoniais, com categorias, locais e histórico de movimentações.

## Funcionalidades

- Painel com indicadores e últimas movimentações
- Cadastro, edição e exclusão de bens
- Categorias e locais de alocação
- Registro de movimentações entre locais
- Busca e filtros por código, nome, categoria, local e status
- Exportação dos bens em CSV

## Como executar

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Acesse http://127.0.0.1:5000. O banco `patrimonio.db` é criado automaticamente na primeira execução.
