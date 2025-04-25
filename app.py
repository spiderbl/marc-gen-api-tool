# app.py
import os
import google.generativeai as genai
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
# É necessário configurar uma chave secreta para usar flash messages no Flask
app.secret_key = os.urandom(24) # Gera uma chave secreta aleatória

# Configurar a API do Google Gemini
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # Se a chave não estiver no .env, tente variáveis de ambiente do sistema
    # (útil para deploy)
    api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Erro: Chave da API do Gemini não encontrada.")
    print("Certifique-se de criar um arquivo .env com GEMINI_API_KEY=SUA_CHAVE")
    print("Ou defina a variável de ambiente GEMINI_API_KEY.")
    # Em uma aplicação real, você poderia desabilitar a funcionalidade
    # ou mostrar um erro mais robusto na interface.
    # Por simplicidade, apenas imprimimos no console e continuamos.
    # A chamada da API falhará se a chave não for válida.
else:
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"Erro ao configurar a API do Gemini: {e}")
        # Tratar o erro conforme necessário

# Modelo Generativo (ex: 'gemini-pro' ou o mais recente disponível)
# Verifique os modelos disponíveis no Google AI Studio ou documentação
model = genai.GenerativeModel('gemini-1.5-flash-latest') # Usando um modelo mais recente e eficiente

# ----- Engenharia de Prompt -----
# Este é o ponto central para obter bons resultados.
# Experimente diferentes abordagens.
BASE_PROMPT = """
Você é um assistente especialista em catalogação bibliográfica no formato MARC21.
Sua tarefa é converter o texto de uma ficha catalográfica fornecido pelo usuário para um registro MARC21 completo e preciso.

Instruções:
1. Analise cuidadosamente o texto da ficha catalográfica.
2. Identifique os campos relevantes (título, autor, imprenta, descrição física, notas, assuntos, etc.).
3. Mapeie cada informação para a tag, indicadores e subcampos MARC21 apropriados.
4. Formate a saída **estritamente** como um registro MARC21 legível, mostrando cada campo em uma nova linha, com a tag, indicadores (use # se não aplicável) e subcampos (ex: $a, $b, $c).
5. Se alguma informação essencial parecer faltar na ficha, use placeholders razoáveis (como "[Informação não fornecida]") ou omita o subcampo/campo se apropriado, mas tente gerar o registro mais completo possível com os dados disponíveis.
6. Preste atenção especial a detalhes como pontuação, capitalização e ordem dos subcampos conforme as regras do MARC21.
7. Inclua o campo Líder (LDR) e o campo de controle 008 com valores plausíveis baseados no conteúdo (mesmo que simplificados).

Texto da Ficha Catalográfica a ser convertida:
---
{ficha_texto}
---

Registro MARC21 Gerado:
"""
# ----- Fim da Engenharia de Prompt -----

@app.route('/', methods=['GET'])
def index():
    """Renderiza a página inicial com o formulário."""
    return render_template('index.html', ficha_texto="", marc_result="")

@app.route('/generate', methods=['POST'])
def generate_marc():
    """Recebe o texto da ficha, chama a API e exibe o resultado."""
    ficha_texto = request.form.get('ficha_texto', '').strip()
    marc_result = ""
    error_message = None

    if not api_key:
        error_message = "Erro de configuração: Chave da API não definida no servidor."
        flash(error_message, 'error')
        return render_template('index.html', ficha_texto=ficha_texto, marc_result="")

    if not ficha_texto:
        error_message = "Por favor, insira o texto da ficha catalográfica."
        flash(error_message, 'warning')
        return render_template('index.html', ficha_texto=ficha_texto, marc_result="")

    try:
        # Cria o prompt final combinando a base com o texto do usuário
        prompt_completo = BASE_PROMPT.format(ficha_texto=ficha_texto)

        # Chama a API do Gemini
        response = model.generate_content(prompt_completo)

        # Extrai o texto da resposta
        # Adiciona verificação para caso a resposta não contenha 'text'
        if hasattr(response, 'text'):
             marc_result = response.text
        elif hasattr(response, 'parts') and response.parts:
             # Tenta extrair de 'parts' se 'text' não estiver disponível
             marc_result = "".join(part.text for part in response.parts if hasattr(part, 'text'))
        else:
             # Se ainda assim não encontrar, tenta acessar o candidato (estrutura pode variar)
             try:
                 marc_result = response.candidates[0].content.parts[0].text
             except (AttributeError, IndexError, KeyError):
                 marc_result = "Erro ao extrair texto da resposta da API."
                 error_message = "A API retornou uma resposta em formato inesperado."
                 print("Resposta completa da API:", response) # Log para depuração


        # Verifica se o conteúdo foi bloqueado (pode acontecer por filtros de segurança)
        if not marc_result and hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
             error_message = f"A geração foi bloqueada pela API. Razão: {response.prompt_feedback.block_reason}"
             marc_result = f"Erro: {error_message}"


    except AttributeError:
         # Captura o erro se 'genai' não foi configurado corretamente (sem API key)
         error_message = "Erro: A API do Gemini não foi configurada corretamente (provavelmente falta a chave API)."
         print(error_message) # Log no servidor
    except Exception as e:
        # Captura outros erros da API ou do processamento
        error_message = f"Ocorreu um erro ao gerar o MARC21: {e}"
        print(f"Erro na chamada da API: {e}") # Log detalhado no servidor
        print("Prompt enviado:", prompt_completo) # Log para depuração
        # Em produção, evite expor detalhes do erro diretamente ao usuário se sensível

    if error_message:
         flash(error_message, 'error') # Mostra a mensagem de erro para o usuário

    # Renderiza a mesma página, mas agora com os resultados (ou erro)
    return render_template('index.html', ficha_texto=ficha_texto, marc_result=marc_result)

if __name__ == '__main__':
    # Executa o servidor Flask em modo de depuração (útil para desenvolvimento)
    # Para produção, use um servidor WSGI como Gunicorn ou Waitress
    app.run(debug=True)