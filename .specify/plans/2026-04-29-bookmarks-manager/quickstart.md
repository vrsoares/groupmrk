# Quickstart: 001-bookmarks-manager

---

## EN - English

### Install / Installation

```bash
pip install groupmrk
```

Or if you have the program already (from folder):

```bash
pip install -e .
```

---

### Basic Usage

**Import and organize bookmarks:**
```bash
groupmrk import bookmarks.html -o organized.html
```

This command:
1. Reads your bookmarks from `bookmarks.html`
2. Uses AI to organize them into categories
3. Saves organized bookmarks to `organized.html`

**Search bookmarks:**
```bash
groupmrk search "python tutorials" bookmarks.html
```

This finds bookmarks matching your search words.

**Export with filter:**
```bash
groupmrk export bookmarks.html output.html --category "Development"
```

---

### Options

| Option | What it does |
|--------|--------------|
| `--max-themes N` | Maximum number of categories (default: 10) |
| `--model MODEL` | Choose AI model |
| `--provider hf\|ollama` | Use HuggingFace (default) or Ollama |
| `--mock` | Test without calling AI (for testing) |

---

### Examples

```bash
# Import with only 5 categories
groupmrk import bookmarks.html -o organized.html --max-themes 5

# Test the program without using AI
groupmrk import bookmarks.html -o organized.html --mock

# Use local Ollama model
groupmrk import bookmarks.html --provider ollama

# Organize and change category manually
groupmrk organize bookmarks.html --set-category "python" "Programming"
```

---

## PT - Português

### Instalar

```bash
pip install groupmrk
```

Ou se voce ja tem o programa (da pasta):

```bash
pip install -e .
```

---

### Como usar

**Importar e organizar favoritos:**
```bash
groupmrk import favoritos.html -o organizados.html
```

Este comando:
1. Le seus favoritos de `favoritos.html`
2. Usa IA para organizar em categorias
3. Salva os favoritos organizados em `organizados.html`

**Buscar favoritos:**
```bash
groupmrk search "tutoriais python" favoritos.html
```

Isso encontra favoritos que matching suas palavras de busca.

**Exportar com filtro:**
```bash
groupmrk export favoritos.html saida.html --category "Desenvolvimento"
```

---

### Opcoes

| Opcao | O que faz |
|-------|-----------|
| `--max-themes N` | Numero maximo de categorias (padrao: 10) |
| `--model MODEL` | Escolhe modelo de IA |
| `--provider hf\|ollama` | Usa HuggingFace (padrao) ou Ollama |
| `--mock` | Testa sem chamar IA (para testes) |

---

### Exemplos

```bash
# Importar com apenas 5 categorias
groupmrk import favoritos.html -o organizados.html --max-themes 5

# Testar o programa sem usar IA
groupmrk import favoritos.html -o organizados.html --mock

# Usar modelo local Ollama
groupmrk import favoritos.html --provider ollama

# Organizar e mudar categoria manualmente
groupmrk organize favoritos.html --set-category "python" "Programacao"
```

---

## Troubleshooting / Solucao de problemas

**Problem:** "File too large"
- Solution: Your file is bigger than 10MB. Trim some bookmarks.

**Problem:** "No results found"
- Solution: Try different search words or check the file has bookmarks.

**Problem:** API errors
- Solution: Use `--mock` flag to test without API, or use `--provider ollama` for local AI.

---

## More info / Mais info

- Full documentation: README.md
- Report problems: GitHub issues