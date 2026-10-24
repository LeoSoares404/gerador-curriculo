# Gerador de Currículo — Planejamento da Estrutura

Este documento detalha **como** o site será construído e **por que** cada decisão foi tomada. O "o quê" está em [ESCOPO.md](ESCOPO.md).

Princípio geral: **usar o que o Django e o navegador já oferecem antes de escrever código ou instalar bibliotecas.** Menos código = menos bugs, e fica mais fácil explicar na apresentação.

---

## 1. Visão geral da arquitetura

```
Navegador (HTML + Bootstrap + JS)
        │  requisições HTTP (GET/POST)
        ▼
Django: urls.py → views.py → forms.py / models.py → templates (HTML)
        │
        ▼
SQLite (db.sqlite3)
```

- **Renderização no servidor (templates do Django), sem API REST.**
  *Por quê:* o Django já monta o HTML com os dados. Uma API + front em JS puro dobraria o trabalho (duas camadas, serialização, autenticação por token) sem ganho para um projeto acadêmico.
- **JS só onde precisa:** adicionar/remover itens nas seções repetíveis e pequenas interações. *Por quê:* o resto o HTML e o Bootstrap resolvem.

---

## 2. Estrutura de pastas

```
gerador-curriculo/
├── manage.py
├── requirements.txt          # Django, Pillow
├── config/                   # projeto Django
│   ├── settings.py
│   └── urls.py
├── contas/                   # app de usuários
│   ├── forms.py              # CadastroForm
│   ├── views.py              # cadastro
│   ├── urls.py               # cadastro, login, logout
│   └── templates/registration/
│       ├── login.html
│       └── cadastro.html
├── curriculos/               # app de currículos
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── ia.py                 # (opcional) chamada à API de IA
│   └── templates/curriculos/
│       ├── home.html
│       ├── painel.html
│       ├── editor.html
│       ├── gerar_texto.html  # (opcional) caixa de texto livre
│       ├── confirmar_exclusao.html
│       └── modelos/
│           ├── classico.html
│           ├── moderno.html
│           ├── minimalista.html
│           ├── criativo.html
│           └── executivo.html
├── templates/
│   └── base.html             # layout comum (navbar, Bootstrap, mensagens)
├── static/
│   ├── css/style.css         # estilos + regras @media print
│   └── js/editor.js          # adicionar/remover itens dos formulários
└── media/                    # fotos enviadas (gerada automaticamente)
```

**Decisões:**

- **Projeto chamado `config`.** *Por quê:* deixa claro que a pasta guarda só configuração, separando-a do app com o código de negócio.
- **Dois apps: `contas` e `curriculos`.** *Por quê:* cada app tem uma responsabilidade só. `contas` cuida de usuários (cadastro, login, logout) e `curriculos` cuida dos currículos. O código de contas é pequeno, porque login/logout vêm prontos no `django.contrib.auth`, mas fica no lugar certo e já tem espaço para perfil ou troca de senha. Também mostra na avaliação o uso correto da divisão em apps, conceito central do Django.
- **Templates de login em `registration/`.** *Por quê:* é a pasta onde as views de autenticação do Django procuram os templates por padrão, então não é preciso configurar nada.
- **`base.html` na pasta global `templates/`.** *Por quê:* todas as páginas herdam dele (`{% extends %}`), então a navbar e o Bootstrap ficam num lugar só.
- **Um CSS e um JS.** *Por quê:* o projeto é pequeno, e vários arquivos só aumentariam os `<link>`/`<script>` sem organizar nada.

---

## 3. Modelo de dados

```
User (Django) 1 ──── N Curriculo 1 ──── N Experiencia
                                  ├──── N Formacao
                                  ├──── N Habilidade
                                  ├──── N Idioma
                                  ├──── N Curso
                                  └──── N Projeto
```

### `Curriculo`
| Campo | Tipo | Observação |
|---|---|---|
| usuario | ForeignKey(User) | dono do currículo |
| titulo | CharField | ex.: "Currículo — Estágio TI" (só aparece no painel) |
| modelo | CharField(choices) | `classico` / `moderno` / `minimalista` / `criativo` / `executivo` |
| nome, email, telefone, cidade | CharField / EmailField | dados pessoais |
| linkedin, site | URLField (opcional) | |
| foto | ImageField (opcional) | exige Pillow |
| resumo | TextField | objetivo profissional |
| criado_em / atualizado_em | DateTimeField | `auto_now_add` / `auto_now` |

