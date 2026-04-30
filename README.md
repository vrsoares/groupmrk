# groupmrk

An open-source browser bookmarks manager powered by LLM. Organize, search, and categorize your bookmarks using artificial intelligence.

---

## English

### Overview

groupmrk is a CLI tool that helps you manage your browser bookmarks with the power of Large Language Models. It can automatically categorize, tag, and search through your bookmarks using natural language queries.

### Features

- **AI-Powered Categorization**: Automatically organize bookmarks into meaningful groups
- **Natural Language Search**: Find bookmarks using everyday language
- **Tag Management**: Intelligent auto-tagging based on content analysis
- **Import/Export**: Support for standard browser bookmark formats
- **Cross-Browser**: Works with Chrome, Firefox, Edge, and others

### Installation

```bash
pip install groupmrk
```

### Usage

```bash
# Import bookmarks from a file
groupmrk import bookmarks.html

# List all bookmarks
groupmrk list

# Search bookmarks using natural language
groupmrk search "python tutorials"

# Auto-categorize uncategorized bookmarks
groupmrk organize

# Export bookmarks
groupmrk export bookmarks_export.html
```

### Configuration

Create a `.env` file in your project directory:

```env
OPENAI_API_KEY=your_api_key_here
```

### License

MIT

---

## Português

### Visão Geral

groupmrk é uma ferramenta de CLI que ajuda você a gerenciar seus favoritos do navegador com o poder dos Modelos de Linguagem de Grande Escala. Ele pode categorizar, marcar e pesquisar automaticamente em seus favoritos usando linguagem natural.

### Recursos

- **Categorização com IA**: Organize automaticamente favoritos em grupos significativos
- **Pesquisa em Linguagem Natural**: Encontre favoritos usando linguagem cotidiana
- **Gerenciamento de Tags**: Marcação automática baseada em análise de conteúdo
- **Importar/Exportar**: Suporte para formatos padrão de favoritos do navegador
- **Multi-Navegador**: Funciona com Chrome, Firefox, Edge e outros

### Instalação

```bash
pip install groupmrk
```

### Uso

```bash
# Importar favoritos de um arquivo
groupmrk import favoritos.html

# Listar todos os favoritos
groupmrk list

# Pesquisar favoritos usando linguagem natural
groupmrk search "tutoriais python"

# Categorizar favoritos não categorizados
groupmrk organize

# Exportar favoritos
groupmrk export favoritos_export.html
```

### Configuração

Crie um arquivo `.env` no diretório do seu projeto:

```env
OPENAI_API_KEY=sua_chave_api_aqui
```

### Licença

MIT