# Diário — Leonardo Soares

**Área:** Base do projeto, contas e integração

## Responsabilidades
- [x] Etapa 1: criar o projeto Django (`config`), os apps `contas` e `curriculos`, o `settings.py` e o `requirements.txt`
- [x] `templates/base.html` (navbar, Bootstrap via CDN, mensagens)
- [x] App `contas`: cadastro, login e logout
- [ ] Segurança: `@login_required` e filtro por dono em todas as views
- [ ] Testes básicos (outro usuário → 404, editor salva)
- [ ] Etapa opcional: geração por texto com IA (`ia.py`, view `gerar_texto`)

---

## Como registrar
Uma entrada por dia de trabalho, a mais recente no topo. Copie o modelo abaixo.

```
### AAAA-MM-DD
**O que fiz:**
-
**Decisões / por quê:**
-
**Problemas e como resolvi:**
-
**Próximos passos:**
-
```

---

## Registros

<!-- novas entradas aqui -->

### 2026-10-26
**O que fiz:**
- Criei o projeto Django (`config`) e o app `contas` na raiz, conforme o ESTRUTURA.md
- Movi o app `curriculos` do João de `src/app/` para a raiz (a migration continua válida)
- `settings.py`: apps, pt-br, fuso de São Paulo, pasta `templates/`, `static/`, URLs de login/logout
- `base.html` com Bootstrap 5, Bootstrap Icons, navbar e mensagens
- App `contas`: cadastro (`CadastroForm` com e-mail), login e logout (views do Django)
- Home e painel simples (o João completa o painel)
- `requirements.txt` com o Django

**Decisões / por quê:**
- Logout por formulário POST na navbar: o Django 5+ não aceita logout por GET (proteção contra CSRF)
- Projeto na raiz em vez de `src/`: segue o plano e o `manage.py` fica onde todos esperam

**Problemas e como resolvi:**
- O repositório não tinha projeto Django, só o app. O projeto foi criado e o app foi movido para a raiz

**Próximos passos:**
- Antes do deploy: tirar `SECRET_KEY` e `DEBUG` do código e passar para variável de ambiente
- Testes de acesso (outro usuário → 404) quando o editor existir

**Como rodar o projeto:**
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
