import pygame, sys, os, random

pygame.init()

Mapa_Atual = [ 
            # Terra 
           [
            '000000000000000000000000000000000000000000000000000000000000',
            '000000000000000000000000000000000000000000000000000000000000',
            '000000000000000000000000000000000000000000044000000000000044',
            '444020000000000000004400000000000000004440000000440400004444',
            '111000000000000440000030000000044440000000000000000000001111',
            '110000000044400000000000000000444400000000000004444444001111',
            '114444444444444444444444444444111144444444444441111111444444',
            '111111111111111111111111111111111111111111111111111111111111',
            '111111111111111111111111111111111111111111111111111111111111'],
            # mARTE
            [
            '000000000000000000000000000000000000000000000000000000000000',
            '000000000000000000000000000000000000000000000000000000000000',
            '000000000000000000000000000000000000000000044000000000000044',
            '444020000000000000004400000000000000004440000000440400004444',
            '111000000000000440000000000000044440000000000000000000001111',
            '110000000044400000000003000000444400000300000004444444001111',
            '114444444444444444444444444444111144444444444441111111444444',
            '111111111111111111111111111111111111111111111111111111111111',
            '111111111111111111111111111111111111111111111111111111111111']
]

Mapa_index = 0

TAMANHO_BLOCO = 90
JANELA_LARGURA = 800

GRAVIDADE = 0.75
janela_altura = len(Mapa_Atual[Mapa_index]) * TAMANHO_BLOCO
SCROLL_THRESH = 200
screen_scroll = 0
tela = pygame.display.set_mode((JANELA_LARGURA, janela_altura))

tiro_som = pygame.mixer.Sound("musica\Tiro_som.mp3")
Fundo_som = pygame.mixer.music.load("musica\Jazz.mp3")

sky_img = pygame.image.load(r"img\Bg\0.png")  

relogio = pygame.time.Clock()


Tiro_img = pygame.image.load(r"img\gosma.png")

pygame.mixer.music.set_volume(0.1)


#MUNDO


lista_planetas = ["Terra", "Marte"]
img_blocos = []
  
for planeta in lista_planetas:    
    temp = [] 
    TIPOS_BLOCO = len(os.listdir(f'img//Blocos//{planeta}'))    
    for i in range(1, TIPOS_BLOCO + 1):
        img = pygame.image.load(f'img/Blocos/{planeta}/{i}.png')
        img = pygame.transform.scale(img, (TAMANHO_BLOCO, TAMANHO_BLOCO))
        temp.append(img)
    img_blocos.append(temp)



def texto(texto,tamanho, cor, x, y):
    fonte = pygame.font.SysFont('Futura', tamanho)
    img = fonte.render(texto, True, cor)
    tela.blit(img, (x, y))


def bg():
    
    tela.blit(sky_img, (0, 0))


# ============================================== HP ========================================================
class HP:
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def desenhar(self, hp):
        self.hp = hp
        fracao = self.hp / self.max_hp
        img = pygame.image.load('img/HP.png')

        pygame.draw.rect(tela, pygame.Color("red"), (self.x, self.y, 150, 25))
        pygame.draw.rect(tela, pygame.Color("green"), (self.x, self.y, 150 * fracao, 25))
        tela.blit(img, (0, 10))


# ============================================== Personagem ========================================================

