import os
import google.generativeai as genai

# Pega a chave secreta configurada no GitHub Actions
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada!")

genai.configure(api_key=api_key)

def gerar_conteudo_com_ia():
    model = genai.GenerativeModel('gemini-3.8-flash')
    
    # Contexto oficial e regras rígidas de padronização visual inspiradas na página Sobre
    contexto_global = """
    Dados Oficiais da Empresa:
    - Nome: Camaçari Cabos Materiais Elétricos
    - Fundação: Desde 2014 em Camaçari - BA.
    - Endereço: Rua Centro, 249, Camaçari - BA (CEP 42800-029).
    - Telefones de Contato / WhatsApp: (71) 99666-0988 / (71) 2136-4416.
    - Atuação: Fornecimento de cabos elétricos (atacado e varejo), plugs e tomadas industriais, disjuntores, refletores, luminárias, fitas de LED, Padrões Coelha, eletrocalhas, perfilados, eletrodutos e suprimentos industriais para Camaçari, Salvador, Lauro de Freitas, Simões Filho, Dias d'Ávila e Mata de São João.
    
    DIRETRIZ CRÍTICA DE DESIGN E PADRONIZAÇÃO (PADRÃO PÁGINA SOBRE):
    - Todas as páginas geradas (index.html, produtos.html, blog.html e sobre.html) DEVEM seguir obrigatoriamente exatamente o mesmo layout, paleta de cores corporativa (tons de azul profundo, branco e detalhes em âmbar/dourado), tipografia limpa (Tailwind CSS) e estrutura de cabeçalho e rodapé da página "Sobre a Empresa".
    - A logomarca oficial '<img src="logo.png" alt="Camaçari Cabos" class="h-10 object-contain">' DEVE estar fixada no canto superior esquerdo de todas as páginas.
    - O rodapé deve conter os telefones, endereço e dados reais da empresa.
    - DIRETRIZ DE ESCRITA: NUNCA use sintaxe LaTeX ($...$) ou fórmulas matemáticas complexas. Escreva variáveis e termos técnicos em texto limpo e legível (ex: Queda de Tensão <= 4%, Temperatura de 40°C).
    """

    # 1. Geração da Página Inicial (index.html)
    print("🤖 Agente gerando a página Inicial (index.html)...")
    prompt_index = f"""
    {contexto_global}
    Crie a página inicial (index.html) completa, moderna e padronizada utilizando Tailwind CSS.
    Inclua o banner principal, os diferenciais para o Polo Industrial de Camaçari, atalhos para o catálogo e artigos recentes, com a logomarca 'logo.png' no topo.
    Retorne apenas o código HTML puro.
    """
    resp_index = model.generate_content(prompt_index)
    html_index = limpar_html(resp_index.text)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_index)
    print("✅ index.html gerado e padronizado!")

    # 2. Geração da Página de Produtos (produtos.html)
    print("🤖 Agente gerando a página de Produtos (produtos.html)...")
    prompt_produtos = f"""
    {contexto_global}
    Crie a página de produtos e catálogo técnico (produtos.html) utilizando exatamente o mesmo layout corporativo padrão da página Sobre.
    Destaque cabos industriais, disjuntores, Padrão Coelba e infraestrutura.
    Retorne apenas o código HTML puro.
    """
    resp_prod = model.generate_content(prompt_produtos)
    html_prod = limpar_html(resp_prod.text)
    with open("produtos.html", "w", encoding="utf-8") as f:
        f.write(html_prod)
    print("✅ produtos.html gerado e padronizado!")

    # 3. Geração da Página do Blog (blog.html)
    print("🤖 Agente gerando a página do Blog (blog.html)...")
    prompt_blog = f"""
    {contexto_global}
    Crie a página de artigos técnicos do blog (blog.html) mantendo rigorosamente a mesma identidade visual e layout padrão das demais páginas.
    Inclua artigos de alto nível técnico sobre dimensionamento elétrico, ampacidade e normas ABNT aplicadas ao Polo Industrial.
    Retorne apenas o código HTML puro.
    """
    resp_blog = model.generate_content(prompt_blog)
    html_blog = limpar_html(resp_blog.text)
    with open("blog.html", "w", encoding="utf-8") as f:
        f.write(html_blog)
    print("✅ blog.html gerado e padronizado!")


def limpar_html(texto_gerado):
    """Remove marcações markdown de código se a IA retornar encapsulado"""
    if "```html" in texto_gerado:
        texto_gerado = texto_gerado.split("```html")[1].split("```")[0]
    elif "```" in texto_gerado:
        texto_gerado = texto_gerado.split("```")[1].split("```")[0]
    return texto_gerado.strip()


if __name__ == "__main__":
    gerar_conteudo_com_ia()
