# Limitações conhecidas

## Fase 1

- O sistema **não é operacional** para empréstimos e devoluções.
- Apenas o modelo de usuário, os perfis e a estrutura inicial existem.
- O banco local padrão é SQLite; PostgreSQL será configurado na Fase 2.
- As permissões por perfil ainda não são aplicadas em telas operacionais.
- Não há telas de atendimento, comprovantes, relatórios ou auditoria.
- O modo offline/PWA não foi implementado (previsto para a Fase 7).
- A contingência em papel está documentada, mas ainda não há campo de lançamento posterior.
- Não há backup automatizado nem restauração testada (Fase 6).
- Não há integração com autenticação institucional.
- A interface usa Bootstrap local; pode ser ajustada após avaliação de acessibilidade.

## Riscos residuais

- Python 3.14 é recente; dependências devem permanecer fixadas e revisadas.
- A auditoria em nível de aplicação não impede alteração direta por administrador do banco.
- Datas e fusos dependem da configuração correta do servidor.
- A impressão de comprovantes depende do navegador até a definição da geração de PDF.

## Fora de escopo nesta fase

- Implantação em produção.
- Envio de e-mail real.
- Autenticação institucional (SSO).
- Assinatura digital ou certificação externa.
- Aplicativo móvel nativo.
