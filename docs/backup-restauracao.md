# Backup e restauração

## Situação atual

A estratégia completa e os scripts testados serão implementados na Fase 6. Esta é a política
inicial.

## Objetivos (a aprovar pela gestão)

- **RPO (perda máxima de dados):** a definir institucionalmente. Proposta inicial: até 24 horas.
- **RTO (tempo máximo de indisponibilidade):** a definir institucionalmente. Proposta inicial:
  até 8 horas.

## Escopo

- Banco de dados PostgreSQL (produção).
- Código da aplicação e dependências fixadas.
- Arquivos de configuração essenciais, sem expor segredos.
- Documentos de contingência digitalizados, quando existirem.

## Diretrizes

1. Executar backup automático diário do banco.
2. Armazenar cópias em local independente do servidor principal.
3. Criptografar backups que contenham dados pessoais.
4. Registrar data, resultado e responsável por cada execução.
5. Testar restauração periodicamente em ambiente separado.
6. Nunca considerar o backup válido apenas porque o comando foi executado.
7. Manter retenção definida pela gestão, com descarte seguro ao final.

## Restauração (procedimento futuro)

1. Interromper a aplicação.
2. Criar banco de teste vazio.
3. Restaurar o dump mais recente.
4. Executar `python manage.py migrate --check` e testes de integridade.
5. Validar contagens e registros recentes.
6. Somente então apontar a aplicação para o banco restaurado.
7. Registrar o incidente e o resultado.

Os comandos exatos serão documentados e testados na Fase 6.
