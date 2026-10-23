# Sistema de Controle de Empréstimos e Devoluções — IL/UFMT

Sistema web para a Secretaria do Instituto de Linguagens da UFMT registrar empréstimos e
devoluções de chaves, controles remotos, projetores e outros materiais.

> **Status:** Fase 1 concluída (fundação). O sistema **ainda não está operacional** e não deve
> ser usado para registros reais antes da homologação institucional.

## Requisitos

- Windows 10/11
- Python 3.14 (testado com 3.14.4)
- Git
- VS Code (opcional)
- PostgreSQL 17 (a partir da Fase 2)

## Instalação no Windows

No PowerShell, dentro da pasta do projeto:

```powershell
# 1. Criar o ambiente virtual (se ainda não existir)
py -3.14 -m venv venv

# 2. Ativar o ambiente virtual
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1

# 3. Instalar dependências
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Criar a configuração local
Copy-Item .env.example .env

# 5. Aplicar migrações
python manage.py migrate

# 6. Criar o administrador inicial
python manage.py createsuperuser

# 7. Iniciar o servidor de desenvolvimento
python manage.py runserver
```

Acesse:

- Aplicação: http://127.0.0.1:8000/
- Saúde: http://127.0.0.1:8000/health/
- Administração: http://127.0.0.1:8000/admin/

No `createsuperuser`, informe a **matrícula**, o **nome completo**, o **e-mail** e a senha.

## Testes

```powershell
.\venv\Scripts\Activate.ps1
python manage.py check
python manage.py test
```

Os testes usam um banco temporário e não alteram os dados locais.

## Estrutura

```
config/            configurações (base, dev, prod), URLs e views institucionais
apps/
  accounts/        usuário customizado e perfis
  inventory/       categorias, locais e materiais (Fase 3)
  loans/           empréstimos, devoluções e comprovantes (Fase 4)
  occurrences/     avarias e ocorrências (Fase 4/5)
  audit/           trilha de auditoria (Fase 5)
  reports/         painel e relatórios (Fase 5)
  contingency/     contingência e sincronização (Fase 6/7)
templates/         páginas HTML
static/            CSS e Bootstrap local
docs/              documentação técnica e operacional
```

## Documentação

- [Arquitetura](docs/arquitetura.md)
- [Dicionário de dados](docs/dicionario-de-dados.md)
- [Guia de administração](docs/guia-administracao.md)
- [Backup e restauração](docs/backup-restauracao.md)
- [Contingência](docs/contingencia.md)
- [Implantação](docs/implantacao.md)
- [Limitações conhecidas](docs/limitacoes-conhecidas.md)

## Segurança

- O arquivo `.env` contém segredos e **não** é versionado.
- Não use a chave de exemplo em produção.
- O ambiente `config.settings.prod` recusa iniciar sem `DJANGO_SECRET_KEY` e `DJANGO_ALLOWED_HOSTS`.
- A implantação oficial depende de autorização e homologação da UFMT.