### Seções repetíveis (todas com `curriculo = ForeignKey(Curriculo, on_delete=CASCADE, related_name=...)`)
| Model | Campos |
|---|---|
| Experiencia | empresa, cargo, inicio, fim (opcional), atual (bool), descricao |
| Formacao | instituicao, curso, nivel (choices), inicio, fim (opcional) |
| Habilidade | nome, nivel (choices: básico/intermediário/avançado) |
| Idioma | idioma, nivel (choices) |
| Curso | nome, instituicao, ano |
| Projeto | nome, descricao, link (opcional) |

**Decisões:**

- **Dados pessoais dentro do próprio `Curriculo`, sem tabela `DadosPessoais` separada.** *Por quê:* a relação é 1 para 1, e uma tabela à parte só traria um JOIN e um formulário a mais. Ficar dentro do `Curriculo` também permite que cada currículo tenha um e-mail ou telefone diferente.
- **Uma tabela por seção repetível.** *Por quê:* cada seção tem campos diferentes. Uma tabela genérica "Item" com campos `texto1`, `texto2`... seria confusa e impossível de validar.
- **`on_delete=CASCADE`.** *Por quê:* ao excluir um currículo, os itens dele não têm mais sentido e são apagados junto.
- **`related_name` (ex.: `curriculo.experiencias.all`).** *Por quê:* deixa os templates legíveis.
- **`choices` para nível e modelo.** *Por quê:* o banco só aceita valores válidos, o formulário vira um `<select>` automaticamente e o template pode usar `get_nivel_display`.
- **Ordenação por data (`Meta.ordering = ['-inicio']`), sem campo "ordem" manual.** *Por quê:* num currículo a experiência mais recente vem primeiro, o que é o padrão esperado. Reordenar arrastando ficaria como melhoria futura.
- **Datas como `DateField`.** *Por quê:* o Django gera um `<input type="date">`, que é o seletor de data nativo do navegador e dispensa bibliotecas de calendário.

---

## 4. URLs e views

| URL | View | Acesso | Função |
|---|---|---|---|
| `/` | `home` | público | página inicial |
| `/contas/cadastro/` | `contas.cadastro` | público | criar conta (`CadastroForm`, baseado no `UserCreationForm`) |
| `/contas/login/`, `/contas/logout/` | `LoginView`, `LogoutView` (Django) | público | autenticação pronta |
| `/painel/` | `painel` | logado | lista os currículos do usuário |
| `/curriculo/novo/` | `editor` | logado | cria um currículo |
| `/curriculo/<id>/editar/` | `editor` | logado + dono | edita o currículo |
| `/curriculo/<id>/` | `visualizar` | logado + dono | exibe com o layout escolhido |
| `/curriculo/<id>/duplicar/` | `duplicar` | logado + dono (POST) | copia o currículo e os itens |
| `/curriculo/<id>/excluir/` | `excluir` | logado + dono | confirmação + exclusão |
| `/curriculo/gerar/` | `gerar_texto` | logado | (opcional) texto livre → IA → editor pré-preenchido |
| `/admin/` | admin do Django | superusuário | gestão dos dados |

**Decisões:**

- **Views em função (FBV), não em classe (CBV).** *Por quê:* o editor salva um formulário e seis formsets de uma vez, e numa função o fluxo fica explícito, de cima para baixo. As CBVs genéricas escondem esse fluxo em métodos herdados, o que dificulta explicar e depurar. Para manter um padrão só, as outras views também serão funções.
- **Uma única view `editor` para criar e editar.** *Por quê:* a lógica é a mesma, e a única diferença é existir ou não um `id`, o que evita duplicar código.
- **Login e logout do próprio Django.** *Por quê:* são seguros e testados, e basta escrever o template.
- **Duplicar e excluir só por POST.** *Por quê:* ações que alteram dados não podem acontecer por um link GET, que pode ser acessado por engano ou pré-carregado pelo navegador. O POST também passa pela proteção CSRF.

---

## 5. Editor de currículo (a parte central)

