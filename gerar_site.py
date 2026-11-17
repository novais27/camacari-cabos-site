import os
import re
import time
from datetime import datetime
from google import genai
from google.genai.errors import ServerError

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada!")

client = genai.Client(api_key=api_key)

PROMPT_AGENTE_BLOG = """
Você é o Redator Comercial e Especialista em Materiais Elétricos da Camaçari Cabos (fundada em 2014, localizada na Rua Centro, 249, Camaçari - BA, CEP 42800-029, Telefones: 71 2136-4416 e WhatsApp 71 99666-0988).

REGRAS DE OURO DO NEGÓCIO (CRÍTICO):
1. A Camaçari Cabos é FORNECEDORA de materiais elétricos e cabeamento estruturado (atacado e varejo).
2. NUNCA diga que fazemos projetos elétricos, estudos luminotécnicos, laudos, acompanhamento técnico, instalações ou dimensionamento.
3. O foco deve ser nos PRODUTOS que fornecemos, diferenças entre materiais, dicas práticas de escolha, aplicação e conservação para os 3 públicos:
   - Industrial (Polo Industrial de Camaçari, galpões logísticos, hospitais, manutenção MRO): Cabos HEPR 1kV, XLPE, PVC 750V, cabos de controle, instrumentação blindado Shield, cabo PP, cobre nu, eletrocalhas, perfilados, eletrodutos galvanizados, conduletes de alumínio e PVC, prensa-cabos, plugs e tomadas industriais, quadro robô, quadro de comando, disjuntores caixa moldada, iluminação High Bay e rede estruturada (Cat5e, Cat6, patch panel, switches, patch cord, RJ45).
   - Comercial (lojas, clínicas, consultórios, restaurantes, escritórios): Iluminação LED, perfis, fitas de LED, painéis, spots, cabos antichama BWF, quadros QDC, disjuntores DIN, DR e DPS, tomadas e cabeamento de rede.
   - Residencial (casas, reformas e condomínios em Camaçari e Litoral Norte): Kits Padrão Coelba homologados (monofásico, bifásico, trifásico), hastes de aterramento, cobre nu, conectores, fios e cabos 750V/1kV, proteção DR/DPS e iluminação residencial.

TAREFA:
Gere exatamente 3 novos artigos de blog completos e aprofundados (1 Industrial, 1 Comercial e 1 Residencial).
Cada artigo deve ter um resumo curto visível no card e uma seção `.artigo-completo` contendo um texto aprofundado (com pelo menos 4 parágrafos detalhados, 2 a 3 subtítulos `<h3>` e um bloco final convidando o leitor a comprar na Camaçari Cabos).
Retorne APENAS o código HTML dos 3 elementos `<article>...</article>` (sem markdown, sem `<html>` ou `<body>`).

ESTRUTURA HTML OBRIGATÓRIA PARA CADA UM DOS 3 `<article>`:
<article class="bg-white rounded-2xl shadow-md border border-slate-200 p-6 flex flex-col justify-between hover:shadow-xl transition">
    <div>
        <div class="flex items-center justify-between gap-2 mb-3">
            <span class="text-[11px] font-extrabold uppercase bg-blue-100 text-blue-950 px-2.5 py-1 rounded">CATEGORIA (Industrial, Comercial ou Residencial)</span>
            <span class="text-[11px] text-slate-400 font-medium">DATA_ATUAL</span>
        </div>
        <h2 class="text-lg font-black text-blue-950 mb-3 leading-snug">TÍTULO ATRATIVO DO ARTIGO</h2>
        <p class="text-xs text-slate-600 leading-relaxed mb-4">Resumo instigante de 2 a 3 linhas apresentando o tema do artigo para despertar o clique no botão de leitura completa...</p>
    </div>

    <div class="artigo-completo hidden space-y-4 text-slate-700 text-sm md:text-base leading-relaxed">
        <p>Parágrafo de introdução contextualizando a importância da escolha correta dos materiais na indústria, comércio ou residência.</p>
        <h3 class="text-lg font-black text-blue-950 pt-2">1. Primeiro Subtítulo Aprofundando nos Produtos</h3>
        <p>Explicação rica e detalhada sobre as especificações, vantagens práticas e aplicações dos materiais fornecidos.</p>
        <h3 class="text-lg font-black text-blue-950 pt-2">2. Segundo Subtítulo com Dicas Práticas de Compra e Aplicação</h3>
        <p>Mais detalhes sobre durabilidade, segurança, normas de fabricação dos produtos e itens complementares.</p>
        <div class="bg-blue-50 border-l-4 border-amber-500 p-5 rounded-r-xl mt-6">
            <h4 class="font-black text-blue-950 text-base">Encontre a Linha Completa na Camaçari Cabos!</h4>
            <p class="text-xs md:text-sm text-slate-700 mt-1">Parágrafo final chamando o cliente para adquirir esses materiais a pronta entrega na Camaçari Cabos (Rua Centro, 249, Camaçari - BA) ou solicitar cotação rápida pelo WhatsApp (71) 99666-0988, atendendo todo o Polo Industrial, Camaçari e Região Metropolitana.</p>
        </div>
    </div>

    <div class="mt-4 pt-4 border-t border-slate-100 flex justify-between items-center">
        <button onclick="abrirLeitorArtigo(this)" class="bg-blue-50 hover:bg-blue-950 text-blue-950 hover:text-white font-extrabold px-3.5 py-2 rounded-lg text-xs transition flex items-center gap-1.5">
            <i class="fa-solid fa-book-open text-amber-500"></i> Ler artigo completo
        </button>
        <a href="https://wa.me/5571996660988?text=Olá, li o artigo no blog da Camaçari Cabos e gostaria de fazer uma cotação" target="_blank" class="text-emerald-600 hover:text-emerald-500 font-extrabold text-xs flex items-center gap-1">
            Cotar <i class="fa-brands fa-whatsapp text-sm"></i>
        </a>
    </div>
</article>
"""

