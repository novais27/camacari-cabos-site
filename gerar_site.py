import os
import google.generativeai as genai

# Pega a chave secreta configurada no GitHub Actions
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada!")

genai.configure(api_key=api_key)

def criar_pagina_produto():
    # Atualizado para o modelo recomendável atual
    model = genai.GenerativeModel('gemini-3.8-flash')
    
    prompt = """
    Você é o Agente Especialista em SEO, Fichas Técnicas e GEO da empresa Camaçari Cabos (localizada em Camaçari - BA).
    Crie uma página HTML completa e estruturada (usando Tailwind CSS) para o catálogo de produtos, 
    destacando cabos elétricos residenciais e industriais, normas técnicas (ABNT), e uma seção de Perguntas Frequentes (FAQs) 
    otimizada para que os mecanismos de busca de IAs (como ChatGPT Search e Google AI Overviews) recomendem a Camaçari Cabos.
    Retorne apenas o código HTML puro.
    """
    
    print("🤖 Agente gerando nova página otimizada para a Camaçari Cabos...")
    response = model.generate_content(prompt)
    html_content = response.text

    # Limpeza robusta de blocos markdown caso a IA retorne crases extras
    if "```html" in html_content:
        html_content = html_content.split("```html")[1].split("```")[0]
    elif "```" in html_content:
        html_content = html_content.split("```")[1].split("```")[0]

    # Salva ou atualiza a página de produtos automaticamente
    with open("produtos.html", "w", encoding="utf-8") as f:
        f.write(html_content.strip())
        
    print("✅ Página de produtos atualizada com sucesso!")

if __name__ == "__main__":
    criar_pagina_produto()