- **Uma única página com as seções em um *accordion* do Bootstrap**, e não um passo a passo (wizard) com várias telas.
  *Por quê:* um wizard exigiria guardar o estado entre as etapas (sessão ou rascunho no banco). Com uma página só, existe um único formulário e um único botão "Salvar", e o accordion evita que a página fique longa demais.
- **`ModelForm` para o `Curriculo` + `inlineformset_factory` para cada seção.**
  *Por quê:* os formsets inline do Django já tratam vários itens filhos ao mesmo tempo (criar, editar e excluir, com o campo `DELETE`) e a validação. Escrever isso à mão daria muito mais código.
- **JS do botão "Adicionar item":** clona o `formset.empty_form` (que o Django fornece com `__prefix__`), troca o prefixo pelo próximo índice e incrementa o `TOTAL_FORMS`. São cerca de 20 linhas, sem bibliotecas.
  *Por quê:* é o método oficial documentado para formsets dinâmicos.
- **Validação em duas camadas:** atributos HTML5 (`required`, `type="email"`, `type="url"`), que o Django já gera, mais a validação dos forms no servidor. Regra extra: em `Experiencia`, se `atual` estiver marcado, `fim` deve ficar vazio, e caso contrário `fim` não pode ser anterior a `inicio` (`clean()` do form).
  *Por quê:* a validação no front dá retorno imediato, mas pode ser burlada, por isso o servidor é quem decide.
- **Tudo salvo dentro de `transaction.atomic()`.** *Por quê:* se um formset falhar no meio, nada fica salvo pela metade.

---

## 6. Modelos visuais e exportação

- **5 layouts, cada um é um template HTML** (`classico`, `moderno`, `minimalista`, `criativo`, `executivo`), e a view `visualizar` escolhe qual renderizar a partir do campo `modelo`:
  `render(request, f'curriculos/modelos/{curriculo.modelo}.html', ...)`
  *Por quê:* criar um layout novo é só criar um arquivo novo e acrescentar uma opção no `choices`. Como o valor vem de `choices`, não há risco de carregar um template arbitrário.
- **A escolha do modelo fica dentro do editor (cards com miniatura + radio button)**, não numa página separada.
  *Por quê:* é um campo do currículo como qualquer outro, e uma página própria seria só uma tela a mais.
- **PDF pelo próprio navegador:** botão "Baixar PDF" chama `window.print()`, e o CSS `@media print` esconde a navbar e os botões e ajusta margens (`@page { size: A4; margin: 15mm; }`).
  *Por quê:* todo navegador moderno salva em PDF. Bibliotecas como WeasyPrint precisam de dependências de sistema (GTK no Windows), que são difíceis de instalar e não dão um resultado muito melhor. Se o professor exigir download direto em PDF, a opção mais leve é o `xhtml2pdf`.

---

## 7. Gerar currículo a partir de texto (opcional — IA)

**Fluxo:**
1. Em `/curriculo/gerar/`, o usuário escreve um texto livre sobre si.
2. A view `gerar_texto` envia o texto para a API de IA (ex.: API do Claude), pedindo a resposta em **JSON no formato dos nossos models** (`nome`, `experiencias: [...]`, `formacoes: [...]`, `habilidades: [...]` etc.).
3. O JSON é validado e usado como `initial` do form e dos formsets, e o **editor abre pré-preenchido**.
4. O usuário revisa, corrige e clica em Salvar. A partir daí o fluxo é igual ao manual.

**Decisões:**
- **A IA só preenche o editor e nunca salva direto.** *Por quê:* a IA pode errar uma data, um nome ou inventar algo. O usuário precisa conferir, e assim reaproveitamos toda a validação dos forms.
- **Recurso opcional e isolado em `curriculos/ia.py`.** *Por quê:* se a API estiver fora do ar, a chave não estiver configurada ou o professor não quiser dependência externa, o botão some e o site continua completo. O resto do código não depende da IA.
- **Chamada pelo servidor (Django), não pelo JavaScript.** *Por quê:* a chave da API não pode ficar no navegador, onde qualquer pessoa a veria.
- **Chave em variável de ambiente (`ANTHROPIC_API_KEY`), nunca no código nem no Git.** *Por quê:* uma chave vazada gera custo para quem é dono dela.
- **Limite de tamanho no texto (ex.: 3.000 caracteres).** *Por quê:* controla o custo por chamada e evita abuso.
- **Tratamento de erro:** se a resposta não for um JSON válido ou a API falhar, mostra a mensagem "Não foi possível gerar, preencha manualmente" e mantém o texto digitado.

