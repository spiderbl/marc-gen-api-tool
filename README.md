# MARC-Gen API Tool

Aplicação web simples que converte texto de fichas catalográficas para o formato MARC21 usando uma API de LLM (exemplo com Google Gemini). O foco principal é demonstrar a integração da API e a engenharia de prompt.

## Funcionalidades

*   Campo de texto para colar o conteúdo da ficha.
*   Botão "Gerar MARC" para iniciar a conversão via API.
*   Área para exibir o resultado MARC21 retornado pela API.

## Tecnologias

*   **LLM:** Google Gemini API (`google-generativeai`)
*   **Linguagem:** Python 3
*   **Framework Web:** Flask
*   **Interface:** HTML/CSS simples

## Setup

1.  **Clone o repositório (ou crie os arquivos):**
    ```bash
    git clone <url-do-repositorio> # Se estiver usando git
    cd marc-gen-api-tool
    ```

2.  **Obtenha uma chave da API do Google Gemini:**
    *   Vá para o [Google AI Studio](https://aistudio.google.com/).
    *   Crie ou use um projeto existente para gerar uma chave de API.
    *   Copie a chave.

3.  **Configure a chave da API:**
    *   Crie um arquivo chamado `.env` na raiz do projeto.
    *   Adicione a seguinte linha ao arquivo `.env`, substituindo `SUA_API_KEY_AQUI` pela sua chave:
      ```dotenv
      GEMINI_API_KEY=SUA_API_KEY_AQUI
      ```
    *   **NUNCA** adicione o arquivo `.env` ao controle de versão (Git). Se estiver usando Git, adicione `.env` ao seu arquivo `.gitignore`.

4.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    ```
    *   Ative o ambiente:
        *   Windows: `.\venv\Scripts\activate`
        *   macOS/Linux: `source venv/bin/activate`

5.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Execução

1.  Certifique-se de que seu ambiente virtual esteja ativado.
2.  Execute a aplicação Flask:
    ```bash
    python app.py
    ```
3.  Abra seu navegador e acesse: `http://127.0.0.1:5000` (ou o endereço que o Flask indicar).

## Engenharia de Prompt

O coração da conversão está no prompt definido na variável `BASE_PROMPT` dentro de `app.py`. Modificar este prompt é a chave para melhorar a qualidade da saída MARC21.

**Dicas para melhorar o prompt:**

*   **Seja mais específico:** Detalhe exatamente como você quer o formato de saída (espaçamento, indicadores, pontuação ISBD dentro dos campos).
*   **Forneça exemplos (Few-Shot Learning):** Inclua um ou dois exemplos de uma ficha e seu MARC21 correspondente *dentro* do prompt para guiar o modelo.
*   **Instrua sobre casos ambíguos:** Diga ao modelo o que fazer se informações estiverem faltando ou forem dúbias.
*   **Refine as tags:** Peça explicitamente por tags específicas (LDR, 008, 020, 100, 245, 260/264, 300, 5XX, 6XX, etc.).
*   **Itere:** Teste diferentes prompts com a mesma ficha de entrada para ver qual gera o melhor resultado.

## Limitações e Considerações

*   **Dependência da API:** Requer conexão com a internet e depende da disponibilidade e políticas do provedor da API (Google).
*   **Custos:** O uso da API pode incorrer em custos após exceder os limites da camada gratuita. Monitore seu uso.
*   **Privacidade:** Os dados da ficha catalográfica são enviados para os servidores do Google para processamento. Considere as implicações de privacidade para dados sensíveis.
*   **Precisão do LLM:** A qualidade da conversão depende da capacidade do modelo LLM e da eficácia do prompt. A saída pode não ser 100% precisa ou pode exigir revisão por um catalogador humano.
*   **Simplicidade:** Esta é uma ferramenta de protótipo, sem tratamento robusto de erros, validação complexa de entrada ou recursos avançados.

## Próximos Passos Possíveis

*   Melhorar a interface do usuário (UI/UX).
*   Adicionar validação de entrada mais robusta.
*   Implementar tratamento de erros mais detalhado e feedback ao usuário.
*   Permitir a escolha do modelo LLM (Gemini, GPT, Claude) via configuração.
*   Adicionar opção para editar o resultado MARC gerado.
*   Integrar com um validador MARC21.
*   Salvar histórico de conversões.