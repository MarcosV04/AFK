def atualizar_camera(fila, pontos_controle, modo_edicao):

    if fila is not None and not fila.empty():

        try:

            while not fila.empty():
                pontos = fila.get_nowait()

            if not modo_edicao and pontos and len(pontos) >= 21:

                escala_x = 2
                escala_y = 1.5

                pontos_controle[0].position = (pontos[4][0] * escala_x, pontos[4][1] * escala_y)
                pontos_controle[1].position = (pontos[8][0] * escala_x, pontos[8][1] * escala_y)
                pontos_controle[2].position = (pontos[12][0] * escala_x, pontos[12][1] * escala_y)
                pontos_controle[3].position = (pontos[16][0] * escala_x, pontos[16][1] * escala_y)
                pontos_controle[4].position = (pontos[20][0] * escala_x, pontos[20][1] * escala_y)


        except Exception as erro:
            print("Erro camera:", erro)