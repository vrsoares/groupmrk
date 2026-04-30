# groupmrk

Um programa de organizacao de favoritos do navegador com IA. Organize, pesquise e categorize seus favoritos usando inteligencia artificial.

---

## English

### What is this?

**groupmrk** is a simple program that helps you organize your browser bookmarks (also called "favorites") using artificial intelligence. You give it your bookmarks, and it automatically organizes them into groups like "Development", "Tutorials", "News", and more.

You don't need to know anything about programming to use it!

### What can it do?

- **Automatic Organization**: Put your bookmarks in, get them organized automatically
- **Natural Search**: Find bookmarks by typing "python tutorials" instead of searching in folders
- **Works Everywhere**: Works with Chrome, Firefox, Edge, and other browsers
- **No Account Needed**: No login, no password, no API key required

### How to Install (Step by Step)

Choose your computer below and follow the steps:

#### Windows

1. **Download Python**
   - Go to: https://www.python.org/downloads/
   - Click the button: "Download Python 3.12.x"
   - Wait for the file to download

2. **Install Python**
   - Double-click the downloaded file
   - **IMPORTANT**: Check the box that says "Add Python to PATH" (very important!)
   - Click "Install Now"
   - Wait for it to finish
   - Close the window

3. **Install groupmrk**
   - Open Command Prompt (press Windows key + R, type "cmd", press Enter)
   - Type: `pip install groupmrk`
   - Press Enter and wait

4. **Done!** Now you can use it!

#### macOS (Apple)

1. **Check if you have Python**
   - Open Terminal (press Cmd + Space, type "Terminal", press Enter)
   - Type: `python3 --version`
   - If it says "command not found", continue below

2. **Install Python**
   - Go to: https://www.python.org/downloads/
   - Click: "Download Python 3.12.x"
   - Open the downloaded file and follow the steps

3. **Install groupmrk**
   - In Terminal, type: `pip3 install groupmrk`
   - Press Enter and wait

4. **Done!**

#### Linux (Ubuntu and similar)

1. **Open Terminal**
   - Press Ctrl + Alt + T

2. **Install Python** (if not installed)
   - Type: `sudo apt update`
   - Press Enter
   - Type: `sudo apt install python3 python3-pip`
   - Press Enter and type your password

3. **Install groupmrk**
   - Type: `pip3 install groupmrk`
   - Press Enter

4. **Done!**

#### Linux (Fedora)

1. **Open Terminal**

2. **Install Python**
   - Type: `sudo dnf install python3 pip`
   - Press Enter

3. **Install groupmrk**
   - Type: `pip3 install groupmrk`

4. **Done!**

#### Linux (Debian)

1. **Open Terminal**

2. **Install Python**
   - Type: `sudo apt update && sudo apt install python3 python3-pip`
   - Press Enter

3. **Install groupmrk**
   - Type: `pip3 install groupmrk`

4. **Done!**

---

## How to Use (Examples)

### IMPORTANT: Where to Run Commands

Before running any command, you need to be in the right folder!

**Check your current folder:**
- **Windows**: In Command Prompt, look at what comes before the `>` symbol
  - Example: `C:\Users\YourName\Documents\bookmarks>` - you're in the "bookmarks" folder
  - If it shows `C:\Users\YourName>` - you're in your home folder
  
- **macOS/Linux**: In Terminal, look at what comes before `$`
  - Example: `~/Documents/bookmarks$` - you're in the "bookmarks" folder
  - If it shows `~` or `$HOME` - you're in your home folder

