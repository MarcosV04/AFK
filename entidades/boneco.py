from fisica.mundo import criar_bloco, criar_corda

def criar_boneco(espaco, pontos_controle, largura):
        
    #corpo do boneco
    torco = criar_bloco(espaco, largura // 2, 200, 75, 90)
    cabeca = criar_bloco(espaco, largura // 2, 90, 80, 80)
    bresq = criar_bloco(espaco, largura // 2 - 50, 200, 25, 50)
    antesq = criar_bloco(espaco, largura // 2 - 50, 275, 25, 50)
    bradir = criar_bloco(espaco, largura // 2 + 50, 200, 25, 50)
    antdir = criar_bloco(espaco, largura // 2 + 50, 275, 25, 50)
    peresq = criar_bloco(espaco, largura // 2 - 25, 325, 25, 50)
    panesq = criar_bloco(espaco, largura // 2 - 25, 400, 25, 50)
    perdir = criar_bloco(espaco, largura // 2 + 25, 325, 25, 50)
    pandir = criar_bloco(espaco, largura // 2 + 25, 400, 25, 50)
    cintura = criar_bloco(espaco, largura // 2, 250, 75, 35)
    
    #cordas do boneco
    criar_corda(espaco, torco.body, cabeca.body, (0, -45), (0, 40), 25)
    criar_corda(espaco, torco.body, bresq.body, (-37.5, -30), (0, -25), 20)
    criar_corda(espaco, bresq.body, antesq.body, (0, 25), (0, -25), 25)
    criar_corda(espaco, torco.body, bradir.body, (37.5, -30), (0, -25), 20)
    criar_corda(espaco, bradir.body, antdir.body, (0, 25), (0, -25), 25)
    criar_corda(espaco, torco.body, cintura.body, (0, 45), (0, -17.5), 15)
    criar_corda(espaco, cintura.body, peresq.body, (-25, 17.5), (0, -25), 25)
    criar_corda(espaco, peresq.body, panesq.body, (0, 25), (0, -25), 25)
    criar_corda(espaco, cintura.body, perdir.body, (25, 17.5), (0, -25), 25)
    criar_corda(espaco, perdir.body, pandir.body, (0, 25), (0, -25), 25)
    criar_corda(espaco, pontos_controle[2], cabeca.body, (0, 0), (0, -40), 100)
    criar_corda(espaco, pontos_controle[0], antesq.body, (0, 0), (0, 25), 150)
    criar_corda(espaco, pontos_controle[4], antdir.body, (0, 0), (0, 25), 150)
    criar_corda(espaco, pontos_controle[1], peresq.body, (0, 0), (0, 25), 400)
    criar_corda(espaco, pontos_controle[3], perdir.body, (0, 0), (0, 25), 400)

    return {
        "cabeca": cabeca,
        "torco": torco,
        "bresq": bresq,
        "antesq": antesq,
        "bradir": bradir,
        "antdir": antdir,
        "peresq": peresq,
        "panesq": panesq,
        "perdir": perdir,
        "pandir": pandir,
        "cintura": cintura
    }