**Dependência extra:** `anthropic` (SDK oficial). Entra no `requirements.txt` só quando essa etapa for feita.

---

## 8. Front-end

- **Bootstrap 5 via CDN no `base.html`.** *Por quê:* não exige instalação nem npm.
- **Bootstrap Icons via CDN** para os ícones (editar, excluir, duplicar).
- **Mensagens de feedback** ("Currículo salvo!") pelo `django.contrib.messages` exibidas como `alert` do Bootstrap no `base.html`. *Por quê:* já vem habilitado no Django.
- **Responsividade:** o grid do Bootstrap (`row`/`col-md-*`) já resolve. Os layouts de currículo são pensados para A4, mas se ajustam a telas pequenas na visualização.

---

## 9. Segurança

| Risco | Como é tratado | Por quê |
|---|---|---|
| Acessar páginas sem login | `@login_required` | redireciona para `/login/` |
| Vazamento da chave da IA | variável de ambiente + chamada só no servidor | a chave nunca chega ao navegador nem ao Git |
| Ver/editar currículo de outra pessoa trocando o `id` na URL | `get_object_or_404(Curriculo, pk=id, usuario=request.user)` em toda view | quem não é dono recebe 404, sem nem saber que o currículo existe |
| Envio de formulário forjado (CSRF) | `{% csrf_token %}` + middleware padrão | já vem ativo no Django |
| Injeção de HTML/JS nos campos (XSS) | escape automático dos templates | nunca usar `|safe` em dados do usuário |
| Senhas | hash do Django (PBKDF2) + validadores de senha padrão | nada a implementar |
| Upload de foto | `ImageField` (valida se é imagem) + limite de tamanho no form | evita arquivos que não são imagem e arquivos enormes |

---

## 10. Configurações (`settings.py`)

- `LANGUAGE_CODE = 'pt-br'`, `TIME_ZONE = 'America/Sao_Paulo'`: mensagens de erro e o admin em português.
- `INSTALLED_APPS += ['contas', 'curriculos']`.
- `LOGIN_URL = 'login'`, `LOGIN_REDIRECT_URL = 'painel'`, `LOGOUT_REDIRECT_URL = 'home'`.
- `STATICFILES_DIRS = [BASE_DIR / 'static']`, `MEDIA_URL` / `MEDIA_ROOT` para as fotos.
- `TEMPLATES['DIRS'] = [BASE_DIR / 'templates']`.
- **Banco SQLite.** *Por quê:* é um arquivo único, sem servidor, e já vem configurado. Para trocar por PostgreSQL basta alterar o `DATABASES`.

**Dependências (`requirements.txt`):** `Django` e `Pillow` (necessária para o `ImageField`). `anthropic` só se a etapa de IA for feita.

---

## 11. Ordem de implementação

1. `django-admin startproject config .` + `startapp contas` + `startapp curriculos`, configurar o settings e o `base.html` com Bootstrap.
2. App `contas`: cadastro, login e logout.
3. Models + `makemigrations`/`migrate` + registro no admin (o admin serve para testar os models antes de existir tela).
4. Painel + editor com o form principal.
5. Formsets das seções + `editor.js`.
6. Templates dos 5 modelos + visualização + CSS de impressão.
7. Duplicar/excluir, mensagens, validações extras.
8. Testes básicos (acesso de outro usuário retorna 404, editor salva os formsets) + revisão visual.
9. **(Opcional)** Geração por texto com IA: `ia.py`, view `gerar_texto`, editor pré-preenchido.

*Por que nessa ordem:* cada etapa depende da anterior, e ao final de cada uma já existe algo funcionando que pode ser mostrado. A IA fica por último porque o site precisa estar completo sem ela.

---

## 12. O que foi deixado de fora e quando adicionar

| Item | Adicionar quando |
|---|---|
| Exportação PDF no servidor | o professor exigir download direto |
| Reordenar itens arrastando | o usuário precisar de uma ordem diferente da cronológica |
| Recuperação de senha por e-mail | houver servidor de e-mail configurado (as views do Django já existem) |
| API REST / front em framework JS | houver app mobile ou outro cliente |
