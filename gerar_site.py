import os
import re
import time
from datetime import datetime
from google import genai
from google.genai.errors import ServerError

# Pega a chave secreta configurada no GitHub Actions
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada!")

client = genai.Client(api_key=api_key)

PROMPT_AGENTE_BLOG = """
Você é o Redator Comercial e Especialista em Produtos da Camaçari Cabos Materiais Elétricos (fundada em 2014, localizada na Rua Centro, 249, Camaçari - BA, WhatsApp 71 99666-0988).

REGRAS DE OURO DO NEGÓCIO (CRÍTICO):
1. A Camaçari Cabos é FORNECEDORA de materiais elétricos (atacado e varejo).
2. NUNCA diga que fazemos projetos elétricos, estudos luminotécnicos, laudos, acompanhamento de engenharia, instalações ou dimensionamento de materiais.
3. O foco do conteúdo deve ser nos PRODUTOS que vendemos, suas características, diferenças práticas, dicas de conservação, checklists de compra e aplicações para os 3 públicos:
   - Público Industrial (Polo Industrial de Camaçari, galpões logísticos, manutenção MRO): Cabos HEPR 1kV, XLPE, cabos de comando/controle, instrumentação blindado Shield, cabo PP, eletrocalhas, perfilados, conduletes de alumínio/PVC, plugs e tomadas industriais, quadro robô, quadro de comando, disjuntores caixa moldada, iluminação High Bay e cabeamento estruturado (Cat5e, Cat6, patch panel, switches, RJ45).
   - Público Comercial (lojas, clínicas, consultórios, restaurantes, escritórios): Painéis e fitas de LED, perfis de alumínio, refletores, cabos antichama BWF, quadros QDC, disjuntores DIN, DR e DPS, tomadas e acabamentos.
   - Público Residencial (casas, reformas, condomínios em Camaçari e Litoral Norte): Kits Padrão Coelba homologados (monofásico, bifásico, trifásico), hastes de aterramento, cobre nu, conectores, proteção contra surtos e raios (DPS), iluminação residencial e jardins.

TAREFA:
Gere exatamente 3 novos artigos de blog (1 voltado para Indústria/Galpões, 1 para Comércio/Serviços e 1 para Residências/Condomínios).
Retorne APENAS o código HTML dos 3 elementos <article>...</article> (sem <html>, sem <head>, sem <body> e sem blocos markdown).

ESTRUTURA HTML OBRIGATÓRIA PARA CADA UM DOS 3 <article>:
<article class="bg-white rounded-2xl shadow-md border border-slate-200 p-6 flex flex-col justify-between hover:shadow-lg transition">
    <div>
        <div class="flex items-center justify-between gap-2 mb-3">
            <span class="text-[11px] font-extrabold uppercase bg-blue-100 text-blue-950 px-2.5 py-1 rounded">CATEGORIA (Industrial, Comercial ou Residencial)</span>
            <span class="text-[11px] text-slate-400 font-medium">DATA_ATUAL</span>
        </div>
        <h2 class="text-lg font-black text-blue-950 mb-3 leading-snug">TÍTULO ATRATIVO DO ARTIGO</h2>
        <p class="text-xs text-slate-600 leading-relaxed mb-3">Primeiro parágrafo explicando de forma prática o produto, quando escolher cada modelo e vantagens de qualidade/segurança.</p>
        <p class="text-xs text-slate-600 leading-relaxed">Segundo parágrafo com dicas práticas de compra/aplicação e destacando que a Camaçari Cabos possui esses itens a pronta entrega.</p>
    </div>
    <div class="mt-6 pt-4 border-t border-slate-100 flex justify-between items-center">
        <span class="text-[11px] font-bold text-slate-500">Pronta entrega em Camaçari e RMS</span>
        <a href="https://wa.me/5571996660988?text=Olá, li o artigo no blog e gostaria de cotar materiais elétricos" target="_blank" class="text-amber-600 hover:text-amber-500 font-extrabold text-xs flex items-center gap-1">
            Cotar Produtos <i class="fa-brands fa-whatsapp"></i>
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

    print("🤖 Gerando 3 novos artigos (Industrial, Comercial e Residencial)...")
    novos_artigos_html = ""

    for tentativa in range(1, max_tentativas + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
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

    # Localiza o marcador de inserção ou a abertura da grade de artigos (<section ... grid ...>)
    marcador = "<!-- NOVOS_ARTIGOS_AQUI -->"
    if marcador in html_atual:
        html_novo = html_atual.replace(marcador, f"{marcador}\n\n{novos_artigos_html}")
    else:
        # Se ainda não tiver o marcador, insere logo na primeira <section> com grid de artigos
        padrao_grid = re.compile(r'(<section[^>]*grid[^>]*>)', re.IGNORECASE)
        if padrao_grid.search(html_atual):
            html_novo = padrao_grid.sub(r'\1\n    <!-- NOVOS_ARTIGOS_AQUI -->\n' + novos_artigos_html, html_atual, count=1)
        else:
            raise ValueError("Não foi possível localizar a seção de artigos no blog.html.")

    with open("blog.html", "w", encoding="utf-8") as f:
        f.write(html_novo)

    print("✅ blog.html atualizado com sucesso! Nenhuma outra página foi alterada.")

if __name__ == "__main__":
    atualizar_apenas_blog()