**To change folder:**
- **Windows**: `cd Documents\bookmarks` (use backslash `\`)
- **macOS/Linux**: `cd Documents/bookmarks` (use forward slash `/`)

### 1. Organize Your Bookmarks

```bash
groupmrk import my_bookmarks.html --output organized.html --mock
```

This will:
- Read your bookmarks from "my_bookmarks.html"
- Organize them using AI (the --mock flag makes it fast for testing)
- Save the organized version to "organized.html"

### 2. Search Your Bookmarks

```bash
groupmrk search "python tutorials" organized.html
```

This will find bookmarks about Python tutorials!

### 3. Export to Browser Format

```bash
groupmrk export organized.html final_bookmarks.html
```

### 4. Get Help

```bash
groupmrk --help
```

---

### Quick Start (5 minutes)

1. Export your bookmarks from your browser:
   - **Chrome**: Click three dots → Bookmarks → Bookmark manager → Export
   - **Firefox**: Click three lines → Bookmarks → Show all bookmarks → Import and Backup → Export
   - **Edge**: Click three dots → Favorites → Export favorites

2. Save the file (let's call it "bookmarks.html")

3. Open terminal/command prompt

4. Navigate to the folder where you saved bookmarks.html
   - Use `cd` command to change to that folder

5. Run: `groupmrk import bookmarks.html --output organized.html --mock`

6. Open "organized.html" in your browser and import it!

---

### Troubleshooting

**"pip" is not recognized (Windows)**
- Make sure you checked "Add Python to PATH" during installation
- Or try: `python -m pip install groupmrk`

**"command not found" (macOS/Linux)**
- Try using `pip3` instead of `pip`

**It says "No LLM client available"**
- Make sure you have internet connection
- Or use the `--mock` flag for testing

**"File not found" error**
- Make sure the bookmark file exists in the folder where you're running the command
- Check that you're in the correct folder with `cd`

---

### License

MIT - Free to use, modify, and share!

---

## Portugues

### O que e isto?

**groupmrk** e um programa que ajuda voce a organizar seus favoritos do navegador usando inteligencia artificial. Voce entrega os favoritos e ele organiza automaticamente em grupos como "Desenvolvimento", "Tutoriais", "Noticias", e mais.

Voce nao precisa saber programacao para usar!

### O que ele faz?

- **Organizacao Automatica**: Coloque os favoritos, receba organizados
- **Pesquisa Natural**: Encontre favoritos digitando "tutoriais python" em vez de procurar em pastas
- **Funciona em Todos**: Chrome, Firefox, Edge e outros navegadores
- **Sem Cadastro**: Sem login, sem senha, sem chave de API

### Como Instalar (Passo a Passo)

Escolha seu computador abaixo e siga os passos:

#### Windows

1. **Baixar Python**
   - Va para: https://www.python.org/downloads/
   - Clique no botao: "Download Python 3.12.x"
   - Aguarde o download

2. **Instalar Python**
   - Clique duas vezes no arquivo baixado
   - **IMPORTANTE**: Marque a caixa "Add Python to PATH" (muito importante!)
   - Clique em "Install Now"
   - Aguarde terminar
   - Feche a janela

3. **Instalar groupmrk**
   - Abra o Prompt de Comando (pressione tecla Windows + R, digite "cmd", pressione Enter)
   - Digite: `pip install groupmrk`
   - Pressione Enter e aguarde

4. **Pronto!** Agora voce pode usar!

#### macOS (Apple)

1. **Verificar se tem Python**
   - Abra o Terminal (pressione Cmd + Space, digite "Terminal", pressione Enter)
   - Digite: `python3 --version`
   - Se aparecer "command not found", continue abaixo

2. **Instalar Python**
   - Va para: https://www.python.org/downloads/
   - Clique: "Download Python 3.12.x"
   - Abra o arquivo baixado e siga os passos

3. **Instalar groupmrk**
   - No Terminal, digite: `pip3 install groupmrk`
   - Pressione Enter e aguarde

4. **Pronto!**

#### Linux (Ubuntu e similares)

1. **Abrir Terminal**
   - Pressione Ctrl + Alt + T

2. **Instalar Python** (se nao tiver)
   - Digite: `sudo apt update`
   - Pressione Enter
   - Digite: `sudo apt install python3 python3-pip`
   - Pressione Enter e digite sua senha

3. **Instalar groupmrk**
   - Digite: `pip3 install groupmrk`
   - Pressione Enter

4. **Pronto!**

#### Linux (Fedora)

1. **Abrir Terminal**

2. **Instalar Python**
   - Digite: `sudo dnf install python3 pip`
   - Pressione Enter

3. **Instalar groupmrk**
   - Digite: `pip3 install groupmrk`

4. **Pronto!**

#### Linux (Debian)

1. **Abrir Terminal**

2. **Instalar Python**
   - Digite: `sudo apt update && sudo apt install python3 python3-pip`
   - Pressione Enter

3. **Instalar groupmrk**
   - Digite: `pip3 install groupmrk`

4. **Pronto!**

---

## Como Usar (Exemplos)

### IMPORTANTE: Onde Executar os Comandos

Antes de executar qualquer comando, voce precisa estar na pasta correta!

**Verificar sua pasta atual:**
- **Windows**: No Prompt de Comando, olhe o que vem antes do simbolo `>`
  - Exemplo: `C:\Users\SeuNome\Documentos\favoritos>` - voce esta na pasta "favoritos"
  - Se mostrar `C:\Users\SeuNome>` - voce esta na pasta pessoal

- **macOS/Linux**: No Terminal, olhe o que vem antes de `$`
  - Exemplo: `~/Documents/bookmarks$` - voce esta na pasta "bookmarks"
  - Se mostrar `~` ou `$HOME` - voce esta na pasta pessoal

**Para mudar de pasta:**
- **Windows**: `cd Documentos\favoritos` (use barra invertida `\`)
- **macOS/Linux**: `cd Documents/favoritos` (use barra normal `/`)

### 1. Organizar seus Favoritos

```bash
groupmrk import meus_favoritos.html --output organizados.html --mock
```

 Isto ira:
 - Ler seus favoritos de "meus_favoritos.html"
 - Organizar usando IA (a flag --mock torna rapido para testar)
 - Salvar a versao organizada em "organizados.html"

### 2. Pesquisar seus Favoritos

```bash
groupmrk search "tutoriais python" organizados.html
```

Isso encontrara favoritos sobre tutoriais Python!

### 3. Exportar para Formato do Navegador

```bash
groupmrk export organizados.html favoritos_finais.html
```

### 4. Obter Ajuda

```bash
groupmrk --help
```

---

### Inicio Rapido (5 minutos)

1. Exporte seus favoritos do navegador:
   - **Chrome**: Clique em tres pontos → Favoritos → Gerenciador de favoritos → Exportar
   - **Firefox**: Clique em tres linhas → Favoritos → Mostrar todos → Importar e Exportar → Exportar
   - **Edge**: Clique em tres pontos → Favoritos → Exportar favoritos

2. Salve o arquivo (chame de "favoritos.html")

3. Abra o terminal/prompt de comando

4. Va ate a pasta onde voce salvou favoritos.html
   - Use o comando `cd` para mudar para essa pasta

5. Execute: `groupmrk import favoritos.html --output organizados.html --mock`

6. Abra "organizados.html" no navegador e importe!

---

### Solucao de Problemas

"pip" nao e reconhecido (Windows)
- Certifique-se de ter marcado "Add Python to PATH" durante a instalacao
- Ou tente: `python -m pip install groupmrk`

"command not found" (macOS/Linux)
- Tente usar `pip3` em vez de `pip`

Diz "No LLM client available"
- Verifique se tem conexao com a internet
- Ou use a flag `--mock` para testar

Erro "File not found"
- Verifique se o arquivo de favoritos existe na pasta onde voce esta executando o comando
- Use `cd` para ir ate a pasta correta

---

### Licenca

MIT - Livre para usar, modificar e compartilhar!