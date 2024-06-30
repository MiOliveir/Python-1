import pygame, sys, os, random

pygame.init()

LV_1 = ['000000000000000000000000000000000000000000000000000000000000',
        '000000000000000000000000000000000000000000000000000000000000',
        '000000000000000000000000000000000000000000000000000000000000',
        '110000001100000001100000000000110000001100000001100000000000',
        '110000000000000003000000000000110000000000000003000000000000',
        '111100000011100000111000000000111100000011100000111000000000',
        '111100000011100000000000000000111100000011100000000000000000',
        '11020000301110000011000000000011000000011100000110000000000',
        '000011100000011100000000000000000011100000011100000000000000',
        '011011111110000011100000000000011011111110000011100000000000',
        '111111110111111100111111110000111111110111111100111111110000']

JANELA_LARGURA = 800
TAMANHO_BLOCO = 64
janela_altura = len(LV_1) * TAMANHO_BLOCO

tela = pygame.display.set_mode((JANELA_LARGURA, janela_altura))
relogio = pygame.time.Clock()

#MUNDO


screen_scroll = 0
bg_scroll = 0


TIPOS_BLOCO = len(os.listdir(f'img/Blocos'))

img_blocos = []
for i in range(1, TIPOS_BLOCO + 1):
    img = pygame.image.load(f'img/Blocos/{i}.png')
    img = pygame.transform.scale(img, (TAMANHO_BLOCO, TAMANHO_BLOCO))
    img_blocos.append(img)

fonte = pygame.font.SysFont('Futura', 30)


def texto(texto, fonte, cor, x, y):
    img = fonte.render(texto, True, cor)
    tela.blit(img, (x, y))


