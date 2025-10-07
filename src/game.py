import pygame
import pymunk
import pymunk.pygame_util

from settings import WIDTH, HEIGHT, FPS, GRAVITY
from physics import criar_bola, criar_caixa

def rodar_jogo():
    #Inicialização do Jogo
    pygame.init()
    tela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Crazy Mommy")  # título da janela
    clock = pygame.time.Clock()

#Criação do espaço fisico
    espaco = pymunk.Space()
    espaco.gravity = GRAVITY
    desenhador = pymunk.pygame_util.DrawOptions(tela)

   #Criação do chão
    chao = pymunk.Segment(espaco.static_body, (0, HEIGHT - 20), (WIDTH, HEIGHT - 20), 5)
    chao.elasticity = 0.8
    espaco.add(chao)


# =========================================
# 🟫 Criação das caixas (obstáculos)
# =========================================
    caixas = []  # lista para armazenar as caixas criadas
    pos_y_base = HEIGHT - 60  # altura da base das torres

# Criar duas torres
    for torre in range(2):
        x = 400 + torre * 100  # torre 1 = x=400, torre 2 = x=500
        for i in range(3):# Empilhar 3 caixas em cada torre
            caixa = criar_caixa(espaco, (x, pos_y_base - i * 45))
            caixas.append(caixa)


    bola = None
    pos_inicial = (100,300) #Ponto fixo estilingue
    arrastando = False
    rodando = True



     # 🌀 Loop principal do jogo
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            #  Pressionar o mouse: cria a bola e começa o arrasto
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if bola is None:
                    bola = criar_bola(espaco, pos_inicial)
                    arrastando = True

            #  Soltar o mouse: lança a bola
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                 # só executa se o jogador estava arrastando e a bola já existe
                if arrastando and bola is not None:
                    # captura a posição atual do mouse no momento em que ele é solto
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # calcula a diferença entre o ponto inicial do estilingue e o ponto final do arrasto
                    # isso cria um "vetor de força" que indica direção e intensidade
                    forca_x = pos_inicial[0] - mouse_x # quanto puxou horizontalmente
                    forca_y = pos_inicial[1] - mouse_y# quanto puxou verticalmente
                    # aplica um impulso instantâneo na bola, proporcional ao arrasto
                    # quanto mais você arrastar o mouse para trás, mais forte será o lançamento
                    # o fator *5 é um multiplicador que ajusta a potência (você pode mudar)
                    bola.apply_impulse_at_local_point((forca_x * 5, forca_y * 5))

                    arrastando = False # desativa o modo de arrasto, voltando ao estado normal do jogo


        tela.fill((255, 255, 255))        # fundo branco
         # desenha o elástico do estilingue
        if arrastando:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(tela, (255, 0, 0), pos_inicial, mouse_pos, 2)

        espaco.step(1 / FPS)              # atualiza física
        espaco.debug_draw(desenhador)     # desenha os objetos
        pygame.display.flip()             # atualiza tela
        clock.tick(FPS)


    pygame.quit()
