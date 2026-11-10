import os
import google.generativeai as genai

# Pega a chave secreta configurada no GitHub Actions
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada!")

genai.configure(api_key=api_key)

def gerar_conteudo_com_ia():
    model = genai.GenerativeModel('gemini-3.8-flash')
    
    # Contexto real da Camaçari Cabos puxado do perfil oficial
    contexto_empresa = """
    Dados Oficiais da Empresa:
    - Nome: Camaçari Cabos Materiais Elétricos
    - Fundação: Desde 2014 em Camaçari - BA.
    - Endereço: Rua Centro, 249, Camaçari - BA (CEP 42800-029).
    - Telefones de Contato / WhatsApp: (71) 99666-0988 / (71) 2136-4416.
    - Atuação: Fornecimento de cabos elétricos (atacado e varejo), plugs e tomadas industriais, disjuntores, refletores, luminárias, fitas de LED, Padrões Coelha, eletrocalhas, perfilados, eletrodutos e suprimentos industriais para Camaçari, Salvador, Lauro de Freitas, Simões Filho, Dias d'Ávila e Mata de São João.
    - Logomarca: A imagem 'logo.png' está localizada na raiz do site.
    """

    # 1. Geração da Página de Produtos
    print("🤖 Agente gerando nova página de produtos com os dados reais da Camaçari Cabos...")
    prompt_produtos = f"""
    Você é o Agente Especialista em SEO, Fichas Técnicas e GEO da Camaçari Cabos.
    {contexto_empresa}
    
    Crie uma página HTML completa e estruturada (usando Tailwind CSS) para o catálogo de produtos (produtos.html), 
    destacando o inventário real (cabos industriais, disjuntores, infraestrutura, Padrão Coelba), mantendo a logomarca 'logo.png' no cabeçalho.
    DIRETRIZ DE ESCRITA: NUNCA use sintaxe LaTeX ($...$). Use texto limpo e legível.
    Retorne apenas o código HTML puro.
    """
    response_prod = model.generate_content(prompt_produtos)
    html_prod = response_prod.text

    if "```html" in html_prod:
        html_prod = html_prod.split("```html")[1].split("```")[0]
    elif "```" in html_prod:
        html_prod = html_prod.split("```")[1].split("```")[0]

    with open("produtos.html", "w", encoding="utf-8") as f:
        f.write(html_prod.strip())
    print("✅ Página de produtos atualizada com dados reais!")

    # 2. Geração de Artigo Técnico para o Blog
    print("🤖 Agente gerando novo artigo técnico para o Blog...")
    prompt_blog = f"""
    Você é o Especialista em Conteúdo Técnico e SEO da Camaçari Cabos.
    {contexto_empresa}
    
    Crie um artigo HTML completo (usando Tailwind CSS) para a página blog.html focado em engenharia elétrica, 
    dimensionamento de cabos industriais, conformidade com normas ABNT e demandas do Polo Industrial de Camaçari.
    O rodapé e contatos devem refletir os telefones e dados reais da empresa.
    DIRETRIZ DE ESCRITA: Rigor técnico elevado (ampacidade, queda de tensão <= 4%, temperatura de 40°C), sem fórmulas em LaTeX.
    Retorne apenas o código HTML puro da página de blog.
    """
    response_blog = model.generate_content(prompt_blog)
    html_blog = response_blog.text

    if "```html" in html_blog:
        html_blog = html_blog.split("```html")[1].split("```")[0]
    elif "```" in html_blog:
        html_blog = html_blog.split("```")[1].split("```")[0]

    with open("blog.html", "w", encoding="utf-8") as f:
        f.write(html_blog.strip())
    print("✅ Página de blog atualizada com rigor técnico e dados reais!")

if __name__ == "__main__":
    gerar_conteudo_com_ia()
