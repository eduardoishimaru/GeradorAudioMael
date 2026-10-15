# Mael Audio — O Herdeiro dos Destinos

**Versão:** 1.0.0  
**Linguagem:** Python 3.11+  
**Plataforma:** Windows 10/11  
**Licença:** Uso pessoal

## 1. Descrição

O **Mael Audio** é um projeto Python para converter a história de **Mael — O Herdeiro dos Destinos**, personagem de Dungeons & Dragons, em um audiolivro narrado em português brasileiro.

A história acompanha Mael, um Aasimar, Mago da Escola de Adivinhação, desde seu nascimento até alcançar o nível 8.

O sistema utiliza a biblioteca `edge-tts` para sintetizar a narração com voz neural masculina, gerando arquivos MP3 individuais por capítulo e um arquivo consolidado.

A narração segue o estilo de um Mestre de RPG, sem música ou efeitos sonoros.

## 2. Funcionalidades

- Conversão de texto em áudio com voz neural.
- Narração em português brasileiro.
- Identificação automática de prólogo, capítulos e epílogo.
- Divisão automática de textos extensos em trechos menores.
- Geração de arquivos MP3 individuais.
- Consolidação dos capítulos em um único audiolivro.
- Configuração de voz, velocidade e volume.
- Remoção de marcações Markdown e instruções entre colchetes.
- Até três tentativas de geração em caso de falha.
- Utilização gratuita, sem chave de API.

**Limitações:**

- Necessita de conexão com a internet.
- A disponibilidade do serviço de síntese de voz pode variar.
- Não diferencia automaticamente as vozes dos personagens.
- As pausas indicadas entre colchetes são removidas, não convertidas em pausas temporizadas.
- Recomenda-se utilizar FFmpeg para a consolidação final dos arquivos MP3.

## 3. Estrutura do projeto

```text
C:\MaelAudio\
│
├── gerar_audio.py
├── historia_mael.txt
├── README.md
│
├── .venv\
│
└── audio\
    ├── capitulo_01.mp3
    ├── capitulo_02.mp3
    ├── capitulo_03.mp3
    ├── capitulo_04.mp3
    ├── capitulo_05.mp3
    ├── capitulo_06.mp3
    ├── capitulo_07.mp3
    ├── capitulo_08.mp3
    ├── capitulo_09.mp3
    ├── capitulo_10.mp3
    ├── mael_completo.mp3
    └── mael_completo_final.mp3
```

Os arquivos de áudio são criados automaticamente durante a execução.

## 4. Pré-requisitos

- Windows 10 ou Windows 11.
- Python 3.11 ou superior.
- Acesso à internet.
- PowerShell.
- FFmpeg (recomendado para consolidação final).

Verifique a instalação do Python:

```powershell
python --version
```

Ou:

```powershell
py --version
```

## 5. Instalação

### 5.1. Criar a pasta do projeto

Abra o PowerShell:

```powershell
New-Item -ItemType Directory -Path C:\MaelAudio -Force
Set-Location C:\MaelAudio
```

### 5.2. Criar o ambiente virtual

```powershell
py -m venv .venv
```

### 5.3. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Se houver bloqueio da política de execução, utilize na sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 5.4. Atualizar o pip

```powershell
python -m pip install --upgrade pip
```

### 5.5. Instalar as dependências

```powershell
python -m pip install edge-tts
```

Para registrar as dependências instaladas:

```powershell
python -m pip freeze > requirements.txt
```

Em instalações futuras, utilize:

```powershell
python -m pip install -r requirements.txt
```

## 6. Preparar a história

Crie o arquivo:

```text
C:\MaelAudio\historia_mael.txt
```

O arquivo deve utilizar codificação UTF-8.

Cole o roteiro completo da história de Mael, mantendo os títulos dos capítulos.

Exemplo:

```text
PRÓLOGO — A CRIANÇA DO ECLIPSE

Há muito tempo, quando os reinos ainda erguiam
suas muralhas contra criaturas esquecidas...

CAPÍTULO I — O DESPERTAR ARCANO

Mael tinha dezesseis anos quando um estranho
chegou a Valedorn...

CAPÍTULO II — OS OLHOS DO DESTINO

Dois anos se passaram...
```

### Organização dos capítulos

| Arquivo | Conteúdo |
|---|---|
| capitulo_01.mp3 | Prólogo — A Criança do Eclipse |
| capitulo_02.mp3 | Capítulo I — O Despertar Arcano |
| capitulo_03.mp3 | Capítulo II — Os Olhos do Destino |
| capitulo_04.mp3 | Capítulo III — A Biblioteca dos Ecos |
| capitulo_05.mp3 | Capítulo IV — O Ritual das Sete Estrelas |
| capitulo_06.mp3 | Capítulo V — A Luz que Não se Apaga |
| capitulo_07.mp3 | Capítulo VI — O Preço do Conhecimento |
| capitulo_08.mp3 | Capítulo VII — O Guardião do Véu |
| capitulo_09.mp3 | Capítulo VIII — Aquele que Escolhe o Amanhã |
| capitulo_10.mp3 | Epílogo — O Nono Caminho |

A numeração é determinada pela ordem em que os capítulos aparecem no arquivo de texto.

## 7. Configurações

As configurações estão disponíveis no início do arquivo `gerar_audio.py`.

```python
VOZ = "pt-BR-AntonioNeural"
VELOCIDADE = "-8%"
VOLUME = "+0%"
PAUSA_CAPITULO_MS = 2000
MAX_CARACTERES = 2500
```

### Voz

A voz padrão é:

```python
VOZ = "pt-BR-AntonioNeural"
```

Para consultar as vozes disponíveis:

```powershell
edge-tts --list-voices | Select-String "pt-BR"
```

