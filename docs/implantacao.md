# Implantação

## Situação atual

A implantação oficial **não está autorizada** e depende de homologação da UFMT. Este documento
descreve apenas a preparação técnica.

## Pré-requisitos

- Servidor Linux institucional com Python 3.14.
- PostgreSQL 17.
- Proxy reverso com HTTPS (por exemplo, servidor web institucional).
- Servidor WSGI/ASGI (a definir na instituição).
- Armazenamento de backup independente.

## Configuração de produção

1. Criar ambiente virtual e instalar `requirements.txt`.
2. Definir as variáveis de ambiente:
   - `DJANGO_SECRET_KEY` forte e exclusiva;
   - `DJANGO_DEBUG=False`;
   - `DJANGO_ALLOWED_HOSTS`;
   - `DB_ENGINE=postgresql` e credenciais do banco;
   - `DJANGO_CSRF_TRUSTED_ORIGINS` com o domínio HTTPS.
3. Executar `python manage.py migrate`.
4. Executar `python manage.py collectstatic --noinput`.
5. Iniciar o servidor de aplicação usando `config.settings.prod`.
6. Configurar o proxy para encaminhar HTTPS e o cabeçalho `X-Forwarded-Proto`.
7. Verificar `/health/` e os cabeçalhos de segurança.

## Checklist antes da homologação

- [ ] PostgreSQL com backup automatizado e restauração testada.
- [ ] HTTPS válido e redirecionamento forçado.
- [ ] `DEBUG=False` e segredos fora do código.
- [ ] Usuários e permissões revisados.
- [ ] Testes automatizados executados.
- [ ] Política de privacidade e retenção aprovada.
- [ ] Procedimento de contingência impresso e distribuído.
- [ ] Equipe treinada.
- [ ] Autorização formal da UFMT.

## O que não fazer

- Não usar o servidor de desenvolvimento (`runserver`) em produção.
- Não usar as credenciais de exemplo do `.env.example`.
- Não publicar o sistema na internet sem autorização.
- Não enviar dados a serviços externos sem aprovação institucional.
