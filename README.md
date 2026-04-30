# groupmrk

Um programa de organização de favoritos do navegador com IA. Organize, pesquise e categorize seus favoritos usando inteligência artificial.

---

## Sumário

- [Descrição do projeto](#descrição-do-projeto)
- [Como instalar](#como-instalar-passo-a-passo)
- [Como usar](#como-usar-passo-a-passo)
- [Início rápido](#início-rápido-5-minutos)
- [Solução de problemas](#solução-de-problemas)
- [Licença](#licença)

## Summary

- [What is this](#what-is-this)
- [How to install](#how-to-install-step-by-step)
- [How to use](#how-to-use-step-by-step)
- [Quick start](#quick-start-5-minutes)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## English

### What is this?

**groupmrk** helps you organize your browser bookmarks (also called "favorites") automatically using artificial intelligence.

#### The problem
After years of saving bookmarks, most people have hundreds (or thousands!) of links scattered in messy folders. When you need something specific, it's faster to Google it again than to find what you already saved. Your bookmarks become useless.

#### The solution
You give groupmrk your saved bookmarks, and it organizes them for you automatically.

#### How it works
1. Export your bookmarks from your browser (Chrome, Firefox, Edge, etc.)
2. Run groupmrk to analyze and organize them
3. Import the organized version back to your browser

The AI reads each bookmark title and URL, understands what it's about, and groups related links together - like "Python Tutorials", "Recipes", "Work Projects", "News Sites".

No programming knowledge needed!

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

## Português

### Descrição do projeto

**groupmrk** ajuda você a organizar seus favoritos do navegador (também chamados de "marcadores") automaticamente usando inteligência artificial.

#### O problema
Depois de anos salvando favoritos, a maioria das pessoas tem centenas (ou milhares!) de links espalhados em pastas bagunçadas. Quando você precisa de algo específico, é mais rápido pesquisar no Google do que encontrar o que já tinha guardado. Seus favoritos se tornam inúteis.

#### A solução
Você entrega seus favoritos salvos para o groupmrk, e ele organiza tudo automaticamente para você.

#### Como funciona
1. Exporte seus favoritos do seu navegador (Chrome, Firefox, Edge, etc.)
2. Execute o groupmrk para analisar e organizar
3. Importe a versão organizada de volta ao navegador

A inteligência artificial lê o título e URL de cada favorito, entende do que se trata, e agrupa links relacionados juntos - como "Tutoriais Python", "Receitas", "Projetos do Trabalho", "Sites de Notícias".

Não precisa saber programação!

### O que ele faz?

- **Organização Automática**: Coloque os favoritos, receba organizados
- **Pesquisa Natural**: Encontre favoritos digitando "tutoriais python" em vez de procurar em pastas
- **Funciona em Todos**: Chrome, Firefox, Edge e outros navegadores
- **Sem Cadastro**: Sem login, sem senha, sem chave de API

### Como Instalar (Passo a Passo)

Escolha seu computador abaixo e siga os passos:

#### Windows

1. **Baixar Python**
   - Vá para: https://www.python.org/downloads/
   - Clique no botão: "Download Python 3.12.x"
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

4. **Pronto!** Agora você pode usar!

#### macOS (Apple)

1. **Verificar se tem Python**
   - Abra o Terminal (pressione Cmd + Space, digite "Terminal", pressione Enter)
   - Digite: `python3 --version`
   - Se aparecer "command not found", continue abaixo

2. **Instalar Python**
   - Vá para: https://www.python.org/downloads/
   - Clique: "Download Python 3.12.x"
   - Abra o arquivo baixado e siga os passos

3. **Instalar groupmrk**
   - No Terminal, digite: `pip3 install groupmrk`
   - Pressione Enter e aguarde

4. **Pronto!**

#### Linux (Ubuntu e similares)

1. **Abrir Terminal**
   - Pressione Ctrl + Alt + T

2. **Instalar Python** (se não tiver)
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
2. Encontre a opção "Exportar Favoritos":
   - **Chrome**: Menu → Favoritos → Gerenciador de favoritos → Exportar
   - **Firefox**: Menu → Favoritos → Mostrar todos → Importar e Exportar → Exportar
   - **Edge**: Menu → Favoritos → Exportar favoritos
3. Salve o arquivo como "bookmarks.html"

### Passo 2: Colar o Arquivo Aqui

Copie o arquivo "bookmarks.html" e cole na mesma pasta onde este arquivo README está (a pasta raiz do projeto).

### Passo 3: Executar o Programa

Agora você está pronto para organizar!

### 1. Organizar seus Favoritos

```bash
groupmrk import meus_favoritos.html --output organizados.html --mock
```

 Isto irá:
 - Ler seus favoritos de "meus_favoritos.html"
 - Organizar usando IA (a flag --mock torna rápido para testar)
 - Salvar a versão organizada em "organizados.html"

### 2. Pesquisar seus Favoritos

```bash
groupmrk search "tutoriais python" organizados.html
```

Isso encontrará favoritos sobre tutoriais Python!

### 3. Exportar para Formato do Navegador

```bash
groupmrk export organizados.html favoritos_finais.html
```

### 4. Obter Ajuda

```bash
groupmrk --help
```

---

### Início Rápido (5 minutos)

#### Passo 1: Exportar Seus Favoritos
1. Abra seu navegador (Chrome, Firefox, Edge)
2. Encontre a opção de exportar:
   - **Chrome**: Menu (três pontos) → Favoritos → Gerenciador de favoritos → Exportar
   - **Firefox**: Menu (três linhas) → Favoritos → Mostrar todos → Importar e Exportar → Exportar
   - **Edge**: Menu (três pontos) → Favoritos → Exportar favoritos
3. Ao salvar, nomeie o arquivo como: **bookmarks.html**
4. Salve na pasta Área de Trabalho ou Downloads (por enquanto)

#### Passo 2: Copiar para a Pasta do Projeto
1. Vá até sua Área de Trabalho ou Downloads
2. Encontre o arquivo "bookmarks.html" que você acabou de criar
3. Copie (clique com botão direito → Copiar, ou pressione Ctrl+C)
4. Vá até a pasta onde você extraiu este projeto (onde está este README)
5. Cole o arquivo ali (clique com botão direito → Colar, ou pressione Ctrl+V)

#### Passo 3: Abrir o Terminal
1. **Windows**: Pressione a tecla Windows + R, digite "cmd", pressione Enter
   - Uma janela preta aparecerá (Prompt de Comando)
2. **macOS**: Pressione Cmd + Space, digite "Terminal", pressione Enter
   - Uma janela branca/cinza aparecerá
3. **Linux**: Pressione Ctrl + Alt + T
   - Uma janela de terminal aparecerá

#### Passo 4: Navegar até a Pasta
No terminal, você precisa ir até a pasta onde você colou bookmarks.html.

**Se você extraiu o projeto na Área de Trabalho (Windows):**
```
cd Desktop\groupmrk
```
(Pressione Enter depois de digitar)

**Se você extraiu o projeto na Área de Trabalho (macOS/Linux):**
```
cd Desktop/groupmrk
```
(Pressione Enter depois de digitar)

**Dica**: Depois de pressionar Enter, você deve ver o nome da pasta no começo da linha, como:
- Windows: `C:\Users\SeuNome\Desktop\groupmrk>`
- macOS: `~/Desktop/groupmrk$`

#### Passo 5: Executar o Programa
Agora digite este comando e pressione Enter:
```
groupmrk import bookmarks.html --output organized.html --mock
```

Aguarde alguns segundos... quando terminar, você verá "organized.html" na sua pasta!

#### Passo 6: Importar de Volta no Navegador
1. Abra seu navegador
2. Encontre a opção de importar (mesma que exportar, mas escolha "Importar")
3. Selecione "organized.html" e importe!

Pronto! Seus favoritos estão organizados!

---

### Solução de Problemas

"pip" não é reconhecido (Windows)
- Certifique-se de ter marcado "Add Python to PATH" durante a instalação
- Ou tente: `python -m pip install groupmrk`

"command not found" (macOS/Linux)
- Tente usar `pip3` em vez de `pip`

Diz "No LLM client available"
- Verifique se tem conexão com a internet
- Ou use a flag `--mock` para testar

Erro "File not found"
- Verifique se o arquivo de favoritos existe na pasta onde você está executando o comando
- Use `cd` para ir até a pasta correta

---

### Licença

MIT - Livre para usar, modificar e compartilhar!

---

## Contribua também! / Contribute too!

Even if you are a beginner, you can help improve this project!

Este projeto foi criado com duas ferramentas especiais que tornam a contribuição fácil:

### Speckit
https://https://github.com/github/spec-kit

Speckit é uma ferramenta que ajuda a planejar e organizar o desenvolvimento de projetos. Ela te guia passo a passo, desde a ideia até a implementação, sem precisar ser um expert.

### OpenCode
https://opencode.ai

OpenCode é uma ferramenta de IA que ajuda você a escrever código, corrigir erros e entender como as coisas funcionam. Você conversando em português ou inglês, ele te ajuda a fazer mudanças no projeto.

### Como contribuir:
1. Acesse o projeto no GitHub: https://github.com/vrsoares/groupmrk
2. Clique em "Fork" para copiar o projeto
3. Use o OpenCode para fazer suas mudanças
4. Use o Speckit para planejar o que quer adicionar
5. Envie suas mudanças com "Pull Request"

Você não precisa saber programar perfeitamente — as ferramentas te ajudam a aprender fazendo!
You don't need to know how to code perfectly — the tools help you learn by doing!

---

即使您是初學者，也可以幫助改進這個項目！