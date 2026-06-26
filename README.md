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

---

## ⚙️ Funcionalidades Implementadas

### 👁️ Visão Computacional
## 👁️ Visão Computacional
- Captura de vídeo em tempo real
- Detecção das mãos simultaneamente
- Rastreamento dos 21 pontos da mão (landmarks)
@@ -53,18 +51,155 @@ O ambiente será um **palco**, com desafios progressivos:

---

## Desenvolvimento das Sprints:
## ⚙️ Como Executar o Projeto

### 📅 Sprint 1
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
```bash
AFK/
├── assets/
      └── images/
             └── menu/
      └── mapas/
      └── skins/
            └── elias/
            └── teste/
            └── testemult/  
      └── sons/
            └── musica/ 
      └── texturas/
            └── skins/
            └── teste/
            └── testemult/
├── camera/
├── core/
├── entidade/
├── fisica/
├── jogo/
      └── states/
             └── gameplay/
             └── tela_main/
             └── tela_pre_game/
      └── systems/
├── ui/
├── dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── README.md
├── docker-compose.yml
├── dockerfile
├── main.py
├── requirements.txt
└── rodar_docker.sh
```
---
