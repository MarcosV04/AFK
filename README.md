<p align="center">
<img width="1000" alt="afk_img" src="https://github.com/user-attachments/assets/1fd5d1be-cbad-4606-bdb3-9af2782eaa1c" />

# 🎭 AFK - Away From the Keyboard

## 📌 Sobre o Projeto

O AFK (Away From the Keyboard) é um projeto que propõe uma nova forma de interação com jogos, substituindo o uso tradicional de teclado e mouse por gestos capturados pela câmera, assim trazendo novos desafio para o mundo dos jogos.

A proposta é desenvolver um jogo onde o jogador controla um personagem no estilo marionete através dos movimentos da mão, utilizando visão computacional.

---

## 🎯 Objetivo
- Criar uma aplicação que integre:
- Visão computacional
- Interação em tempo real
- Desenvolvimento de jogos

---

## 🛠️ Tecnologias
- Python
- OpenCV
- MediaPipe
- Pygame
- Pymunk
- Docker 

---

## 👁️ Visão Computacional
- Captura de vídeo em tempo real
- Detecção das mãos simultaneamente
- Rastreamento dos 21 pontos da mão (landmarks)

---

## 🎮 Proposta do Jogo

O jogo será baseado em controle por gestos:

- A câmera captura os movimentos da mão
- Os gestos são interpretados como comandos
- O personagem (marionete) reage em tempo real

O ambiente será um **palco**, com desafios progressivos:
- Obstáculos (espinhos, bombas, etc.)
- Aumento gradual da dificuldade
- Sistema de fases

---

## ⚙️ Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/MarcosV04/AFK.git
cd AFK
```

---

## 🖥️ Execução Local

### 2. Crie e ative o ambiente virtual
- Linux

```bash
python -m venv venv
source venv/bin/activate
```

- Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Execute o projeto

```bash
python main.py
```

---

## 🐳 Docker e Docker Compose

### 1. build do docker
- Docker
```bash
docker build -t afk-game .
```

- Docker Compose
```bash
docker compose up --build
```
---

### 2. Permissão de interface gráfica
- Linux
```bash
xhost +local:docker
```

---

### 3. Executar container
- Linux
```bash
docker run \
--device=/dev/video0 \
-e DISPLAY=$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix \
afk-game
```
---

### 4. Comando para utilizar script auxiliar
- Docker (Linux)
```bash
chmod +x rodar_docker.sh
```
---

### 5. Executando
- Docker (Linux)
```bash
./rodar_docker.sh
```

- Docker (Windows)
```bash
docker run --device=/dev/video0 afk-game
```

- Docker Compose
```bash
docker compose up
```

---

## ⚠️ Observações

### Linux
- Necessário permitir acesso gráfico.
- Necessário possuir webcam conectada.

### Windows
- Recomendado utilizar Docker Desktop
- Algumas funções relacionadas à câmera podem variar dependendo da configuração do WSL2
- Recomendado usar Docker Compose

---

# 📂 Estrutura do Projeto

```bash
AFK/
├── assets/
      └── images/
             └── menu/
      └── skins/
             └── teste/
             └── testemult/
├── camera/
├── config/
├── entidades/
├── fisica/
├── jogo/
      └── states/
             └── gameplay/
             └── tela_main/
             └── tela_pre_game/
      └── systems/
├── ui/
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── dockerfile
├── main.py
├── README.md
├── requirements.txt
└── rodar_docker.sh
└── 
```
---
## Desenvolvimento das Sprints:
### 📅 Sprint 1
- Estruturação do repositório no GitHub
- Definição das tecnologias
- Organização inicial do projeto
- Planejamento das próximas etapas
- Início dos estudos com visão computacional

### 📅 Sprint 2
- Implementação do sistema de hand tracking com MediaPipe
- Detecção de duas mãos simultaneamente (direita e esquerda)
- Mapeamento dos 21 landmarks da mão para coordenadas na tela
- Criação de lógica de zona central (área neutra) para evitar movimentos involuntários
- Integração inicial entre o sistema de visão computacional e o jogo em Pygame
- Controle do personagem através de gestos em tempo real
- Ajustes finos na detecção de movimentos para melhorar a precisão
- Uso de Git com versionamento e criação de branch para testes

### 📅 Sprint 3
- Organização e estruturação dos Arquivos do jogo.
- Otimização do código.
- Dockerização e portabilidade com a camêra.

---

## 📌 Status
- Sprint 1 - concluída (✅)
- Sprint 2 - concluída (✅)
- Sprint 3 - em desenvolvimento (🛠️)
- Sprint 4 - planejada 
- Sprint 5 - planejada 

---
