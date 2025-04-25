# MARC-Gen API Tool

Aplicação web simples que recebe texto de uma ficha catalográfica (simulando OCR) e utiliza a API de um Grande Modelo de Linguagem (LLM), como o Google Gemini, para gerar o registro MARC21 correspondente. O foco principal é aprender a integrar APIs de LLMs e praticar engenharia de prompt para tarefas biblioteconômicas.

## Funcionalidades

*   Campo de texto para inserir/colar o conteúdo da ficha catalográfica.
*   Botão "Gerar MARC" para enviar o texto à API do LLM.
*   Área para exibir o resultado MARC21 retornado pela API.

## Tecnologias Utilizadas

*   **Linguagem:** Python 3
*   **Framework Web:** Flask
*   **LLM API:** Google Gemini (via `google-generativeai`)
*   **Interface:** HTML, CSS básico
*   **Gerenciamento de Dependências:** Pip, `requirements.txt`
*   **Ambiente Virtual:** `venv`
*   **Controle de Versão:** Git, GitHub

## Configuração e Instalação Local

1.  **Clonar o Repositório:**
    ```bash
    git clone https://github.com/spiderbl/marc-gen-api-tool.git
    cd marc-gen-api-tool
    ```
2.  **Criar e Ativar Ambiente Virtual:**
    ```bash
    # Criar o ambiente (ex: venv)
    python -m venv venv
    # Ativar no Windows (cmd)
    .\venv\Scripts\activate.bat
    # Ativar no Windows (PowerShell) - Pode requerer ajuste de política de execução
    # .\venv\Scripts\Activate.ps1
    # Ativar no macOS/Linux
    # source venv/bin/activate
    ```
3.  **Instalar Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configurar Chave da API:**
    *   Obtenha sua chave de API no [Google AI Studio](https://aistudio.google.com/).
    *   Crie um arquivo chamado `.env` na raiz do projeto.
    *   Adicione a seguinte linha ao `.env`, substituindo `SUA_API_KEY_AQUI` pela sua chave:
        ```dotenv
        GEMINI_API_KEY=SUA_API_KEY_AQUI
        ```
    *   **Importante:** O arquivo `.env` está listado no `.gitignore` e não deve ser enviado ao repositório. Se você acidentalmente o enviou, remova-o do histórico do Git e gere uma nova chave de API.

## Como Executar

1.  Certifique-se de que seu ambiente virtual esteja ativado (você verá `(venv)` no início do prompt).
2.  Execute a aplicação Flask:
    ```bash
    python app.py
    ```
3.  Abra seu navegador e acesse: `http://127.0.0.1:5000`
4.  Cole o texto de uma ficha catalográfica na área de texto e clique em "Gerar MARC".

## Engenharia de Prompt

A qualidade da conversão para MARC21 depende fortemente do prompt enviado à API do LLM. O prompt base está definido na variável `BASE_PROMPT` dentro de `app.py`. Experimente modificá-lo para:

*   Ser mais específico sobre o formato de saída desejado.
*   Fornecer exemplos (few-shot learning).
*   Instruir sobre como lidar com informações ausentes ou ambíguas.

## Notas sobre Deploy (Produção)

*   O servidor de desenvolvimento do Flask (`app.run()`) **não** é adequado para produção.
*   Utilize um servidor WSGI como **Gunicorn** (Linux/macOS) ou **Waitress** (Multiplataforma).
*   Adicione o servidor WSGI escolhido ao `requirements.txt`.
*   Em plataformas de hospedagem (como Render, PythonAnywhere, Heroku):
    *   Configure o comando de start para usar o servidor WSGI (ex: `gunicorn app:app`).
    *   Configure a chave `GEMINI_API_KEY` como uma **variável de ambiente** na plataforma, **não** usando o arquivo `.env`.

## Considerações

*   **Dependência da API:** Requer conexão com a internet e depende da disponibilidade e políticas do provedor da API (Google).
*   **Custos:** O uso da API pode incorrer em custos após exceder os limites da camada gratuita.
*   **Privacidade:** Os dados da ficha catalográfica são enviados para os servidores do Google.
*   **Precisão:** A saída do LLM pode não ser 100% precisa e pode requerer revisão.