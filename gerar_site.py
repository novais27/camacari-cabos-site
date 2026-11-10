import os
import google.generativeai as genai

# Pega a chave secreta configurada no GitHub Actions
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada!")

genai.configure(api_key=api_key)

# Contexto global padronizado da Camaçari Cabos
CONTEXTO_EMPRESA = """
Dados Oficiais da Empresa:
- Nome: Camaçari Cabos Materiais Elétricos
- Fundação: Desde 2014 em Camaçari - BA.
- Endereço: Rua Centro, 249, Camaçari - BA (CEP 42800-029).
- Telefones / WhatsApp: (71) 99666-0988 / (71) 2136-4416.
- Atuação: Fornecimento de cabos elétricos (atacado e varejo), plugs e tomadas industriais, disjuntores, refletores, luminárias, fitas de LED, Padrões Coelha, eletrocalhas, perfilados, eletrodutos e suprimentos industriais para Camaçari, Salvador, Lauro de Freitas, Simões Filho, Dias d'Ávila e Mata de São João.

DIRETRIZ DE DESIGN:
- Siga rigorosamente um layout profissional corporativo em Tailwind CSS (tons de azul profundo, branco e detalhes em âmbar).
- A logomarca oficial '<img src="logo.png" alt="Camaçari Cabos" class="h-10 object-contain">' deve estar no canto superior esquerdo de todas as páginas.
- DIRETRIZ DE ESCRITA: NUNCA use sintaxe LaTeX ($...$). Use texto limpo (ex: Queda de Tensão <= 4%).
"""

def limpar_html(texto):
    if "```html" in texto:
        texto = texto.split("```html")[1].split("```")[0]
    elif "```" in texto:
        texto = texto.split("```")[1].split("```")[0]
    return texto.strip()

def gerar_pagina(nome_arquivo, prompt_especifico):
    print(f"🤖 Gerando {nome_arquivo}...")
    # Usando o modelo estável
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"{CONTEXTO_EMPRESA}\n\n{prompt_especifico}")
    html_limpo = limpar_html(response.text)
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(html_limpo)
    print(f"✅ {nome_arquivo} gerado com sucesso!")

if __name__ == "__main__":
    gerar_pagina("index.html", "Crie a página inicial (index.html) completa utilizando Tailwind CSS, destacando o banner principal, o Polo Industrial e links de navegação.")
    gerar_pagina("produtos.html", "Crie a página de catálogo de produtos (produtos.html) com listagem detalhada de cabos industriais, disjuntores e Padrão Coelba.")
    gerar_pagina("blog.html", "Crie a página do blog técnico (blog.html) com artigos focados em normas ABNT e engenharia elétrica para indústrias.")
