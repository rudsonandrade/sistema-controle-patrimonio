# Arquitetura

## Visão geral

Aplicação web monolítica em Django 5.2 LTS, com renderização no servidor e JavaScript
pontual. O objetivo é simplicidade operacional, integridade transacional e auditabilidade.

```
Navegador
   │ HTTPS (produção)
   ▼
Django (views, forms, permissões)
   │ ORM / transações
   ▼
PostgreSQL (produção e desenvolvimento a partir da Fase 2)
```

## Componentes

| Módulo | Responsabilidade |
|---|---|
| `config` | Configurações por ambiente, URLs raiz, health check |
| `apps.accounts` | Usuário customizado, perfis e permissões |
| `apps.inventory` | Categorias, locais e materiais |
| `apps.loans` | Empréstimos, devoluções e comprovantes |
| `apps.occurrences` | Avarias e ocorrências |
| `apps.audit` | Eventos de auditoria append-only e correções |
| `apps.reports` | Painel, consultas e exportações |
| `apps.contingency` | Registros de contingência e sincronização futura |

## Decisões

1. **Django 5.2 LTS**: compatível com Python 3.14 desde a 5.2.8 e com suporte de longo prazo.
2. **Usuário customizado desde a primeira migração**: `AUTH_USER_MODEL = "accounts.User"`,
   login por matrícula institucional.
3. **Perfis**: administrador, atendente, auditor e solicitante. A autorização efetiva será
   aplicada com grupos e permissões do Django no backend (Fase 2).
4. **PostgreSQL em produção**: o desenvolvimento usará o mesmo SGBD a partir da Fase 2.
   SQLite permanece apenas como fallback inicial e para testes leves.
5. **Bootstrap servido localmente**: evita dependência de CDN e funciona em rede restrita.
6. **Configuração por ambiente**: `.env` não versionado; `prod.py` falha se segredos não forem
   definidos.
7. **Idioma e fuso**: interface em português brasileiro; `America/Cuiaba`; `USE_TZ=True`.
8. **Integridade**: transações atômicas, `select_for_update` e restrições de unicidade para
   impedir empréstimos duplicados (Fase 4).
9. **Auditoria append-only**: correções geram novos eventos, preservando o histórico (Fase 5).
10. **Offline/PWA adiado**: só será implementado após o núcleo estar homologado (Fase 7).

## Ambientes

- `config.settings.dev`: desenvolvimento local, SQLite por padrão, DEBUG conforme `.env`.
- `config.settings.prod`: HTTPS, cookies seguros, HSTS, WhiteNoise, exigência de segredos.
- Testes: `manage.py test` usa as configurações de desenvolvimento e cria banco temporário.

## Requisitos de infraestrutura (produção)

- Servidor Linux institucional com Python 3.14 e PostgreSQL 17.
- Servidor de aplicação WSGI/ASGI atrás de proxy HTTPS.
- Armazenamento de backup independente do servidor principal.
- Definição institucional de retenção, privacidade e resposta a incidentes.

Nenhum serviço externo é presumido ou utilizado.
