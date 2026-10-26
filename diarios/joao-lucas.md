# Diário — João Lucas

**Área:** Dados e editor

## Responsabilidades
- [ ] Models (`Curriculo`, `Experiencia`, `Formacao`, `Habilidade`, `Idioma`, `Curso`, `Projeto`) + migrations + admin
- [ ] `curriculos/forms.py`: ModelForm + inline formsets + validações (`clean()`)
- [ ] View `editor` (criar/editar) com `transaction.atomic()`
- [ ] `static/js/editor.js`: adicionar/remover itens
- [ ] Painel (lista), duplicar e excluir

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

### 10/26/2026

**O que fiz**
- Foi feita a modelagem inicial do app Curriculos que é o app principal do projeto. Foi feito inicialmente para testes e posteriormente pode ser alterado retirando ou adicionando informações.

- Tomei a decisão de deixar os tipos de escolaridade, níveis de linguagens e maestria em habilidades como enums para que fique mais fácil para deixar como botões selecionáveis mesmo sendo variáveis.

- Não houveram tantos problemas

- Próximo passo é iniciar o app de contas, montar as views iniciais e refinar o app curriculos

