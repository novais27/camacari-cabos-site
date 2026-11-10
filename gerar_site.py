import os
import google.generativeai as genai

# Pega a chave secreta configurada no GitHub Actions
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada!")

genai.configure(api_key=api_key)

def gerar_conteudo_com_ia():
    model = genai.GenerativeModel('gemini-3.8-flash')
    
    # 1. Geração da Página de Produtos
    print("🤖 Agente gerando nova página de produtos para a Camaçari Cabos...")
    prompt_produtos = """
    Você é o Agente Especialista em SEO, Fichas Técnicas e GEO da empresa Camaçari Cabos (localizada em Camaçari - BA).
    Crie uma página HTML completa e estruturada (usando Tailwind CSS) para o catálogo de produtos, 
    destacando cabos elétricos industriais, residenciais, disjuntores, infraestrutura e normas ABNT.
    DIRETRIZ DE ESCRITA: NUNCA use sintaxe LaTeX ($...$) ou códigos matemáticos crus. Use texto limpo e legível (ex: delta V menor ou igual a 4%, 40 graus Celsius).
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
    print("✅ Página de produtos atualizada!")

    # 2. Geração de Artigo Técnico para o Blog
    print("🤖 Agente gerando novo artigo técnico para o Blog...")
    prompt_blog = """
    Você é o Especialista em Conteúdo Técnico e SEO da Camaçari Cabos.
    Crie um artigo HTML completo (usando Tailwind CSS) para a página blog.html focado em engenharia elétrica, 
    dimensionamento de cabos industriais, conformidade com normas ABNT e demandas do Polo Industrial de Camaçari.
    DIRETRIZ DE ESCRITA: Mantenha altíssimo rigor técnico (ampacidade, fatores de correção, queda de tensão), 
    mas NUNCA utilize fórmulas em LaTeX ($...$). Escreva os símbolos e variáveis em texto claro e profissional (ex: Queda de Tensão <= 4%, Temperatura de 40°C, Fator Ft = 0.91).
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
    print("✅ Página de blog atualizada sem ruídos de formatação!")

if __name__ == "__main__":
    gerar_conteudo_com_ia()
