import tkinter as tk
from tkinter import messagebox
import random
from enum import Enum

class Direcao(Enum):
    CIMA = 0
    BAIXO = 1
    ESQUERDA = 2
    DIREITA = 3

class JogoCobra:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Cobra")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a1a")
        
        # Configurações do jogo
        self.tamanho_bloco = 20
        self.largura = 800 // self.tamanho_bloco
        self.altura = 600 // self.tamanho_bloco
        
        # Estado do jogo
        self.cobra = [(self.largura // 2, self.altura // 2)]
        self.direcao = Direcao.DIREITA
        self.proxima_direcao = Direcao.DIREITA
        self.comida = self.gerar_comida()
        self.pontuacao = 0
        self.velocidade = 100  # em ms
        self.jogo_ativo = True
        
        # Interface
        self.criar_interface()
        self.atualizar_jogo()
        
    def criar_interface(self):
        """Cria a interface do jogo"""
        # Frame superior com instruções
        frame_superior = tk.Frame(self.root, bg="#1a1a1a")
        frame_superior.pack(fill=tk.X, padx=10, pady=10)
        
        # Label do título
        titulo = tk.Label(frame_superior, text="🐍 JOGO DA COBRA 🐍", 
                         font=("Arial", 20, "bold"), 
                         bg="#1a1a1a", fg="#00FF00")
        titulo.pack(side=tk.LEFT)
        
        # Label da pontuação
        self.label_pontuacao = tk.Label(frame_superior, text="Pontuação: 0", 
                                        font=("Arial", 16, "bold"),
                                        bg="#1a1a1a", fg="#FFD700")
        self.label_pontuacao.pack(side=tk.RIGHT, padx=20)
        
        # Canvas para desenhar o jogo
        self.canvas = tk.Canvas(self.root, width=800, height=550, 
                               bg="#000000", highlightthickness=0)
        self.canvas.pack(padx=10, pady=5)
        
        # Frame inferior com instruções
        frame_inferior = tk.Frame(self.root, bg="#1a1a1a")
        frame_inferior.pack(fill=tk.X, padx=10, pady=10)
        
        instrucoes = tk.Label(frame_inferior, 
                             text="⬆️ ⬇️ ⬅️ ➡️ Setas para mover | ESPAÇO para pausar | R para recomeçar",
                             font=("Arial", 10), 
                             bg="#1a1a1a", fg="#FFFFFF")
        instrucoes.pack()
        
        # Bind das teclas
        self.root.bind("<Up>", lambda e: self.mover(Direcao.CIMA))
        self.root.bind("<Down>", lambda e: self.mover(Direcao.BAIXO))
        self.root.bind("<Left>", lambda e: self.mover(Direcao.ESQUERDA))
        self.root.bind("<Right>", lambda e: self.mover(Direcao.DIREITA))
        self.root.bind("<space>", self.pausar)
        self.root.bind("<r>", self.recomecar)
        self.root.bind("<R>", self.recomecar)
    
    def mover(self, direcao):
        """Define a próxima direção"""
        # Evita que a cobra volte para trás
        if (self.direcao == Direcao.CIMA and direcao == Direcao.BAIXO) or \
           (self.direcao == Direcao.BAIXO and direcao == Direcao.CIMA) or \
           (self.direcao == Direcao.ESQUERDA and direcao == Direcao.DIREITA) or \
           (self.direcao == Direcao.DIREITA and direcao == Direcao.ESQUERDA):
            return
        self.proxima_direcao = direcao
    
    def atualizar_jogo(self):
        """Atualiza a lógica do jogo"""
        if not self.jogo_ativo:
            return
        
        # Atualiza a direção
        self.direcao = self.proxima_direcao
        
        # Calcula a nova posição da cabeça
        cabeca_x, cabeca_y = self.cobra[0]
        
        if self.direcao == Direcao.CIMA:
            cabeca_y -= 1
        elif self.direcao == Direcao.BAIXO:
            cabeca_y += 1
        elif self.direcao == Direcao.ESQUERDA:
            cabeca_x -= 1
        elif self.direcao == Direcao.DIREITA:
            cabeca_x += 1
        
        # Verifica colisão com as paredes
        if cabeca_x < 0 or cabeca_x >= self.largura or cabeca_y < 0 or cabeca_y >= self.altura:
            self.fim_jogo("Você colidiu com a parede!")
            return
        
        # Verifica colisão com a própria cobra
        if (cabeca_x, cabeca_y) in self.cobra:
            self.fim_jogo("Você colidiu com a própria cobra!")
            return
        
        # Adiciona a nova cabeça
        self.cobra.insert(0, (cabeca_x, cabeca_y))
        
        # Verifica se comeu a comida
        if (cabeca_x, cabeca_y) == self.comida:
            self.pontuacao += 10
            self.comida = self.gerar_comida()
            # Aumenta a velocidade a cada 50 pontos
            if self.pontuacao % 50 == 0 and self.velocidade > 30:
                self.velocidade -= 5
        else:
            # Remove a cauda se não comeu
            self.cobra.pop()
        
        # Desenha o jogo
        self.desenhar()
        
        # Chama a função novamente
        self.root.after(self.velocidade, self.atualizar_jogo)
    
    def gerar_comida(self):
        """Gera uma nova comida em posição aleatória"""
        while True:
            x = random.randint(0, self.largura - 1)
            y = random.randint(0, self.altura - 1)
            if (x, y) not in self.cobra:
                return (x, y)
    
    def desenhar(self):
        """Desenha o jogo no canvas"""
        self.canvas.delete("all")
        
        # Desenha a grade (opcional)
        for i in range(0, 800, self.tamanho_bloco):
            self.canvas.create_line(i, 0, i, 550, fill="#222222", width=1)
        for i in range(0, 550, self.tamanho_bloco):
            self.canvas.create_line(0, i, 800, i, fill="#222222", width=1)
        
        # Desenha a cobra
        for i, (x, y) in enumerate(self.cobra):
            x1 = x * self.tamanho_bloco
            y1 = y * self.tamanho_bloco
            x2 = x1 + self.tamanho_bloco
            y2 = y1 + self.tamanho_bloco
            
            if i == 0:  # Cabeça
                self.canvas.create_oval(x1, y1, x2, y2, fill="#00FF00", outline="#00AA00", width=2)
                # Desenha olhos
                olho_x = x1 + self.tamanho_bloco // 2
                olho_y = y1 + self.tamanho_bloco // 2
                self.canvas.create_oval(olho_x - 2, olho_y - 5, olho_x + 2, olho_y - 2, 
                                       fill="#000000")
                self.canvas.create_oval(olho_x + 5, olho_y - 5, olho_x + 8, olho_y - 2,
                                       fill="#000000")
            else:  # Corpo
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#00CC00", outline="#008800", width=1)
        
        # Desenha a comida
        x1 = self.comida[0] * self.tamanho_bloco
        y1 = self.comida[1] * self.tamanho_bloco
        x2 = x1 + self.tamanho_bloco
        y2 = y1 + self.tamanho_bloco
        self.canvas.create_oval(x1, y1, x2, y2, fill="#FF0000", outline="#AA0000", width=2)
        # Desenha uma estrela na comida
        self.canvas.create_text((x1 + self.tamanho_bloco // 2), (y1 + self.tamanho_bloco // 2),
                               text="✦", font=("Arial", 14), fill="#FFFF00")
        
        # Atualiza a pontuação
        self.label_pontuacao.config(text=f"Pontuação: {self.pontuacao}")
    
    def pausar(self, event=None):
        """Pausa/despausa o jogo"""
        self.jogo_ativo = not self.jogo_ativo
        if self.jogo_ativo:
            self.atualizar_jogo()
    
    def recomecar(self, event=None):
        """Recomeça o jogo"""
        self.cobra = [(self.largura // 2, self.altura // 2)]
        self.direcao = Direcao.DIREITA
        self.proxima_direcao = Direcao.DIREITA
        self.comida = self.gerar_comida()
        self.pontuacao = 0
        self.velocidade = 100
        self.jogo_ativo = True
        self.desenhar()
        self.atualizar_jogo()
    
    def fim_jogo(self, mensagem):
        """Finaliza o jogo"""
        self.jogo_ativo = False
        self.canvas.create_rectangle(0, 0, 800, 550, fill="#000000", outline="#FF0000", width=5)
        self.canvas.create_text(400, 250, text=f"GAME OVER!\n{mensagem}\nPontuação: {self.pontuacao}",
                               font=("Arial", 24, "bold"), fill="#FF0000", justify=tk.CENTER)
        self.canvas.create_text(400, 400, text="Pressione R para recomeçar",
                               font=("Arial", 16), fill="#FFFF00")


def main():
    root = tk.Tk()
    jogo = JogoCobra(root)
    root.mainloop()

if __name__ == "__main__":
    main()
