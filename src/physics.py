from curses.ascii import alt
import pymunk

def criar_bola(espaco, posicao, raio=20, massa=1):
    inercia = pymunk.moment_for_circle(massa,0,raio)
    corpo = pymunk.Body(massa, inercia)
    corpo.position = posicao
    forma = pymunk.Circle(corpo,raio)
    forma.elasticity = 0.8
    espaco.add(corpo,forma)
    return corpo

def criar_caixa (espaco, posicao, largura=40, altura=40, massa=5):
      # Calcula o momento de inércia da caixa (como ela reage à rotação)
    inercia = pymunk.moment_for_box(massa, (largura, altura))

     # Cria o corpo da caixa — tem massa e pode se mover
    corpo = pymunk.Body(massa,inercia)
    corpo.position = posicao # posição inicial no mundo (x, y)

    # Cria a forma visível (colisão) da caixa
    forma = pymunk.Poly.create_box (corpo, (largura, altura))
    forma.elasticity = 0.4 # quanto ela "quica" quando bate
    forma.friction = 0.8    # atrito (para não deslizar demais)

    # Adiciona a caixa ao espaço físico
    espaco.add(corpo, forma)
    return corpo

