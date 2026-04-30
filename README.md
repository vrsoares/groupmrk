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

## How to Use (Step by Step)

### Step 1: Export Your Bookmarks from Browser

1. Open your browser (Chrome, Firefox, Edge, etc.)
2. Find the "Export Bookmarks" option:
   - **Chrome**: Menu → Bookmarks → Bookmark manager → Export
   - **Firefox**: Menu → Bookmarks → Show all bookmarks → Import and Backup → Export
   - **Edge**: Menu → Favorites → Export favorites
3. Save the file as "bookmarks.html"

### Step 2: Put the File Here

Copy the "bookmarks.html" file and paste it in the same folder where this README file is (the project root).

### Step 3: Run the Program

Now you're ready to organize!

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

#### Step 1: Export Your Bookmarks
1. Open your browser (Chrome, Firefox, Edge)
2. Find the export option:
   - **Chrome**: Menu (three dots) → Bookmarks → Bookmark manager → Export
   - **Firefox**: Menu (three lines) → Bookmarks → Show all bookmarks → Import and Backup → Export
   - **Edge**: Menu (three dots) → Favorites → Export favorites
3. When saving, name the file: **bookmarks.html**
4. Save it in your Desktop or Downloads folder (for now)

#### Step 2: Copy to Project Folder
1. Go to your Desktop or Downloads folder
2. Find the "bookmarks.html" file you just created
3. Copy it (right-click → Copy, or press Ctrl+C)
4. Go to the folder where you extracted this project (where this README is)
5. Paste the file there (right-click → Paste, or press Ctrl+V)

#### Step 3: Open Terminal
1. **Windows**: Press the Windows key + R, type "cmd", press Enter
   - A black window will appear (Command Prompt)
2. **macOS**: Press Cmd + Space, type "Terminal", press Enter
   - A white/gray window will appear
3. **Linux**: Press Ctrl + Alt + T
   - A terminal window will appear

#### Step 4: Navigate to the Folder
In your terminal, you need to go to the folder where you pasted bookmarks.html.

**If you extracted the project to Desktop (Windows):**
```
cd Desktop\groupmrk
```
(Press Enter after typing)

**If you extracted the project to Desktop (macOS/Linux):**
```
cd Desktop/groupmrk
```
(Press Enter after typing)

**Tip**: After pressing Enter, you should see the folder name at the beginning of the line, like:
- Windows: `C:\Users\YourName\Desktop\groupmrk>`
- macOS: `~/Desktop/groupmrk$`

#### Step 5: Run the Program
Now type this command and press Enter:
```
groupmrk import bookmarks.html --output organized.html --mock
```

Wait a few seconds... when it finishes, you will see "organized.html" in your folder!

#### Step 6: Import Back to Browser
1. Open your browser
2. Find the import option (same as export, but choose "Import")
3. Select "organized.html" and import!

Done! Your bookmarks are now organized!

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

## Como Usar (Passo a Passo)

### Passo 1: Exportar Seus Favoritos do Navegador

1. Abra seu navegador (Chrome, Firefox, Edge, etc.)
2. Encontre a opcao "Exportar Favoritos":
   - **Chrome**: Menu → Favoritos → Gerenciador de favoritos → Exportar
   - **Firefox**: Menu → Favoritos → Mostrar todos → Importar e Exportar → Exportar
   - **Edge**: Menu → Favoritos → Exportar favoritos
3. Salve o arquivo como "bookmarks.html"

### Passo 2: Colar o Arquivo Aqui

Copie o arquivo "bookmarks.html" e cole na mesma pasta onde este arquivo README esta (a pasta raiz do projeto).

### Passo 3: Executar o Programa

Agora voce esta pronto para organizar!

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

#### Passo 1: Exportar Seus Favoritos
1. Abra seu navegador (Chrome, Firefox, Edge)
2. Encontre a opcao de exportar:
   - **Chrome**: Menu (tres pontos) → Favoritos → Gerenciador de favoritos → Exportar
   - **Firefox**: Menu (tres linhas) → Favoritos → Mostrar todos → Importar e Exportar → Exportar
   - **Edge**: Menu (tres pontos) → Favoritos → Exportar favoritos
3. Ao salvar, nomeie o arquivo como: **bookmarks.html**
4. Salve na pasta Area de Trabalho ou Downloads (por enquanto)

#### Passo 2: Copiar para a Pasta do Projeto
1. Va ate sua Area de Trabalho ou Downloads
2. Encontre o arquivo "bookmarks.html" que voce acabou de criar
3. Copie (clique com botao direito → Copiar, ou pressione Ctrl+C)
4. Va ate a pasta onde voce extraiu este projeto (onde esta este README)
5. Cole o arquivo ali (clique com botao direito → Colar, ou pressione Ctrl+V)

#### Passo 3: Abrir o Terminal
1. **Windows**: Pressione a tecla Windows + R, digite "cmd", pressione Enter
   - Uma janela preta aparecera (Prompt de Comando)
2. **macOS**: Pressione Cmd + Space, digite "Terminal", pressione Enter
   - Uma janela branca/cinza aparecera
3. **Linux**: Pressione Ctrl + Alt + T
   - Uma janela de terminal aparecera

#### Passo 4: Navegar ate a Pasta
No terminal, voce precisa ir ate a pasta onde voce colou bookmarks.html.

**Se voce extraiu o projeto na Area de Trabalho (Windows):**
```
cd Desktop\groupmrk
```
(Pressione Enter depois de digitar)

**Se voce extraiu o projeto na Area de Trabalho (macOS/Linux):**
```
cd Desktop/groupmrk
```
(Pressione Enter depois de digitar)

**Dica**: Depois de pressionar Enter, voce deve ver o nome da pasta no comeco da linha, como:
- Windows: `C:\Users\SeuNome\Desktop\groupmrk>`
- macOS: `~/Desktop/groupmrk$`

#### Passo 5: Executar o Programa
Agora digite este comando e pressione Enter:
```
groupmrk import bookmarks.html --output organized.html --mock
```

Aguarde alguns segundos... quando terminar, voce verah "organized.html" na sua pasta!

#### Passo 6: Importar de Volta no Navegador
1. Abra seu navegador
2. Encontre a opcao de importar (mesma que exportar, mas escolha "Importar")
3. Selecione "organized.html" e importe!

Pronto! Seus favoritos estao organizados!

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