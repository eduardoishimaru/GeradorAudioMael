
import asyncio
import re
import struct
from pathlib import Path

import edge_tts

BASE = Path(__file__).resolve().parent
ENTRADA = BASE / "historia_mael.txt"
SAIDA = BASE / "audio"

VOZ = "pt-BR-AntonioNeural"
VELOCIDADE = "-8%"
VOLUME = "+0%"
PAUSA_CAPITULO_MS = 2000
MAX_CARACTERES = 2500

SAIDA.mkdir(exist_ok=True)


def limpar_texto(texto):
    # Remove instruções de interpretação: [pausa], [voz grave] etc.
    texto = re.sub(r"\[[^\]]*\]", "", texto)

    # Remove marcações Markdown.
    texto = re.sub(r"[*_#`]", "", texto)

    # Remove linhas de metadados.
    texto = re.sub(
        r"(?im)^(narrador|formato|idioma|áudio|estilo|"
        r"duração estimada):.*$",
        "",
        texto,
    )

    return re.sub(r"\n{3,}", "\n\n", texto).strip()


def dividir_capitulos(texto):
    padrao = re.compile(
        r"(?im)^(?:PRÓLOGO|EPÍLOGO|CAP[IÍ]TULO\s+"
        r"(?:[IVX]+|\d+))\s*[—:-].*$"
    )

    linhas = texto.splitlines()
    capitulos = []
    titulo = "INTRODUÇÃO"
    conteudo = []

    for linha in linhas:
        if padrao.match(linha.strip()):
            if conteudo and "".join(conteudo).strip():
                capitulos.append(
                    (titulo, "\n".join(conteudo))
                )
            titulo = linha.strip()
            conteudo = [titulo]
        else:
            conteudo.append(linha)

    if conteudo and "".join(conteudo).strip():
        capitulos.append((titulo, "\n".join(conteudo)))

    return capitulos


def dividir_trechos(texto, limite=MAX_CARACTERES):
    paragrafos = re.split(r"\n\s*\n", texto)
    partes = []
    atual = ""

    for paragrafo in paragrafos:
        frases = re.split(
            r"(?<=[.!?])\s+",
            paragrafo.strip()
        )

        for frase in frases:
            while len(frase) > limite:
                corte = frase.rfind(" ", 0, limite)
                if corte < 1:
                    corte = limite

                if atual:
                    partes.append(atual.strip())
                    atual = ""

                partes.append(frase[:corte].strip())
                frase = frase[corte:].strip()

            if len(atual) + len(frase) + 1 > limite:
                if atual:
                    partes.append(atual.strip())
                atual = frase
            else:
                atual = (atual + " " + frase).strip()

    if atual:
        partes.append(atual.strip())

    return partes


async def sintetizar(texto, destino):
    comunicacao = edge_tts.Communicate(
        text=texto,
        voice=VOZ,
        rate=VELOCIDADE,
        volume=VOLUME,
    )
    await comunicacao.save(str(destino))


def silencio_mp3(duracao_ms):
    # Quadro MPEG-2 Layer III, 16 kbps, 24 kHz, mono.
    # Cada quadro contém 576 amostras (~24 ms).
    cabecalho = bytes.fromhex("FFF3A4C4")
    tamanho = 48
    quadro = cabecalho + bytes(tamanho - 4)
    quantidade = round(duracao_ms / 24)
    return quadro * quantidade


def unir_mp3(arquivos, destino):
    # Concatenação de MP3s com os mesmos parâmetros
    # de codificação. Para maior compatibilidade,
    # recomenda-se FFmpeg (ver observação abaixo).
    with destino.open("wb") as saida:
        for indice, arquivo in enumerate(arquivos):
            if indice:
                # Sem silêncio artificial, evitando
                # incompatibilidade entre codificações.
                pass
            saida.write(arquivo.read_bytes())


async def main():
    if not ENTRADA.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ENTRADA}"
        )

    texto = ENTRADA.read_text(encoding="utf-8")
    capitulos = dividir_capitulos(texto)

    if not capitulos:
        raise ValueError("Nenhum texto encontrado.")

    arquivos_capitulos = []

    print(f"Capítulos encontrados: {len(capitulos)}")

    for numero, (titulo, conteudo) in enumerate(
        capitulos, start=1
    ):
        print(f"\n[{numero}/{len(capitulos)}] {titulo}")

        conteudo = limpar_texto(conteudo)
        partes = dividir_trechos(conteudo)
        arquivos_temporarios = []

        for indice, parte in enumerate(partes, start=1):
            temporario = SAIDA / (
                f"temp_{numero:02d}_{indice:03d}.mp3"
            )

            print(f"  Gerando trecho {indice}/{len(partes)}")

            for tentativa in range(1, 4):
                try:
                    await sintetizar(parte, temporario)
                    break
                except Exception as erro:
                    if tentativa == 3:
                        raise
                    print(f"  Tentativa {tentativa}: {erro}")
                    await asyncio.sleep(3 * tentativa)

            arquivos_temporarios.append(temporario)

        destino = SAIDA / f"capitulo_{numero:02d}.mp3"
        unir_mp3(arquivos_temporarios, destino)

        arquivos_capitulos.append(destino)

        for temporario in arquivos_temporarios:
            temporario.unlink(missing_ok=True)

        print(f"  Salvo: {destino.name}")

    completo = SAIDA / "mael_completo.mp3"
    unir_mp3(arquivos_capitulos, completo)

    print("\nProcessamento concluído.")
    print(f"Arquivo final: {completo}")


if __name__ == "__main__":
    asyncio.run(main())
