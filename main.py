import pygame
import random
import itertools
import time
import sys

pygame.init()
WIDTH, HEIGHT = 900, 700
UI_HEIGHT = 150
CANVAS_HEIGHT = HEIGHT - UI_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caixeiro Viajante - Força Bruta vs Vizinho mais próximo")
font = pygame.font.SysFont("Arial", 16)
font_large = pygame.font.SysFont("Arial", 20, bold=True)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
ROSE = (238, 130, 238)
PURPLE = (106, 90, 205)
GREEN = (50, 200, 50)

cidades = [] # Lista de tuplas (x, y)
matriz_distancias = []
rota_atual = []
custo_atual = 0
tempo_atual = 0.0
modo_exibicao = None # 'BRUTA' ou 'VIZINHO'

def adicionar_cidade(pos):
    """Adiciona uma cidade e atualiza a matriz com custos aleatórios simétricos."""
    cidades.append(pos)
    n = len(cidades)
    
    if n == 1:
        matriz_distancias.append([0])
    else:
        nova_linha = []
        for i in range(n - 1):
            # Custo aleatório entre 10 e 100
            custo_aleatorio = random.randint(10, 100)
            matriz_distancias[i].append(custo_aleatorio)
            nova_linha.append(custo_aleatorio)
        nova_linha.append(0) # Distância para si mesmo é 0
        matriz_distancias.append(nova_linha)

def tsp_forca_bruta():
    """Calculo com base em todas as combinações"""
    n = len(cidades)
    if n < 2: return [], 0
    
    menor_distancia = float('inf')
    melhor_rota = None
    
    ids_cidades = list(range(n))

    # Calcula o custo para cada permutação
    for permutacao in itertools.permutations(ids_cidades[1:]):
        rota = [0] + list(permutacao)
        distancia = 0
        for i in range(n - 1):
            distancia += matriz_distancias[rota[i]][rota[i + 1]]
        distancia += matriz_distancias[rota[-1]][0]
        
        if distancia < menor_distancia:
            menor_distancia = distancia
            melhor_rota = rota
            
    return melhor_rota + [0], menor_distancia

def tsp_vizinho_mais_proximo():
    """Cálculo com base no vizinho mais próximo"""
    n = len(cidades)
    if n < 2: return [], 0
    
    nao_visitadas = set(range(1, n))
    rota = [0]
    cidade_atual = 0
    distancia_total = 0
    
    while nao_visitadas:
        # Escolhe a cidade com base no custo 
        proxima_cidade = min(nao_visitadas, key=lambda c: matriz_distancias[cidade_atual][c])
        distancia_total += matriz_distancias[cidade_atual][proxima_cidade]
        rota.append(proxima_cidade)
        nao_visitadas.remove(proxima_cidade)
        cidade_atual = proxima_cidade
        
    distancia_total += matriz_distancias[cidade_atual][0]
    rota.append(0)
    
    return rota, distancia_total

def desenhar_botoes():
    botoes = [
        {"rect": pygame.Rect(20, HEIGHT - 130, 200, 40), "cor": PURPLE, "texto": "1. Força Bruta", "acao": "BRUTA"},
        {"rect": pygame.Rect(240, HEIGHT - 130, 200, 40), "cor": ROSE, "texto": "2. Vizinho Próximo", "acao": "VIZINHO"},
        {"rect": pygame.Rect(460, HEIGHT - 130, 150, 40), "cor": GRAY, "texto": "Limpar Tudo", "acao": "LIMPAR"}
    ]
    
    for btn in botoes:
        pygame.draw.rect(screen, btn["cor"], btn["rect"], border_radius=5)
        txt = font_large.render(btn["texto"], True, WHITE if btn["cor"] != GRAY else BLACK)
        txt_rect = txt.get_rect(center=btn["rect"].center)
        screen.blit(txt, txt_rect)
        
    return botoes

