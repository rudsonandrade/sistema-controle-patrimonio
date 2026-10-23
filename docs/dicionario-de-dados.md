# Dicionário de dados

Este documento descreve o modelo planejado e o que já está implementado. Apenas a entidade
`User` existe nesta fase.

## Implementado na Fase 1

### `accounts.User` (estende `AbstractUser`)

| Campo | Tipo | Regras |
|---|---|---|
| `id` | BigAutoField | Chave primária |
| `matricula` | CharField(20) | Única, obrigatória, login (`USERNAME_FIELD`) |
| `nome_completo` | CharField(150) | Obrigatório |
| `email` | EmailField | Único, obrigatório |
| `perfil` | CharField(20) | `administrador`, `atendente`, `auditor`, `solicitante` |
| `password` | CharField(128) | Hash do Django; nunca armazenado em texto puro |
| `is_active` | Boolean | Padrão `True` |
| `is_staff` | Boolean | Acesso à administração |
| `is_superuser` | Boolean | Todas as permissões |
| `last_login`, `date_joined` | DateTime | Controle do Django |
| `groups`, `user_permissions` | M2M | Permissões do Django |

A matrícula e o e-mail são únicos. O nome não é usado como chave.

## Planejado

### `inventory.Categoria`
`id`, `nome` (único), `descricao`, `ativa`, `criado_em`.

### `inventory.Local`
`id`, `nome` (único), `responsavel`, `descricao`, `ativo`, `criado_em`.

### `inventory.Material`
`id`, `codigo` (único e permanente), `numero_patrimonio` (único quando informado), `nome`,
`descricao`, `categoria` (FK PROTECT), `local` (FK PROTECT), `estado_conservacao`,
`situacao`, `data_cadastro`, `observacoes`, `criado_por` (FK usuário).
Situações: `disponivel`, `emprestado`, `manutencao`, `indisponivel`, `perdido`, `baixado`.
Itens baixados ou indisponíveis não podem ser emprestados.

### `loans.Solicitante`
`id`, `nome`, `matricula`, `email` (opcional), `usuario` (FK opcional), `observacoes`.
Separado de `User` porque o solicitante pode não ter conta no sistema.

### `loans.Emprestimo`
`id`, `protocolo` (único), `solicitante` (FK), `atendente` (FK usuário), `finalidade`,
`previsao_devolucao`, `status` (`aberto`, `devolvido`, `cancelado`), `data_retirada`,
`registrado_em`, `observacoes`.

### `loans.ItemEmprestimo`
`id`, `emprestimo` (FK), `material` (FK), `devolvido_em`, `condicao_devolucao`.
Restrição: no máximo um item aberto por material (constraint parcial no PostgreSQL).

### `loans.Devolucao`
`id`, `protocolo` (único), `emprestimo` (FK), `atendente` (FK), `data_efetiva`,
`registrado_em`, `idempotency_key` (única), `condicao`, `observacoes`, `status`
(`confirmada`, `contingencia`, `pendente`).

### `loans.Comprovante`
`id`, `devolucao` (1:1), `codigo_publico` (aleatório, único), `criado_em`, `hash_verificacao`.

### `occurrences.Ocorrencia`
`id`, `material` (FK), `emprestimo` (FK opcional), `tipo`, `descricao`, `situacao`,
`aberta_por` (FK), `aberta_em`, `resolvida_em`.

### `audit.AuditoriaEvento` (append-only)
`id`, `tipo`, `ator` (FK usuário), `entidade`, `entidade_id`, `estado_anterior` (JSON),
`estado_posterior` (JSON), `justificativa`, `evento_anterior` (FK self),
`correlacao` (UUID), `criado_em`, `endereco_ip` (quando necessário e autorizado).

### `contingency.RegistroContingencia`
`id`, `numero_documento` (único), `tipo_operacao`, `material`, `solicitante`,
`data_hora_efetiva`, `data_hora_lancamento`, `responsavel`, `observacoes`, `status_conciliacao`.

## Decisões de integridade

- Chaves primárias numéricas; nenhum código visual ou nome é chave.
- `PROTECT` em referências que não devem desaparecer silenciosamente.
- Protocolos únicos e `idempotency_key` para evitar duplicidade.
- Datas/hora e atendente definidos no servidor.
- Exclusões operacionais substituídas por cancelamento ou baixa com auditoria.
