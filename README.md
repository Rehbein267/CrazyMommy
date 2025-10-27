# 🎮 Crazy Mommy — Versão Final (Projeto de Graduação)

🧠 **Crazy Mommy** é um jogo 2D desenvolvido em **Python + Pygame**, criado como trabalho da disciplina Linguagem de Programação Aplicada no curso de **Análise e Desenvolvimento de Sistemas** no Centro Universitário **Uninter**.

Nesta versão final, o jogo apresenta três fases completas, com movimentação fluida, colisões, sons, HUD dinâmico e transições entre níveis.
Foi desenvolvido de forma modular e com boas práticas de organização de código, separando lógica de jogo, interface e assets.

---

## 💡 Objetivo do Projeto

O projeto teve como propósito:

- Implementar um **jogo interativo e funcional**, utilizando a linguagem Python e a biblioteca Pygame.
- Explorar **conceitos de orientação a objetos**, eventos, colisões e física básica.
- Aplicar **padrões de design**, modularização e reutilização de código.
- Demonstrar **autonomia técnica e criativa** no desenvolvimento de software.

---

## 🧩 Estrutura do Projeto (Simplificada)

CrazyMommy/
│
├── assets/
│ ├── images/ # Cenários, personagens, sprites, HUD
│ └── sounds/ # Efeitos sonoros e trilhas
│
├── src/
│ ├── main.py # Arquivo principal — inicia o jogo
│ ├── menu.py # Menu inicial
│ ├── level1.py # Fase 1 — introdução
│ ├── level2.py # Fase 2 — desafio intermediário
│ ├── level3.py # Fase 3 — obstáculos e IA
│ ├── characters.py # Classes da Mãe e inimigos
│ ├── flipflop.py # Mecânica do chinelo (arma)
│ ├── hud.py # Sistema de barras de vida e tempo
│ ├── explosion.py # Efeitos de vitória e colisão
│ └── settings.py # Configurações globais do jogo
│
└── README.md

---

## 🕹️ Como jogar

1. Instale as dependências:
   ```bash
   pip install pygame
	```
2. Execute o jogo:
```
    python3 src/main.py
```
3. Controles:

- ← / → mover

- ↑ pular

- Espaço lançar o chinelo 🩴

- ESC para sair

## ⚙️ Tecnologias utilizadas

- Python 3.12

- Pygame 2.6

- VS Code / Linux

- Boas práticas de OOP, modularização e uso de assets externos

## 📊 Status do Projeto

- ✅ Versão estável e finalizada
- 💻 Código otimizado e organizado em módulos
- 📦 Disponível para uso acadêmico e demonstrações

## 🤝 Contribuições

Contribuições são bem-vindas!
Se desejar sugerir melhorias, abra uma issue ou envie um pull request com sua proposta.

## ⚠️ Direitos Autorais

© 2025 Jane Rehbein Matias
Centro Universitário Uninter — Curso de Análise e Desenvolvimento de Sistemas

## 🧩 Uso autorizado apenas para fins acadêmicos e colaborativos.
Proibida a cópia ou redistribuição sem autorização da autora.
Créditos devem ser mantidos e reconhecidos em qualquer derivação do projeto.
