"""Gera as páginas dos capítulos do site a partir dos textos em Markdown.

Uso (na pasta do site):  python3 fonte/build.py
Precisa do pandoc instalado. Cada arquivo .md em fonte/ vira uma página .html.
"""
import pathlib
import re
import subprocess

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTE = RAIZ / "fonte"

TOPO = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} · Do Dado ao Banco</title>
<meta name="description" content="{parte}, {numero}: {titulo}. Banco de dados para quem não sabe absolutamente nada.">
<link rel="icon" href="imagens/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,400;0,700;1,400&family=Poppins:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="estilo.css">
</head>
<body>
<header class="topo"><nav>
<a class="marca" href="index.html"><img src="imagens/favicon.png" alt="">Do Dado ao Banco</a>
<span class="menu"><a href="index.html#caminho">Capítulos</a><a href="sobre.html">Sobre</a></span>
</nav></header>
<main>
<span class="selo">{parte} · {numero}</span>
<h1>{titulo}</h1>
"""

RODAPE = """
<nav class="navegacao"><a href="index.html#caminho">← Todos os capítulos</a><span class="embreve">Próximo: Do caderno à planilha</span></nav>
</main>
<footer class="rodape">
<p>Do Dado ao Banco, criado por Vera Lúcia Rosendo em parceria com Claude (Anthropic).</p>
<p>Livre para copiar, adaptar e compartilhar, citando a autoria, sob a licença <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.pt-br">CC BY-SA 4.0</a>.</p>
</footer>
</body>
</html>
"""


def ler(md_path):
    texto = md_path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    meta = dict(linha.split(": ", 1) for linha in m.group(1).splitlines())
    return meta, texto[m.end():]


def main():
    for md in sorted(FONTE.glob("*.md")):
        meta, corpo = ler(md)
        html = subprocess.run(
            ["pandoc", "-f", "markdown", "-t", "html5", "--wrap=none"],
            input=corpo, capture_output=True, text=True, check=True,
        ).stdout
        pagina = TOPO.format(**meta) + html + RODAPE
        (RAIZ / meta["arquivo"]).write_text(pagina, encoding="utf-8")
        print("gerado:", meta["arquivo"])


if __name__ == "__main__":
    main()