def bg():
    tela.fill(pygame.Color("green"))
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

        Lista_tipos_Animacao = ["Parado", "Andando"]  # "Pulo" + "Morte"
        for animation in Lista_tipos_Animacao:
            temp_list = []
            frames = len(os.listdir(f"img/{self.tipo}/{animation}"))
            for i in range(frames):
                image = pygame.image.load(f'img/{tipo}/{animation}/{i}.png').convert_alpha()
                temp_list.append(image)

            self.animacao.append(temp_list)

        self.image = self.animacao[self.movimento_status][self.index]
        self.rect = pygame.Rect(posx, posy, self.image.get_width(), self.image.get_height())
        self.rect.center = (posx, posy)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):

        if self.hp <= 0:
            self.hp = 0
            self.velocidade = 0
            self.vivo = False
            self.update_acao(1)  # ADD MORTE DOS (4)  

        if self.tiro_cooldown > 0:
            self.tiro_cooldown -= 1

    def move(self, direita_x, esquerda_x):
        # Variação do x e y  
        screen_scroll = 0
        dx = 0
        dy = 0
        

        if direita_x:
            dx = self.velocidade
            self.flip = False
            self.direcao = 1

        if esquerda_x:
            dx = -self.velocidade
            self.flip = True
            self.direcao = -1

        if self.pulo == True and not self.no_ar:
            self.vel_y = -11
            self.pulo = False
            self.no_ar = True

        self.vel_y += GRAVIDADE
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        for bloco in lv1.obstaculos:
            if bloco[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == 'Rato':
                    self.direction *= -1
                    self.ai_contador = 0
            if bloco[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = bloco[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.no_ar = False
                    dy = bloco[1].top - self.rect.bottom

      

      
        self.rect.x += dx
        self.rect.y += dy

      

    def Animacao(self, mov_tipo):
        COOLDONW = 100
        self.movimento_status = mov_tipo

        if mov_tipo == self.pulo:
            if pygame.time.get_ticks() - self.animacao_timer > COOLDONW:
                self.image = self.animacao[self.movimento_status][
                    self.index % len(self.animacao[self.movimento_status])]
                self.animacao_timer = pygame.time.get_ticks()
                self.index += 1
            if self.index >= len(self.animacao[self.movimento_status]):
                self.index = 0

    def Atirar(self):

        if self.tiro_cooldown == 0:
            self.tiro_cooldown = 20
            tiro = Bala(self.rect.centerx + (0.7 * self.rect.size[0] * self.direcao), self.rect.centery, self.direcao)
            Tiro_Grupo.add(tiro)

    def AI(self):

        # Detecção do jogador
        self.visao.center = (self.rect.centerx + 70 * self.direcao, self.rect.centery)  # Posição área de detecção

        pygame.draw.rect(tela, pygame.Color("red"), self.visao)  # Área de detecção visivel

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

            self.rect.x += tl_rolagem

    def update_acao(self, nova_acao):
        if nova_acao != self.movimento_status:
            self.movimento_status = nova_acao
            self.index = 0
            self.animacao_timer = pygame.time.get_ticks()

    

    def desenhar(self):
        tela.blit(pygame.transform.flip(self.animacao[self.movimento_status][self.index], self.flip, False), self.rect)

        pygame.draw.rect(tela, (0, 225, 0), self.rect, 2)


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
                    img = img_blocos[coll - 1]
                    img_rect = img.get_rect()
                    img_rect.x = x
                    img_rect.y = y
                    bloco_data = (img, img_rect)
                    if coll == 1:
                        self.obstaculos.append(bloco_data)
                    elif coll == 2:
                        Jogador = personagem(x, y, 10, "Jogador")
                        Barra_saude = HP(50, 14, Jogador.hp, Jogador.hp)
                    elif coll == 3:
                        Inimigo = personagem(x, y, 5, "Rato")
                        Inimigos_Grupo.add(Inimigo)
                    elif coll == 4:
                        pass  # paradas n interagiveis (geradores)

        return Jogador, Barra_saude


    def draw(self):
        for bloco in self.obstaculos:
            bloco[1].x -= tl_rolagem
            tela.blit(bloco[0], (bloco[1].x, bloco[1].y))
            print(tl_rolagem)


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
                Jogador.hp -= 1
                self.kill()

        for inimigo in Inimigos_Grupo:
            if pygame.sprite.spritecollide(inimigo, Tiro_Grupo, False):
                if inimigo.vivo:
                    inimigo.hp -= 50
                    self.kill()


# ============================================== Fim Classes ========================================================

ROLAGEM_LIMITE = 200
GRAVIDADE = 0.75

tl_rolagem = 0

sky_img = pygame.image.load(r"img\Bg\0.png")
Tiro_img = pygame.image.load(r"img\gosma.png")

Inimigos_Grupo = pygame.sprite.Group()
Tiro_Grupo = pygame.sprite.Group()

lv1 = Lv()

Jogador, Barra_saude = lv1.mapa(LV_1)


# ============================================== Menu ========================================================

def menu():
    pygame.display.set_caption("Menu")

    menu_texto = pygame.image.load("img//Menu.png").convert_alpha()
    botao_img = pygame.image.load("img//Botao.png").convert_alpha()  # image botão

    botao_img_rect = botao_img.get_rect()
    botao_img_rect.center = (JANELA_LARGURA / 2, janela_altura / 2)
    tela.fill(pygame.Color("gray"))

    run = True
    while run:

        tela.blit(menu_texto, (JANELA_LARGURA / 2 - menu_texto.get_width() * 0.5, 0))

        tela.blit(botao_img, (botao_img_rect.x, botao_img_rect.y))

        pygame.draw.rect(tela, (1, 100, 1), botao_img_rect, 1)

        mods = pygame.key.get_mods()
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or mods & pygame.KMOD_CTRL and event.key == pygame.K_w:
                sys.exit()

        if botao_img_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                jogo()

        pygame.display.update()


# ============================================== Jogo ========================================================

def jogo():
    pygame.display.set_caption("Jogo")
    run = True
    bg_rolagem = 0
    direita_x = False
    esquerda_x = False
    Tiro = False
    while run:

        relogio.tick(60)

        tela.fill(pygame.Color("white"))

        bg()

        lv1.draw()

        texto(f'Tiro cooldown:{Jogador.tiro_cooldown}', fonte, (0, 255, 255), 30, 70)

        # GRUPOS

        for Inimigo in Inimigos_Grupo:
            Inimigo.AI()
            Inimigo.desenhar()
            Inimigo.update()

        Tiro_Grupo.update()
        Tiro_Grupo.draw(tela)

        # Jogador
        Barra_saude.desenhar(Jogador.hp)

        Jogador.update()
        Jogador.desenhar()

        if Jogador.vivo:
            if Tiro:
                Jogador.Atirar()
            if Jogador.no_ar:
                Jogador.Animacao(1)  # dps pra 2
            elif direita_x or esquerda_x:
                Jogador.Animacao(1)
            else:
                Jogador.Animacao(0)

            Jogador.move(direita_x, esquerda_x)
            bg_rolagem -= tl_rolagem
            # Pega teclas especiais (Crtl, Alt...)

        mods = pygame.key.get_mods()
        for event in pygame.event.get():
            # Exit
            if event.type == pygame.QUIT or mods & pygame.KMOD_CTRL and event.key == pygame.K_w:
                sys.exit()
            # Controles

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                Tiro = True
            if event.type == pygame.MOUSEBUTTONUP:
                Tiro = False

            if event.type == pygame.K_ESCAPE:
                menu()

        pygame.display.update()


menu()

# Problemas atuais: 
#
# -[X] Pulo e andar em simultâneo
# -[] Mundo scroll n vai, só n vai, ele se recusa
#
# https://www.youtube.com/watch?v=JTM8_pcQOUU&list=PLjcN1EyupaQm20hlUE11y9y8EY2aXLpnv&index=11

# o mano 2
# https://www.youtube.com/watch?v=YWN8GcmJ-jA&list=PL8ui5HK3oSiGXM2Pc2DahNu1xXBf7WQh-&index=3