def desenhar_estatisticas():
    y_offset = HEIGHT - 80
    info_cidades = font.render(f"Cidades no mapa: {len(cidades)}", True, BLACK)
    screen.blit(info_cidades, (20, y_offset))
    
    if modo_exibicao:
        cor_destaque = PURPLE if modo_exibicao == 'BRUTA' else ROSE
        algoritmo = "Força Bruta" if modo_exibicao == 'BRUTA' else "Vizinho Próximo (Gulosa)"
        
        info_alg = font_large.render(f"Algoritmo: {algoritmo}", True, cor_destaque)
        info_custo = font_large.render(f"Custo Total: {custo_atual}", True, BLACK)
        info_tempo = font.render(f"Tempo de execução: {tempo_atual:.6f} segundos", True, BLACK)
        
        screen.blit(info_alg, (240, y_offset))
        screen.blit(info_custo, (240, y_offset + 25))
        screen.blit(info_tempo, (240, y_offset + 50))

        caminho_str = " -> ".join(str(c) for c in rota_atual)
        info_ordem = font.render(f"Ordem percorrida: {caminho_str}", True, cor_destaque)
        screen.blit(info_ordem, (460, y_offset + 25))



def desenhar_cidades_e_rotas():
    """Desenhar as cidades e rotas se calculadas"""
    if rota_atual and len(rota_atual) > 1:
        cor_rota = PURPLE if modo_exibicao == 'BRUTA' else ROSE
        for i in range(len(rota_atual) - 1):
            c1 = rota_atual[i]
            c2 = rota_atual[i + 1]
            p1 = cidades[c1]
            p2 = cidades[c2]
            
            # Linha
            pygame.draw.line(screen, cor_rota, p1, p2, 3)
            
            # Custo da aresta (no meio da linha)
            custo_aresta = matriz_distancias[c1][c2]
            mid_x = (p1[0] + p2[0]) // 2
            mid_y = (p1[1] + p2[1]) // 2
            texto_label = f"{i + 1}º (Custo: {custo_aresta})"
            txt_custo = font.render(texto_label, True, BLACK)
            
            bg_rect = txt_custo.get_rect(center=(mid_x, mid_y))
            pygame.draw.rect(screen, WHITE, bg_rect)
            pygame.draw.rect(screen, cor_rota, bg_rect, 1)
            screen.blit(txt_custo, bg_rect)

    for i, pos in enumerate(cidades):
        pygame.draw.circle(screen, BLACK, pos, 15)
        txt = font.render(str(i), True, WHITE)
        screen.blit(txt, txt.get_rect(center=pos))

running = True
while running:
    screen.fill(WHITE)
    
    # Desenhar área da Interface e divisor
    pygame.draw.rect(screen, (240, 240, 240), (0, CANVAS_HEIGHT, WIDTH, UI_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, CANVAS_HEIGHT), (WIDTH, CANVAS_HEIGHT), 2)
    
    botoes = desenhar_botoes()
    desenhar_cidades_e_rotas()
    desenhar_estatisticas()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            
            # Verificar se clicou em um botão
            clicou_botao = False
            for btn in botoes:
                if btn["rect"].collidepoint(pos):
                    clicou_botao = True
                    
                    if btn["acao"] == "LIMPAR":
                        cidades = []
                        matriz_distancias = []
                        rota_atual = []
                        custo_atual = 0
                        modo_exibicao = None
                        
                    elif btn["acao"] == "BRUTA" and len(cidades) > 1:
                        if len(cidades) > 11:
                            print("Aviso: Muitas cidades para Força Bruta (pode travar).")
                        
                        inicio = time.perf_counter()
                        rota_atual, custo_atual = tsp_forca_bruta()
                        fim = time.perf_counter()
                        
                        tempo_atual = fim - inicio
                        modo_exibicao = "BRUTA"
                        
                    elif btn["acao"] == "VIZINHO" and len(cidades) > 1:
                        inicio = time.perf_counter()
                        rota_atual, custo_atual = tsp_vizinho_mais_proximo()
                        fim = time.perf_counter()
                        
                        tempo_atual = fim - inicio
                        modo_exibicao = "VIZINHO"
            
            # Se clicou na área do mapa, adicionar cidade
            if not clicou_botao and pos[1] < CANVAS_HEIGHT - 15:
                adicionar_cidade(pos)
                rota_atual = [] # Reseta a rota visual ao adicionar nova cidade
                modo_exibicao = None

    pygame.display.flip()

pygame.quit()
sys.exit()