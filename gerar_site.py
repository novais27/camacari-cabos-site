import os
import google.generativeai as genai

# Pega a chave secreta configurada no GitHub Actions
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada!")

genai.configure(api_key=api_key)

def gerar_conteudo_com_ia():
    # Utiliza o modelo estável atual
    model = genai.GenerativeModel('gemini-3.8-flash')
    
    # 1. Geração da Página de Produtos
    print("🤖 Agente gerando nova página de produtos para a Camaçari Cabos...")
    prompt_produtos = """
    Você é o Agente Especialista em SEO, Fichas Técnicas e GEO da empresa Camaçari Cabos (localizada em Camaçari - BA).
    Crie uma página HTML completa e estruturada (usando Tailwind CSS) para o catálogo de produtos, 
    destacando cabos elétricos residenciais e industriais, disjuntores, infraestrutura de iluminação e normas técnicas (ABNT).
    Inclua uma seção de Perguntas Frequentes (FAQs) otimizada para buscadores de IA.
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
    dimensionamento de cabos industriais, conformidade com normas ABNT ou dicas de infraestrutura para o Polo Industrial de Camaçari.
    O artigo deve ser informativo, de alto nível técnico e otimizado para o Google (SEO) e IAs.
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
    print("✅ Página de blog atualizada com novo artigo técnico!")

if __name__ == "__main__":
    gerar_conteudo_com_ia()