def limpar_codigo(texto):
    if "```html" in texto:
        texto = texto.split("```html")[1].split("```")[0]
    elif "```" in texto:
        texto = texto.split("```")[1].split("```")[0]
    return texto.strip()

def atualizar_apenas_blog(max_tentativas=4):
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    prompt_final = PROMPT_AGENTE_BLOG.replace("DATA_ATUAL", data_hoje)

    print("🤖 Gerando 3 novos artigos aprofundados (Industrial, Comercial e Residencial)...")
    novos_artigos_html = ""

    for tentativa in range(1, max_tentativas + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt_final
            )
            novos_artigos_html = limpar_codigo(response.text)
            break
        except ServerError as e:
            print(f"⚠️ Servidor ocupado (tentativa {tentativa}/{max_tentativas}). Aguardando 8s...")
            if tentativa == max_tentativas:
                raise e
            time.sleep(8)

    if not os.path.exists("blog.html"):
        raise FileNotFoundError("O arquivo blog.html não foi encontrado no repositório!")

    with open("blog.html", "r", encoding="utf-8") as f:
        html_atual = f.read()

    marcador = "<!-- NOVOS_ARTIGOS_AQUI -->"
    if marcador in html_atual:
        html_novo = html_atual.replace(marcador, f"{marcador}\n\n{novos_artigos_html}")
    else:
        padrao_grid = re.compile(r'(<section[^>]*grid[^>]*>)', re.IGNORECASE)
        if padrao_grid.search(html_atual):
            html_novo = padrao_grid.sub(r'\1\n    <!-- NOVOS_ARTIGOS_AQUI -->\n' + novos_artigos_html, html_atual, count=1)
        else:
            raise ValueError("Não foi possível localizar a seção de artigos no blog.html.")

    with open("blog.html", "w", encoding="utf-8") as f:
        f.write(html_novo)

    print("✅ blog.html atualizado com sucesso com artigos expansíveis!")

if __name__ == "__main__":
    atualizar_apenas_blog()