### Velocidade

| Configuração | Característica |
|---|---|
| -15% | Narração mais lenta |
| -8% | Narração moderada, estilo RPG |
| +0% | Velocidade normal |
| +10% | Narração acelerada |

Exemplo:

```python
VELOCIDADE = "-8%"
```

### Volume

```python
VOLUME = "+0%"
```

### Tamanho dos trechos

```python
MAX_CARACTERES = 2500
```

Controla o tamanho máximo aproximado de cada trecho enviado para síntese.

**Nota:** A variável `PAUSA_CAPITULO_MS` está reservada para uma implementação futura de pausas. Na versão 1.0.0, ela não produz silêncio automaticamente.

## 8. Execução

Abra o PowerShell:

```powershell
cd C:\MaelAudio
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Execute:

```powershell
python gerar_audio.py
```

O programa identificará os capítulos e iniciará a síntese.

Exemplo de saída:

```text
Capítulos encontrados: 10

[1/10] PRÓLOGO — A CRIANÇA DO ECLIPSE
  Gerando trecho 1/3
  Gerando trecho 2/3
  Gerando trecho 3/3
  Salvo: capitulo_01.mp3

[2/10] CAPÍTULO I — O DESPERTAR ARCANO
  Gerando trecho 1/4
  ...

Processamento concluído.
Arquivo final: C:\MaelAudio\audio\mael_completo.mp3
```

## 9. Consolidação com FFmpeg

O programa gera `mael_completo.mp3` por concatenação direta dos segmentos.

Para obter uma versão consolidada com melhor compatibilidade, utilize FFmpeg.

### 9.1. Instalar FFmpeg

```powershell
winget install Gyan.FFmpeg
```

Reabra o PowerShell e verifique:

```powershell
ffmpeg -version
```

### 9.2. Consolidar os capítulos

```powershell
cd C:\MaelAudio\audio

$arquivos = Get-ChildItem "capitulo_*.mp3" |
    Sort-Object Name

$lista = foreach ($arquivo in $arquivos) {
    "file '$($arquivo.Name)'"
}

$lista | Set-Content "lista.txt" -Encoding ascii

ffmpeg -y -f concat -safe 0 -i lista.txt `
    -c:a libmp3lame -b:a 192k `
    mael_completo_final.mp3
```

O resultado será:

```text
C:\MaelAudio\audio\mael_completo_final.mp3
```

## 10. Solução de problemas

### Python não encontrado

Verifique:

```powershell
py --version
```

Caso não esteja instalado, instale o Python e recrie o ambiente virtual.

### Falha ao ativar o ambiente virtual

Execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois:

```powershell
.\.venv\Scripts\Activate.ps1
```

### ModuleNotFoundError: No module named 'edge_tts'

Instale a dependência no ambiente virtual:

```powershell
python -m pip install edge-tts
```

### Arquivo historia_mael.txt não encontrado

Confirme a existência do arquivo:

```powershell
Test-Path C:\MaelAudio\historia_mael.txt
```

O resultado esperado é:

```text
True
```

### Falha na geração do áudio

Verifique a conexão com a internet e a disponibilidade do serviço de síntese.

O script realiza até três tentativas por trecho antes de interromper a execução.

### Capítulos não identificados corretamente

Confirme que os títulos começam no início da linha e seguem o padrão:

```text
PRÓLOGO — TÍTULO
CAPÍTULO I — TÍTULO
CAPÍTULO II — TÍTULO
EPÍLOGO — TÍTULO
```

### FFmpeg não reconhecido

Reabra o PowerShell após a instalação.

Se necessário, verifique se o executável está disponível no PATH.

## 11. Arquivos gerados

| Arquivo | Descrição |
|---|---|
| capitulo_01.mp3 até capitulo_10.mp3 | Áudios individuais |
| mael_completo.mp3 | Concatenação realizada pelo Python |
| mael_completo_final.mp3 | Arquivo consolidado com FFmpeg |
| lista.txt | Lista utilizada pelo FFmpeg |

A pasta `audio` é criada automaticamente pelo script.

## 12. Melhorias planejadas

Possíveis evoluções do projeto:

- Suporte a múltiplas vozes para os personagens.
- Pausas temporizadas entre cenas e capítulos.
- Interface gráfica para Windows.
- Seleção de voz e velocidade pela interface.
- Geração de arquivos M4B com capítulos.
- Inclusão de metadados e capa no audiolivro.
- Registro de logs de execução.
- Retomada automática após falhas.
- Geração de legendas sincronizadas.
- Empacotamento como executável Windows.
- Normalização de volume com FFmpeg.

## 13. Versionamento

### Versão 1.0.0

Implementação inicial contendo:

- Síntese neural com `edge-tts`.
- Identificação automática de capítulos.
- Divisão do texto em trechos.
- Geração de MP3 por capítulo.
- Consolidação básica dos arquivos.
- Configuração de voz, velocidade e volume.
- Tratamento simples de falhas com novas tentativas.

## 14. Considerações finais

O Mael Audio permite transformar um roteiro narrativo em um audiolivro sem necessidade de gravação manual.

O projeto foi desenvolvido para a história de Mael, mas pode ser adaptado para outros personagens, campanhas de RPG, contos e narrativas.

Para melhores resultados, recomenda-se revisar o texto antes da geração, manter os títulos padronizados e ouvir cada capítulo para identificar eventuais problemas de pronúncia.

---

**Projeto:** Mael Audio  
**Obra:** Mael — O Herdeiro dos Destinos  
**Versão:** 1.0.0  
**Personagem:** Mael, Aasimar, Mago da Escola de Adivinhação  
**Narrativa:** Níveis 1 a 8
