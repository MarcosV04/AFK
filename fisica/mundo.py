import pymunk

def criar_chao(espaco, largura, altura):

    chao = pymunk.Segment(espaco.static_body, (0, altura - 50), (largura, altura - 50), 5)
    chao.friction = 1.0

    espaco.add(chao)

def criar_bloco(espaco, x, y, largura, altura, massa=10):

    momento = pymunk.moment_for_box(massa, (largura, altura))
    corpo = pymunk.Body(massa, momento)
    corpo.position = x, y
    forma = pymunk.Poly.create_box(corpo, (largura, altura))
    forma.friction = 0.5
    forma.elasticity = 0.3

    espaco.add(corpo, forma)
    
    return forma

    
    
def criar_corda(espaco, corpo_a, corpo_b, ancora_a, ancora_b, comprimento):

    corda = pymunk.SlideJoint(corpo_a, corpo_b, ancora_a, ancora_b, 0, comprimento)

    espaco.add(corda)

    return corda