class personagem(pygame.sprite.Sprite):
    def __init__(self, posx, posy, velocidade, tipo):
        pygame.sprite.Sprite.__init__(self)
        global direita_x, esquerda_x

        # AI
        self.ai_contador = 0
        self.Parado = False
        self.ai_Parado_contador = 0
        self.visao = pygame.Rect(0, 0, 150, 20)  # Área detecção do personagem

        # pulo
        self.pulo = False
        self.vel_y = 0
        self.no_ar = False

        #Tiro
        self.tiro_cooldown = 0

        #geral
        self.flip = False
        self.hp = 100
        self.vivo = True
        self.velocidade = velocidade
        self.direcao = 1

        #Animação
        self.tipo = tipo
        self.movimento_status = 0
        self.index = 0
        self.animacao_timer = pygame.time.get_ticks()
        self.animacao = []

        Lista_tipos_Animacao = ["Parado", "Andando" ,  "Pulo" , "Morte"]
        for animation in Lista_tipos_Animacao:
            temp_list = []
            frames = len(os.listdir(f"img/{self.tipo}/{animation}"))
            for i in range(frames):
                image = pygame.image.load(f'img/{self.tipo}/{animation}/{i}.png').convert_alpha()
                temp_list.append(image)

            self.animacao.append(temp_list)

        self.image = self.animacao[self.movimento_status][self.index]
        
        self.rect = pygame.Rect(posx, posy, self.image.get_width(), self.image.get_height())
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.topleft = self.rect.topleft

    def update(self):

        if self.hp <= 0:
            self.hp = 0
            self.velocidade = 0
            self.vivo = False
            self.update_acao(3)  # ADD MORTE DOS (4)
            if self.tipo == "Jogador":
                texto("Fim de Jogo", 50,pygame.Color("red"), janela_altura/2,JANELA_LARGURA/2 -30)
                menu_pricipal()

        if self.tiro_cooldown > 0:
            self.tiro_cooldown -= 1

    def Animacao(self, mov_tipo):
        COOLDONW = 100
        self.movimento_status = mov_tipo

        if pygame.time.get_ticks() - self.animacao_timer > COOLDONW:
            self.image = self.animacao[self.movimento_status][
                self.index % len(self.animacao[self.movimento_status])]
            self.animacao_timer = pygame.time.get_ticks()
            self.index += 1
        if self.index >= len(self.animacao[self.movimento_status]):
            self.index = 0

        self.rect.size = self.image.get_size()

    def Atirar(self):        

      

        if self.tiro_cooldown == 0:
            self.tiro_cooldown = 20
            tiro_som.play()
            tiro = Bala(self.rect.centerx + (0.7 * self.rect.size[0] * self.direcao), self.rect.centery, self.direcao)
            Tiro_Grupo.add(tiro)

    def AI(self):
        global screen_scroll

        self.visao.center = (self.rect.centerx + 70 * self.direcao, self.rect.centery) 

        #pygame.draw.rect(tela, pygame.Color("red"), self.visao)  

        if self.vivo and self.vivo:
            if self.Parado == False and random.randint(1, 200) == 1:
                self.update_acao(0)  # Parado
                self.Parado = True
                self.ai_Parado_contador = 50
            if self.visao.colliderect(Jogador.rect):
                self.update_acao(0)
                self.Atirar()
            else:
                if self.Parado == False:
                    if self.direcao == 1:
                        ai_direita = True
                    else:
                        ai_direita = False
                    ai_esquerda = not ai_direita
                    self.move(ai_direita, ai_esquerda)
                    self.update_acao(1)  #  Andando
                    self.ai_contador += 1

                    if self.ai_contador > TAMANHO_BLOCO:
                        self.direcao *= -1
                        self.ai_contador *= -1


                else:
                    self.ai_Parado_contador -= 1
                    if self.ai_Parado_contador <= 0:
                        self.Parado = False

        self.rect.x += screen_scroll  

    def update_acao(self, nova_acao):
        if nova_acao != self.movimento_status:
            self.movimento_status = nova_acao
            self.index = 0
            self.animacao_timer = pygame.time.get_ticks()

    def move(self, direita_x, esquerda_x):
        global screen_scroll 
        screen_scroll = 0
       
        dx = 0
        dy = 0


        if direita_x :
            dx = self.velocidade
            self.flip = False
            self.direcao = 1
            

        if esquerda_x:
            dx = -self.velocidade
            self.flip = True
            self.direcao = -1
           
 
        if self.pulo:
            self.vel_y = -20
            self.pulo = False
            self.no_ar = True

        self.vel_y += GRAVIDADE
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
       

        self.rect.x += dx

        for bloco in lv1.obstaculos:
            if bloco[1].colliderect(self.rect):
                if dx > 0:  # ta indo pra dir
                    self.rect.right = bloco[1].left
                elif dx < 0:  # esq
                    self.rect.left = bloco[1].right


        self.rect.y += dy

        for bloco in lv1.obstaculos:
            if bloco[1].colliderect(self.rect):
                if dy > 0:  # caindo
                    self.rect.bottom = bloco[1].top
                    self.vel_y = 0
                    self.no_ar = False
                elif dy < 0:  # pulo
                    self.rect.top = bloco[1].bottom
                    self.vel_y = 0

        if self.tipo == "Jogador":
            if self.rect.right > JANELA_LARGURA - SCROLL_THRESH:

                screen_scroll -= self.rect.right - (JANELA_LARGURA - SCROLL_THRESH)
                self.rect.right = JANELA_LARGURA - SCROLL_THRESH
            
            elif self.rect.left < SCROLL_THRESH:
                
                screen_scroll -= self.rect.left - SCROLL_THRESH
                self.rect.left = SCROLL_THRESH

        return screen_scroll



    def desenhar(self):
        tela.blit(pygame.transform.flip(self.animacao[self.movimento_status][self.index], self.flip, False),(self.rect.x, self.rect.y))

        #pygame.draw.rect(tela, (0, 225, 0), self.rect, 2)



