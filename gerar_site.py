import os
import time
from google import genai
from google.genai.errors import ServerError

# Pega a chave secreta configurada no GitHub Actions
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada!")

# Inicializa o cliente oficial moderno
client = genai.Client(api_key=api_key)

# Contexto global padronizado da Camaçari Cabos
CONTEXTO_EMPRESA = """
Dados Oficiais da Empresa:
- Nome: Camaçari Cabos Materiais Elétricos
- Fundação: Desde 2014 em Camaçari - BA.
- Endereço: Rua Centro, 249, Camaçari - BA (CEP 42800-029).
- Telefones / WhatsApp: (71) 99666-0988 / (71) 2136-4416.
- Atuação: Fornecimento de cabos elétricos (atacado e varejo), plugs e tomadas industriais, disjuntores, refletores, luminárias, fitas de LED, Padrões Coelha, eletrocalhas, perfilados, eletrodutos e suprimentos industriais para Camaçari, Salvador, Lauro de Freitas, Simões Filho, Dias d'Ávila e Mata de São João.

DIRETRIZ CRÍTICA DE ESTRUTURA E DESIGN:
- Crie páginas HTML completas, separadas e independentes (NÃO faça página única / one-page).
- Todas as páginas DEVEM possuir o mesmo cabeçalho (com links reais para index.html, produtos.html, blog.html, sobre.html e a logomarca '<img src="logo.png" alt="Camaçari Cabos" class="h-10 object-contain">') e o mesmo rodapé corporativo.
- Paleta de cores em Tailwind CSS: tons de azul profundo, branco e detalhes em âmbar.
- DIRETRIZ DE ESCRITA: NUNCA use sintaxe LaTeX ($...$). Use texto limpo (ex: Queda de Tensão <= 4%).
"""

def limpar_html(texto):
    if "```html" in texto:
        texto = texto.split("```html")[1].split("```")[0]
    elif "```" in texto:
        texto = texto.split("```")[1].split("```")[0]
    return texto.strip()

def gerar_pagina_com_tentativas(nome_arquivo, prompt_especifico, max_tentativas=5):
    print(f"🤖 Gerando página independente: {nome_arquivo}...")
    tentativa = 0
    
    while tentativa < max_tentativas:
        try:
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=f"{CONTEXTO_EMPRESA}\n\n{prompt_especifico}"
            )
            html_limpo = limpar_html(response.text)
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write(html_limpo)
            print(f"✅ {nome_arquivo} gerado com sucesso!")
            return
            
        except ServerError as e:
            tentativa += 1
            print(f"⚠️ Servidor ocupado. Tentativa {tentativa} de {max_tentativas} para {nome_arquivo}. Aguardando 10 segundos...")
            if tentativa >= max_tentativas:
                raise e
            time.sleep(10)

if __name__ == "__main__":
    # 1. Página Inicial
    gerar_pagina_com_tentativas("index.html", 
        "Crie a página inicial (index.html) completa utilizando Tailwind CSS. Deve conter um menu de navegação superior com links para index.html, produtos.html, blog.html e sobre.html, a logomarca 'logo.png', um banner principal forte voltado para o Polo Industrial de Camaçari, seções de destaque e rodapé completo.")
    
    # 2. Página de Produtos e Catálogo
    gerar_pagina_com_tentativas("produtos.html", 
        "Crie a página de catálogo e produtos (produtos.html) utilizando exatamente o mesmo layout e menu de navegação padrão das outras páginas. Deve detalhar cabos elétricos, disjuntores, infraestrutura e Padrão Coelba em formato de grade organizada.")
    
    # 3. Página do Blog Técnico
    gerar_pagina_com_tentativas("blog.html", 
        "Crie a página do blog técnico (blog.html) mantendo rigorosamente a mesma identidade visual e menu de navegação padrão. Inclua artigos detalhados sobre dimensionamento de cabos, ampacidade e normas ABNT para indústrias.")

    # 4. Página Sobre
    gerar_pagina_com_tentativas("sobre.html", 
        "Crie a página institucional Sobre a Empresa (sobre.html) mantendo o mesmo padrão visual, logomarca e menu. Conte a trajetória da Camaçari Cabos desde 2014, valores e compromisso com o Polo Industrial.")
