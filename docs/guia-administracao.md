# Guia de administração

## Criar o primeiro administrador

```powershell
.\venv\Scripts\Activate.ps1
python manage.py createsuperuser
```

Informe matrícula, nome completo, e-mail e senha. O perfil será automaticamente
`administrador`.

## Acessar a administração

- URL: http://127.0.0.1:8000/admin/
- Login: matrícula e senha.

## Perfis previstos

| Perfil | Uso |
|---|---|
| Administrador do sistema | Usuários, cadastros, parâmetros, auditoria |
| Servidor responsável pelo atendimento | Empréstimos, devoluções, comprovantes, ocorrências |
| Gestor ou auditor autorizado | Consultas, relatórios e auditoria, sem alteração operacional |
| Solicitante | Acesso futuro aos próprios empréstimos, quando autorizado |

Na Fase 1, os perfis estão definidos no modelo. A aplicação efetiva de permissões por grupo
ocorre na Fase 2, sempre no backend.

## Boas práticas

- Não compartilhe contas; cada servidor deve ter usuário próprio.
- Desative imediatamente usuários desligados ou afastados.
- Não registre dados pessoais desnecessários.
- Não edite registros diretamente no banco em produção.
- Em caso de correção, use o fluxo de auditoria que será implementado na Fase 5.
