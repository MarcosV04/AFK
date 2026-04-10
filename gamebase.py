import pygame
import pymunk
import pymunk.pygame_util
import math

# --- Configurações Iniciais ---

def jogo():
    pygame.init()
    LARGURA, ALTURA = 1280, 720
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("🎭 AFK - Away From the Keyboard")
    relogio = pygame.time.Clock()

    # --- Configuração da Física (Pymunk) ---   
    espaco = pymunk.Space() 
    espaco.gravity = (0, 981)   
    opcoes_desenho  = pymunk.pygame_util.DrawOptions(tela)   

    # --- Funções p ara criar objetos ---    
    def criar_chao( espaco): 
        chao_body =  es  paco.static_body  
        chao_shape  = p  ymunk.Segment(chao_body, (0, ALTURA - 50), (LARGURA, ALTURA    - 50), 5)
        chao_shape. fri  ction = 1.0   
        espaco.add( cha  o_shape)  

    def criar_bloco (es  paco, x, y, largura, altura, massa=10):   
        momento = p ymu  nk.moment_for_box(massa, (largura, altura))   
        corpo = pym unk  .Body(massa, momento) 
        corpo.posit ion   = x, y   
        forma = pym unk  .Poly.create_box(corpo, (largura, altura))    
        forma.frict ion   = 0.5    
        forma.elast ici  ty = 0.3  
        espaco.add( cor  po, forma)    
        return form a    

    def criar_esfer a(e  spaco,     x, y, raio, massa=10): 
        momento = p ymu  nk.mom    ent_for_circle(massa, 0, raio, (0, 0))  
        corpo = pym unk  .Body(    massa, momento) 
        corpo.posit ion   = x,     y   
        forma = pym unk  .Circl    e(corpo, raio)  
        forma.frict ion   = 0.5    
        forma.elast ici  ty = 0    .3  
        espaco.add( cor  po, fo    rma)    
        return form a    

    def criar_corda (es  paco,     corpo_a, corpo_b, ancora_a, ancora_b, c omprimento): 
        corda = pym unk  .Slide    Joint(corpo_a, corpo_b, ancora_a, ancor a_b, 0, compri   mento)
        espaco.add( cor  da)   
        return cord a    

    # --- NOVO: Cri and  o os 5     Pontos de Controle     (Cinemáticos) ---   
    pontos_controle  =   []    
    for i in range( 5):  
        # Body_type  KI  NEMATI    C faz com que ignore     gravidade e forças 
        corpo = pym unk  .Body(    body_type=pymunk.Bod    y.KINEMATIC)    
        corpo.posit ion   = ((L    ARGURA // 2) - 200 +     (i * 100), 150)    
        forma = pym unk  .Circl    e(corpo, 15)    
        forma.color  =   (0, 10    0, 255, 255)     # Azul     para identificar    
        forma.senso r =   True     # Para não "    atropela    r" os blocos fisica mente se você    não quiser
        espaco.add( cor  po, fo    rma)    
        pontos_cont rol  e.appe    nd(corpo)   

    # Criar o cenár io   e bone    co  
    criar_chao(espa co)  
    def criar_bonec o()  : 
        torco = cri ar_  bloco(    espaco, LARG    URA // 2    , 200, 75, 90)  
        cabeca = cr iar  _bloco    (espaco, LAR    GURA //     2 , 90, 80, 80) 
        bresq = cri ar_  bloco(    espaco, LARG    URA // 2     - 50, 200, 25, 50)      
        antesq = cr iar  _bloco    (espaco, LAR    GURA //     2 - 50, 275, 25, 50 )    
        bradir = cr iar  _bloco    (espaco, LAR    GURA //     2 + 50, 200, 25, 50 )    
        antdir = cr iar  _bloco    (espaco, LAR    GURA //     2 + 50, 275, 25, 50 )    
        peresq = cr iar  _bloco    (espaco, LAR    GURA //     2 - 25, 325, 25, 50 )    
        panesq = cr iar  _bloco    (espaco, LAR    GURA //     2 - 25, 400, 25, 50 )    
        perdir = cr iar  _bloco    (espaco, LAR    GURA //     2 + 25, 325, 25, 50 )    
        pandir = cr iar  _bloco    (espaco, LAR    GURA //     2 + 25, 400, 25, 50 )    
        cintura = c ria  r_bloc    o(espaco, LA    RGURA //     2, 250, 75, 35)    
        criar_corda (es  paco,     torco.body,     cabeca.b    ody, (0, -45), (0,  40), 25) 
        criar_corda (es  paco,     torco.body,     bresq.bo    dy, (-37.5, -30), ( 0, -25), 20) 
        criar_corda (es  paco,     bresq.body,     antesq.b    ody, (0, 25), (0, - 25), 25) 
        criar_corda (es  paco,     torco.body,     bradir.b    ody, (37.5, -30), ( 0, -25), 20) 
        criar_corda (es  paco,     bradir.body,     antdir.    body, (0, 25), (0,  -25), 25)    
        criar_corda (es  paco,     torco.body,     cintura.    body, (0, 45), (0,  -17.5), 25)  
        criar_corda (es  paco,     cintura.body    , peresq    .body, (-25, 17.5),  (0, -25), 25)   
        criar_corda (es  paco,     peresq.body,     panesq.    body, (0, 25), (0,  -25), 25)    
        criar_corda (es  paco,     cintura.body    , perdir    .body, (25, 17.5),  (0, -25), 25)    
        criar_corda (es  paco,     perdir.body,     pandir.    body, (0, 25), (0,  -25), 25)    
        criar_corda (es  paco,     pontos_contr    ole[2],     cabeca.body, (0, 0) , (0, -40), 10   0)
        criar_corda (es  paco,     pontos_contr    ole[0],     antesq.body, (0, 0) , (0, 25), 300   )
        criar_corda (es  paco,     pontos_contr    ole[4],     antdir.body, (0, 0) , (0, 25), 300   )
        criar_corda (es  paco,     pontos_contr    ole[1],     peresq.body, (0, 0) , (0, 25), 450   )
        criar_corda (es  paco,     pontos_contr    ole[3],     perdir.body, (0, 0) , (0, 25), 450   )
    criar_boneco()  
    #criar_esfera(e spa  co, LA    RGURA // 2 +     200, 10    0, 50, 100) # Bola  para interagir   
    criar_bloco(esp aco  , LARG    URA // 2 + 2    00, 100,     20, 100, 50) # Blo co para intera   gir

    # Variáveis par a i  nteraç    ão com o mou    se  
    mouse_body = py mun  k.Body    (body_type=p    ymunk.  Bo    dy.KINEMATIC)   
    mouse_joint = N one  

    # Variáveis para c  riação     da corda   
    corpo_corda_a = No  ne    
    ancora_a_local = N  one   

    # Variáveis de interação    
    mouse_body = pymunk.Body    (body_type=p    ymun    k.  Bo    dy.KINEMATIC)   
    mouse_joint = None  
    ponto_arrastando = None     # Armazena q    ual     po  nt    o azul estamos move ndo  

    rodando = True  
    while rodando:  
        tela.fill((240, 240,     240)) # Fun    do c    in  za     claro  
        mouse_pos = pygame.m    ouse.get_pos    ()  

        for evento in pygame    .event.get()    :   
            if evento.type =    = pygame.QUI    T:  
                rodando = Fa    lse 

            # --- PEGAR BLOCOS COM O MOU    SE -    --  
            elif evento.type == pygame.M    OUSE    BU  TT    ONDOWN: 
                if evento.button == 1:  
                    info = espaco.point_    quer    y_  ne    arest(mouse_pos, 0, pymunk  .ShapeFilter())
                    if info and info.sha    pe: 
                        corpo_clicado =     info    .s  ha    pe.body 
                        # Se for um dos     noss    os   p    ontos azuis (Kinematic) 
                        if corpo_clicado     in     po  nt    os_controle:    
                            ponto_arra  st    ando     =   c    orpo_clicado    
                        # Se for um bl  oc    o no    rm  al     (Dynamic)  
                        elif corpo_cli  ca    do.b    od  y_    type == pymunk.Body.DYNAMI  C:
                            mouse_body  .p    osit    io  n     = mouse_pos 
                            mouse_join  t     = py    mu  nk    .PivotJoint(mouse_body, co  rpo_clicado, mouse_po s)
                            mouse_join  t.    max_    fo  rc    e = 250000  
                            espaco.add  (m    ouse    _j  oi    nt) 

            elif evento.type == pygame  .M    OUSE    BU  TTONUP:   
                if evento.button == 1:  
                    if mouse_joint: 
                        espaco.remove(  mo    use_    jo  int)  
                        mouse_joint =   No    ne  
                    ponto_arrastando =   N    one 

            # --- TECLAS DE ATALHO ---  
            elif evento.type == pygame  .K    EYDO    WN  : 
                info_hover = espaco.po  in    t_qu    er  y_nearest(mouse_pos, 0, p ymu  nk.ShapeFilter()) 

                # TECLA 'R': Criar Cor  da    
                if ev   ento.key == pygam  e.    K_r:    
                    i   f info_hover: # P  od    e pr    eg  ar no chão (estático) ou  blo  cos (dinâmico)    
                             corpo_alvo = i  nf    o_ho    ve  r.shape.body  

                             if corpo_corda  _a     is     No  ne:   
                                 # Primeiro   c    liqu    e:   define o ponto A 
                                 corpo_cord  a_    a =     co  rpo_alvo  
                                 # Guarda a   p    osiç    ão   relativa do clique dentr o d  o bloco   
                                 ancora_a_l  oc    al =     c  orpo_alvo.world_to_local( mou  se_pos)   
                                 print("Pon  to     1 d    a   corda fixado! Aperte 'R'  em   outro lugar para amar rar.")   
                             else:   
                                 # Segundo   cl    ique    :   define o ponto B e cria a  co  rda   
                                 corpo_b =   co    rpo_    al  vo    
                                 ancora_b_l  oc    al =     c  orpo_b.world_to_local(mou se_  pos)  

                                 # Descobri  r     a po    si  ção atual dos dois pontos  no   mundo para calcular  o tamanho    
                                 pos_a_mund  o     = co    rp  o_corda_a.local_to_world( anc  ora_a_local)  
                                 pos_b_mund  o     = co    rp  o_b.local_to_world(ancora _b_  local)    

                                 # Teorema   de     Pit    ág  oras para saber o comprim ent  o inicial da corda    
                                 dx = pos_b  _m    undo    [0  ] - pos_a_mundo[0]    
                                 dy = pos_b  _m    undo    [1  ] - pos_a_mundo[1]    
                                 distancia   =     math    .s  qrt(dx**2 + dy**2)    

                                 # Criar a   Sl    ideJ    oi  nt (min: 0, max: distanci a)   
                                 corda = py  mu    nk.S    li  deJoint(corpo_corda_a, co rpo  _b, ancora_a_local, a ncora_b_local, 0,    distancia)
                                 espaco.add  (c    orda    )   
                                 print("Cor  da     cri    ad  a!")  

                                 # Resetar   pa    ra a     p  róxima corda  
                                 corpo_cord  a_    a =     No  ne    
                                 ancora_a_l  oc    al =     N  one   

                  elif    info_hover and in  fo    _hov    er.shape.body.body_type ==  pym  unk.Body.DYNAMIC: 
                      #    TECLA 'P': Prega  r     (Pin     estático)  
                      i   f evento.key == p  yg    ame.    K_p:    
                             pino = pymunk.  Pi    votJ    oint(info_hover.shape.body,  es  paco.static_body, mou se_pos)  
                             espaco.add(pin  o)    
                             print("Bloco p  re    gado    !") 

                      #    TECLA 'C': Alter  na    r Colisão   
                      e   lif evento.key ==   p    ygame.K_c:  
                             info_hover.sha  pe    .sensor = not info_hover.shape. sen  sor   

        # ---   Lógica    de Movimentação -  --    
        # Se e  stiver    arrastando um pon  to     azul, a posição dele é setada  manualmente  
        if pon  to_arra   stando:    
            po  nto_arr   astando.position   =     mouse_pos   

        # Se e  stiver    arrastando um blo  co    , a junta cuida da física   
        if mou  se_join   t: 
            mo  use_bod   y.position = mous  e_    pos 

        # Atua  liza a    posição do mouse   
        if mou  se_join   t: 
            mo  use_bod   y.position = mous  e_    pos 

        # ---   Passo d   a Física ---   
        espaco  .step(1    / 60.0)   

        # ---   Desenho    ---   
        espaco  .debug_   draw(opcoes_desen  ho)   

        # Visu  al extr   a para os pontos de controle (Blue Glow)   
        for p   in pont   os_controle:   
            py  game.dr   aw.circle(tela, (0, 100, 255), (int(p.position.x),  int(p.position.y)), 15,  2)  

        # Dese  nhar um   a linha vermelha de "pré-visualização" se o jogado r estiver criando uma corda  
        if cor  po_cord   a_a is not None:   
            #   Pega on   de o ponto A está agora (caso o bloco tenha caído  enquanto o jogador move o mouse) 
            po  s_atual   _a = corpo_corda_a.local_to_world(ancora_a_local)  
            py  game.dr   aw.line(tela, (255, 0, 0), pos_atual_a, mouse_pos,  2)  

        # Inst  ruções    
        fonte   = pygam   e.font.SysFont(None, 24)   
        tela.b  lit(fon   te.render("Clique Esquerdo: Pegar bloco", True, (0,0,0)), (10, 10))    
        #tela.  blit(fo   nte.render("Mouse + 'P': Colocar um Prego fixo", True, (0,0,0)), (10, 30)) 
        #tela.  blit(fo   nte.render("Mouse + 'C': Ligar/Desligar colisão", True, (0,0,0)), (10, 50))    
        #tela.  blit(fo   nte.render("Mouse + 'R': Ponto 1 da Corda -> Mouse + 'R': Ponto 2", True, (0,0,200)), (10, 7   0))

        pygame  .displa   y.flip()
        relogi  o.tick(   60)

    pygame.qui  t()

jogo()