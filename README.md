# LTLO (Leave The Light Off)

Este repositório contém o código-fonte de **LTLO**, um jogo desenvolvido em Python utilizando a biblioteca Pyglet. O projeto possui uma arquitetura híbrida: consiste no desenvolvimento do jogo propriamente dito e, simultaneamente, de uma engine proprietária experimental integrada ("Embedded Engine").

> **Nota:** O projeto encontra-se em estágio de desenvolvimento ativo (versão `dev1.0.0`). A engine e o jogo estão acoplados neste momento, com abstrações sendo criadas conforme a necessidade das mecânicas.

## Visão Geral da Arquitetura

O projeto não utiliza uma engine comercial (Godot, Unity), optando por uma implementação customizada sobre o framework multimídia Pyglet. A estrutura é dividida em camadas de controle e gerenciamento de entidades.

### Stack Tecnológico
*   **Linguagem:** Python 3
*   **Core Framework:** [Pyglet](https://pyglet.org/) (Janelas, Input, Renderização, Áudio)
*   **Build:** PyInstaller
*   **Dependência Externa:** FFmpeg (para decodificação de mídia)

### Estrutura do Sistema

A engine opera através de um sistema de controladores hierárquicos e um gerenciador de cenas customizado.

1.  **MasterController:** Gerencia o ciclo de vida da aplicação e a troca entre contextos maiores (Menu vs. Ingame).
2.  **Scene System (`game/scenes/`):**
    *   A classe base `Scene` implementa o *game loop*, gerenciamento de delta time, *event polling* e renderização.
    *   Possui suporte nativo para reprodução de vídeo e áudio via FFmpeg.
3.  **Entity System (`game/types/scenes.py`):**
    *   As entidades não seguem um padrão ECS estrito, mas sim uma composição onde objetos desenháveis do Pyglet (Sprites, Shapes, Labels) são envelopados em uma classe `Entity`.
    *   **Logic Injection:** A lógica não reside nas entidades. Ela é processada por "Systems" ou "Features" que iteram sobre as entidades baseando-se em `tags` e `ids`.
4.  **Commit System:**
    *   Para evitar problemas de modificação de listas durante a iteração, a engine utiliza um sistema de **Commits** (`commit_entities_update_by_id`).
    *   Alterações estruturais (spawn, destroy, replace) são enfileiradas e aplicadas em um momento seguro do frame.

## Estrutura de Diretórios

O código é organizado separando a lógica de engine ("core") das implementações específicas do jogo:

```text
gufl3r-ltlo/
├── game/
│   ├── entitymodels/   # "Prefabs" de entidades (Botões, Imagens, Inputs)
│   ├── features/       # Lógica de jogo modular (Mecânica de visão, Audio settings)
│   ├── scenes/         # Controladores de cena (Main Menu, Night, Final)
│   ├── systems/        # Inicialização e lógica de processo por cena
│   ├── types/          # Definições de tipos de dados (Dataclasses)
│   └── mastercontroller.py
├── utils/              # Bibliotecas auxiliares (Assets, Save, Path, Math)
├── libs/               # DLLs externas (FFmpeg)
├── main.py             # Entry point
└── config.json         # Configurações base (Resolução nativa)
```

## Dependências e Configuração

Para executar o projeto, é necessário configurar o ambiente Python e fornecer as bibliotecas binárias exigidas pelo Pyglet para manipulação de mídia.

### 1. Ambiente Python
Instale as dependências listadas (o projeto utiliza Pyglet como dependência principal).

```bash
pip install -r requirements.txt
```

### 2. Binários do FFmpeg (Obrigatório)
O Pyglet requer binários do FFmpeg para processar áudio e vídeo. **Estes arquivos não estão incluídos no controle de versão.**

1.  Obtenha uma build **shared** do FFmpeg (contendo as DLLs `avcodec`, `avformat`, `avutil`, `swresample`, `swscale`, etc.).
2.  Crie a pasta `libs/ffmpeg/` na raiz do projeto, se não existir.
3.  Coloque as DLLs dentro desta pasta.

O arquivo `main.py` carrega dinamicamente essas DLLs via `utils.libs.load()` antes de iniciar a janela.

## Build

O projeto inclui um script de build (`build.bat`) configurado para o PyInstaller. Ele gera um executável único (`--onefile`), empacotando os assets e bibliotecas.

```bat
# Exemplo de execução (Windows)
.\build.bat
```

O script assume que um ambiente virtual (`.venv`) está presente na raiz. O executável final será gerado na pasta `build/`.

## Funcionalidades Implementadas

Atualmente, o repositório reflete o seguinte estado de desenvolvimento:

*   **Sistema de Salvamento:** Persistência de dados em JSON localizada em `Meus Documentos/{Author}/{Slug}`, gerenciando configurações e progresso.
*   **Menu de Configurações:**
    *   Controle de resolução (com suporte a troca dinâmica).
    *   Alternância de Fullscreen.
    *   Mixer de áudio (Master, Music, SFX, Cutscene) com *numeric steppers*.
*   **Mecânicas In-Game ("Night Scene"):**
    *   Renderização de cenário 2D.
    *   Sistema de "Sight" (Visão): Detecção de mouse nas bordas da tela para realizar o *panning* da câmera (movimentação relativa do cenário).
*   **Media Player:** Suporte integrado para *cutscenes* e áudio ambiente.

## Limitações Conhecidas

*   **Engine Acoplada:** A engine não é instalável como pacote separado; classes de "Game" herdam diretamente de classes de "Engine" no mesmo diretório.
*   **Hardcoded Resolutions:** As opções de resolução estão definidas estaticamente em `utils.save.RESOLUTION_OPTIONS`.
*   **FPS Loop:** O controle de framerate é feito manualmente via `time.sleep` e `pyglet.clock.tick`, com um sistema de correção de *drift* de tempo.