# ============================================== LV ========================================================
class Lv:
    def __init__(self):
        self.obstaculos = []

    def mapa(self, layout):


        for indexy, linha in enumerate(layout):
            for indexx, coll in enumerate(linha):
                coll = int(coll)
                x = indexx * TAMANHO_BLOCO
                y = indexy * TAMANHO_BLOCO
                if coll >= 1:
                    img = img_blocos[Mapa_index][coll - 1]
                    img_rect = img.get_rect()
                    img_rect.x = x 
                    img_rect.y = y
                    bloco_data = (img, img_rect)
                    if coll == 1:
                        self.obstaculos.append(bloco_data)
                    elif coll == 2:
                        print(x,y)
                        Jogador = personagem(x, y, 10, "Jogador")
                        Barra_saude = HP(50, 14, Jogador.hp, Jogador.hp)
                    elif coll == 3:
                        
                        pass
                        #Inimigo = personagem(x, y, 3, "Rato")
                        #Inimigos_Grupo.add(Inimigo)
                    elif coll ==  4:
                        self.obstaculos.append(bloco_data)
                    elif coll == 5:
                        self.obstaculos.append(bloco_data)

        return Jogador, Barra_saude

    def draw(self):
        for bloco in self.obstaculos:
            bloco[1].x += screen_scroll 
            tela.blit(bloco[0], bloco[1])

# ============================================== Bala ========================================================
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        pygame.sprite.Sprite.__init__(self)
        self.velocidade = 10
        self.image = Tiro_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direcao = direcao

    def update(self):
        self.rect.x += self.direcao * self.velocidade
        # se saiu da tela     
        if self.rect.right < 0 or self.rect.left > JANELA_LARGURA:
            self.kill()

        for bloco in lv1.obstaculos:
            if bloco[1].colliderect(self.rect):
                self.kill()

        if pygame.sprite.spritecollide(Jogador, Tiro_Grupo, False):
            if Jogador.vivo:
                Jogador.hp -= 30
                self.kill()

        for inimigo in Inimigos_Grupo:
            if pygame.sprite.spritecollide(inimigo, Tiro_Grupo, False):
                if inimigo.vivo:
                    inimigo.hp -= 30
                    self.kill()


# ============================================== Fim Classes ========================================================

Inimigos_Grupo = pygame.sprite.Group()
Tiro_Grupo = pygame.sprite.Group()

# ============================================== Menu Principal ========================================================
def menu_pricipal(): 
        global Mapa_index

        pygame.display.set_caption("Menu")

        start_img = pygame.image.load("img//Menu//start.png")
        menu_texto = pygame.image.load("img//Menu//Menu.png")
        botao_opcoes = pygame.image.load("img//Menu//opcoes.png")
        # image botão
        start_img = pygame.transform.scale(start_img, (190,90))
        botao_opcoes = pygame.transform.scale(botao_opcoes, (190,90))

        marte = pygame.image.load("img//Menu//marte.png")
        terra = pygame.image.load("img//Menu//terra.png")
        marte = pygame.transform.scale(marte, (200,200))
        terra = pygame.transform.scale(terra, (200,200))

        terra_rect = terra.get_rect()
        terra_rect.center = (JANELA_LARGURA / 2 - 200, janela_altura / 2 + 200)

        marte_rect = marte.get_rect()
        marte_rect.center = (JANELA_LARGURA/2 + 200, janela_altura / 2 + 200)

        botao_opcoes_rect = start_img.get_rect()
        botao_opcoes_rect.center = (JANELA_LARGURA / 2, janela_altura / 2 -100)

        start_img_rect = start_img.get_rect()
        start_img_rect.center = (JANELA_LARGURA / 2, janela_altura / 2 - 200)

        tela.fill((126, 152, 130))

        run = True
        while run:

            tela.blit(menu_texto, (JANELA_LARGURA / 2 - menu_texto.get_width() * 0.5, 50))

            # start
            tela.blit(start_img, (start_img_rect.x , start_img_rect.y))
             # opções       
            tela.blit(botao_opcoes, (start_img_rect.x , start_img_rect.y + 110))

            pygame.draw.rect(tela, (1, 100, 1), start_img_rect, 1)
            pygame.draw.rect(tela, (1, 100, 1), marte_rect, 1)
            pygame.draw.rect(tela, (1, 100, 1), terra_rect, 1)


            #texto("Escolha o planeta destino", 30,(0,0,0), )

            tela.blit(marte, (marte_rect.x, marte_rect.y))
            tela.blit(terra, (terra_rect.x, terra_rect.y))


            mods = pygame.key.get_mods()
            pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or mods & pygame.KMOD_CTRL and event.key == pygame.K_w:
                    sys.exit()

            if botao_opcoes_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:   
                    menu_esc()

            if start_img_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:   
                    jogo()


            if marte_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    Mapa_index = 1

 
            if terra_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    Mapa_index = 0
                    


            pygame.display.update()
# ============================================== Menu ========================================================

def menu_esc():
    global tela, JANELA_LARGURA, janela_altura
    pygame.display.set_caption("Opções")
    volume_musica = 0.5
    volume_som = 0.5
    pygame.mixer.music.set_volume(volume_musica)
    tiro_som.set_volume(volume_som)
    tela.fill((126, 152, 130))

    run = True
    while run:

        texto("Opções", 50, (255, 255, 255), JANELA_LARGURA / 2 - 50, 50)

        texto("Volume:", 30, (255, 255, 255), 100, 150)
        
        texto("Volume efeitos sonoros:", 30, (255, 255, 255), 100, 250)
        
        pygame.draw.rect(tela, (0, 0, 0), (400, 150, 300, 50))
        pygame.draw.rect(tela, (0, 255, 0), (400, 150, 300 * volume_musica, 50))

        pygame.draw.rect(tela, (0, 0, 0), (400, 250, 300, 50))
        pygame.draw.rect(tela, (0, 255, 0), (400, 250, 300 * volume_som, 50))

        mods = pygame.key.get_mods()
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or mods & pygame.KMOD_CTRL and event.key == pygame.K_w:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_pricipal()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 400 <= pos[0] <= 700:
                    if 150 <= pos[1] <= 200:
                        volume_musica = (pos[0] - 400) / 300
                        pygame.mixer.music.set_volume(volume_musica)
                    if 250 <= pos[1] <= 300:
                        volume_som = (pos[0] - 400) / 300
                        tiro_som.set_volume(volume_som)
                    if 350 <= pos[1] <= 400:
                        escala = (pos[0] - 400) / 300
                        JANELA_LARGURA = int(800 * escala)
                        JANELA_ALTURA = int(600 * escala)
                        tela = pygame.display.set_mode((JANELA_LARGURA, JANELA_ALTURA))

        pygame.display.update()

# ============================================== Jogo ========================================================
def jogo():
    global Jogador, Barra_saude, lv1
    pygame.display.set_caption("Jogo")
    run = True
    direita_x = False
    esquerda_x = False
    Tiro = False  
    lv1 = Lv()

    Inimigo2 = personagem(30,70, 3, "Rato")
    Inimigos_Grupo.add(Inimigo2)

    Jogador, Barra_saude = lv1.mapa(Mapa_Atual[Mapa_index])
    pygame.mixer.music.play(1)
    tela.fill(pygame.Color("white"))

    while run:
        relogio.tick(60)
        
        bg() 

        texto(f'Tiro cooldown:{Jogador.tiro_cooldown}', 30, (0, 255, 255), 30, 70)

        for Inimigo in Inimigos_Grupo:
            Inimigo.AI()
            Inimigo.update()
            Inimigo.desenhar()
            
        Tiro_Grupo.update()
        print(Inimigos_Grupo)


        # Jogador
        Barra_saude.desenhar(Jogador.hp)
        Jogador.update()

        if Jogador.vivo:
            if Tiro:
                Jogador.Atirar()
            if Jogador.no_ar:
                Jogador.Animacao(2)
            elif direita_x or esquerda_x:
                Jogador.Animacao(1)
            else:
                Jogador.Animacao(0)

            screen_scroll = Jogador.move(direita_x, esquerda_x)
            #bg_scroll -= screen_scroll 
        

        lv1.draw()  
        Tiro_Grupo.draw(tela)

        
        tela.blit(pygame.transform.flip(Jogador.image, Jogador.flip, False), Jogador.rect)

        pygame.draw.rect(tela, (0, 225, 0), Jogador.rect, 2)  
        mods = pygame.key.get_mods()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (mods & pygame.KMOD_CTRL and event.key == pygame.K_w):
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    direita_x = True
                if event.key == pygame.K_a:
                    esquerda_x = True
                if event.key == pygame.K_SPACE and not Jogador.no_ar:
                    Jogador.pulo = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    direita_x = False
                if event.key == pygame.K_a:
                    esquerda_x = False
                if event.key == pygame.K_ESCAPE:
                    menu_esc()

            if event.type == pygame.MOUSEBUTTONDOWN:
                Tiro = True
            if event.type == pygame.MOUSEBUTTONUP:
                Tiro = False

        pygame.display.update()


menu_pricipal()


# https://www.youtube.com/watch?v=JTM8_pcQOUU&list=PLjcN1EyupaQm20hlUE11y9y8EY2aXLpnv&index=11

# o mano 2
# https://www.youtube.com/watch?v=YWN8GcmJ-jA&list=PL8ui5HK3oSiGXM2Pc2DahNu1xXBf7WQh-&index=3
