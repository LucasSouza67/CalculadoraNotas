import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk

# --- Variáveis Globais ---
entries = []
num_avaliacoes_n1 = 0
num_avaliacoes_n2 = 0

# --- Variáveis Globais para Widgets (inicializadas como None) ---
root = None
entry_num_n1 = None
entry_num_n2 = None
input_frame_notas = None
label_resultado_media = None
label_resultado_minima = None

# --- Paleta de Cores ---
BACKGROUND_COLOR = "#f0f0f0"
BUTTON_BG_COLOR = "#4a7a8c"
BUTTON_FG_COLOR = "white"
BUTTON_HOVER_COLOR = "#5c94a9"
LABEL_COLOR = "#333333"
ENTRY_BG_COLOR = "white"

#  Funções de Cálculo 
def calcular_media_final(notas_n1, notas_n2):
    if not notas_n1 or not notas_n2:
        return 0
    n1 = sum(notas_n1) / len(notas_n1)
    n2 = sum(notas_n2) / len(notas_n2)
    media_final = (2 * n1 + 3 * n2) / 5
    return media_final

# Calcula a nota mínima necessária na última avaliação da N2 para obter média 7.
def calcular_nota_minima(notas_n1_preenchidas, notas_n2_preenchidas, total_av_n1, total_av_n2):
    if not total_av_n1 or not total_av_n2:
        return 0

    soma_n1 = sum(notas_n1_preenchidas)
    soma_n2 = sum(notas_n2_preenchidas)

    n1_calculada = soma_n1 / total_av_n1

    nota_minima_av_ultima = ((35 - 2 * n1_calculada) * total_av_n2 / 3) - soma_n2
    return nota_minima_av_ultima

#  Funções da Interface Gráfica 

def criar_campos_entrada():
    global num_avaliacoes_n1, num_avaliacoes_n2
    try:
        num_avaliacoes_n1 = int(entry_num_n1.get())
        num_avaliacoes_n2 = int(entry_num_n2.get())
        total_avaliacoes = num_avaliacoes_n1 + num_avaliacoes_n2
        if not (2 <= total_avaliacoes <= 6) or num_avaliacoes_n1 < 1 or num_avaliacoes_n2 < 1:
            messagebox.showerror("Erro", "O número total de avaliações deve ser entre 2 e 6, com pelo menos uma avaliação para N1 e N2.")
            return
    except ValueError:
        messagebox.showerror("Erro", "Por favor, digite números válidos para as avaliações.")
        return

    for widget in input_frame_notas.winfo_children():
        widget.destroy()
    entries.clear()

    tk.Label(input_frame_notas, text="Avaliações N1", font=("Helvetica", 11, "bold"), fg=LABEL_COLOR, bg=BACKGROUND_COLOR).grid(row=0, column=0, columnspan=2, pady=5)
    for i in range(num_avaliacoes_n1):
        label = tk.Label(input_frame_notas, text=f"Nota AV{i+1}:", font=("Helvetica", 10), fg=LABEL_COLOR, bg=BACKGROUND_COLOR)
        label.grid(row=i+1, column=0, pady=2, sticky='w')
        entry = tk.Entry(input_frame_notas, width=15, font=("Helvetica", 10), bg=ENTRY_BG_COLOR)
        entry.grid(row=i+1, column=1, pady=2)
        entries.append(entry)
    
    tk.Label(input_frame_notas, text="Avaliações N2", font=("Helvetica", 11, "bold"), fg=LABEL_COLOR, bg=BACKGROUND_COLOR).grid(row=num_avaliacoes_n1 + 1, column=0, columnspan=2, pady=5)
    for i in range(num_avaliacoes_n2):
        label = tk.Label(input_frame_notas, text=f"Nota AV{num_avaliacoes_n1 + i+1}:", font=("Helvetica", 10), fg=LABEL_COLOR, bg=BACKGROUND_COLOR)
        label.grid(row=num_avaliacoes_n1 + i + 2, column=0, pady=2, sticky='w')
        entry = tk.Entry(input_frame_notas, width=15, font=("Helvetica", 10), bg=ENTRY_BG_COLOR)
        entry.grid(row=num_avaliacoes_n1 + i + 2, column=1, pady=2)
        entries.append(entry)

# Define e retorna as notas válidas, separadas em duas listas distintas para N1 e N2.
def obter_notas_validas():
    global num_avaliacoes_n1, num_avaliacoes_n2
    
    notas_n1_preenchidas = []
    notas_n2_preenchidas = []
    
    for i, entry in enumerate(entries):
        if entry.get():
            try:
                nota = float(entry.get())
                if not (0 <= nota <= 10):
                    messagebox.showerror("Erro de Entrada", "Por favor, insira notas entre 0 e 10.")
                    return None, None
                
                if i < num_avaliacoes_n1:
                    notas_n1_preenchidas.append(nota)
                else:
                    notas_n2_preenchidas.append(nota)
            except ValueError:
                messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos válidos.")
                return None, None
    
    return notas_n1_preenchidas, notas_n2_preenchidas

# Botão para calcular a média
def acao_calcular_media():
    notas_n1, notas_n2 = obter_notas_validas()
    if notas_n1 is None or len(notas_n1) != num_avaliacoes_n1 or len(notas_n2) != num_avaliacoes_n2:
        messagebox.showwarning("Aviso", "Preencha todas as notas para calcular a média final.")
        return
    
    media_final = calcular_media_final(notas_n1, notas_n2)
    label_resultado_media.config(text=f"Média Final: {media_final:.2f}", fg="#008000")
    label_resultado_minima.config(text="")

# Botão para calcular a nota mínima
def acao_calcular_minima():
    global num_avaliacoes_n1, num_avaliacoes_n2
    
    notas_n1, notas_n2 = obter_notas_validas()
    
    if notas_n1 is None or len(notas_n1) != num_avaliacoes_n1 or len(notas_n2) != num_avaliacoes_n2 - 1:
        messagebox.showwarning("Aviso", "Para calcular a nota mínima, preencha todas as notas de N1 e todas as notas de N2, exceto a última.")
        return
    
    nota_minima = calcular_nota_minima(notas_n1, notas_n2, num_avaliacoes_n1, num_avaliacoes_n2)
    
    if 0 <= nota_minima <= 10:
        label_resultado_minima.config(text=f"Nota mínima na última AV de N2: {nota_minima:.2f}", fg="#0000FF") # Exibe a o resultado da nota mínima
    else:
        label_resultado_minima.config(text="Não é possível obter média 7 com as notas fornecidas.", fg="#FF0000") # Exibe uma mensagem se não for possível obter média 7
    label_resultado_media.config(text="")

def limpar_campos():
    entry_num_n1.delete(0, tk.END)
    entry_num_n2.delete(0, tk.END)
    for widget in input_frame_notas.winfo_children():
        widget.destroy()
    entries.clear()
    label_resultado_media.config(text="")
    label_resultado_minima.config(text="")

def on_enter(e):
    e.widget['background'] = BUTTON_HOVER_COLOR
def on_leave(e):
    e.widget['background'] = BUTTON_BG_COLOR

def main():
    """Cria e executa a interface gráfica principal da aplicação."""
    global root, entry_num_n1, entry_num_n2, input_frame_notas, label_resultado_media, label_resultado_minima

    root = tk.Tk()
    root.title("Calculadora de Notas")
    root.geometry("600x850")
    root.resizable(False, False)
    root.config(bg=BACKGROUND_COLOR)

    # Frame para o cabeçalho (logo e título)
    header_frame = tk.Frame(root, bg=BACKGROUND_COLOR, padx=15, pady=10)
    header_frame.pack(fill=tk.X, pady=(15, 0))

    # --- Caminho base para as imagens ---
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Diretório do script atual (build)
    project_root = os.path.dirname(script_dir) # Sobe um nível para a raiz do projeto
    image_path = os.path.join(project_root, "src", "images")

    # --- Adicionando a Imagem ---
    try:
        logo_path = os.path.join(image_path, "logoIFCE.png")
        imagem_logo_pil = Image.open(logo_path).resize((120, 120))
        imagem_logo_tk = ImageTk.PhotoImage(imagem_logo_pil)
        
        label_logo = tk.Label(header_frame, image=imagem_logo_tk, bg=BACKGROUND_COLOR)
        label_logo.image = imagem_logo_tk
        
        title_label = tk.Label(header_frame, text="Calculadora de Notas", font=("Helvetica", 16, "bold"), bg=BACKGROUND_COLOR, fg=LABEL_COLOR)

        label_logo.grid(row=0, column=0, padx=(0, 50))
        title_label.grid(row=0, column=1, sticky="w")
        
    except FileNotFoundError:
        print("Aviso: Arquivo de imagem não encontrado. A logomarca não será exibida.")
        title_label = tk.Label(header_frame, text="Calculadora de Notas", font=("Helvetica", 16, "bold"), bg=BACKGROUND_COLOR, fg=LABEL_COLOR)
        title_label.pack(anchor=tk.W)

    # definindo imagens
    imagem_calculadora = Image.open(os.path.join(image_path, "calculate_24dp_black.png"))
    imagem_confirma = Image.open(os.path.join(image_path, "confirm_24dp_black.png"))
    imagem_limpar= Image.open(os.path.join(image_path, "cleaning_services_24dp_black.png"))

    tamanho_desejado = (20, 20)
    imagem_calculadora = imagem_calculadora.resize(tamanho_desejado, Image.Resampling.LANCZOS)
    imagem_confirma = imagem_confirma.resize(tamanho_desejado, Image.Resampling.LANCZOS)
    imagem_limpar = imagem_limpar.resize(tamanho_desejado, Image.Resampling.LANCZOS)

    imagem_calc = ImageTk.PhotoImage(imagem_calculadora)
    imagem_conf = ImageTk.PhotoImage(imagem_confirma)
    imagem_clear = ImageTk.PhotoImage(imagem_limpar)

    num_avaliacoes_frame = tk.Frame(root, padx=10, pady=10, bg=BACKGROUND_COLOR)
    num_avaliacoes_frame.pack(pady=5)

    input_frame_notas = tk.Frame(root, padx=15, pady=5, bg=BACKGROUND_COLOR)
    input_frame_notas.pack(pady=5)

    button_frame = tk.Frame(root, padx=15, pady=10, bg=BACKGROUND_COLOR)
    button_frame.pack(pady=5)

    result_frame = tk.Frame(root, padx=15, pady=15, bg=BACKGROUND_COLOR)
    result_frame.pack(pady=10)

    tk.Label(num_avaliacoes_frame, text="Nº de Avaliações N1:", font=("Helvetica", 10, "bold"), fg=LABEL_COLOR, bg=BACKGROUND_COLOR).grid(row=0, column=0, pady=5, sticky='w')
    entry_num_n1 = tk.Entry(num_avaliacoes_frame, width=10, font=("Helvetica", 10), bg=ENTRY_BG_COLOR)
    entry_num_n1.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(num_avaliacoes_frame, text="Nº de Avaliações N2:", font=("Helvetica", 10, "bold"), fg=LABEL_COLOR, bg=BACKGROUND_COLOR).grid(row=1, column=0, pady=5, sticky='w')
    entry_num_n2 = tk.Entry(num_avaliacoes_frame, width=10, font=("Helvetica", 10), bg=ENTRY_BG_COLOR)
    entry_num_n2.grid(row=1, column=1, padx=5, pady=5)

    btn_confirmar = tk.Button(num_avaliacoes_frame, text="Confirmar", command=criar_campos_entrada, font=("Helvetica", 10, "bold"), bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, relief="flat", padx=10, pady=5,  image=imagem_conf, compound=tk.LEFT)
    btn_confirmar.grid(row=2, column=0, columnspan=2, pady=10)
    btn_confirmar.bind("<Enter>", on_enter)
    btn_confirmar.bind("<Leave>", on_leave)

    btn_calcular_media = tk.Button(button_frame, text="Calcular Média Final", command=acao_calcular_media, font=("Helvetica", 10, "bold"), bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, relief="flat", padx=10, pady=5, image=imagem_calc, compound=tk.LEFT)
    btn_calcular_media.grid(row=0, column=0, padx=5, pady=5)
    btn_calcular_media.bind("<Enter>", on_enter)
    btn_calcular_media.bind("<Leave>", on_leave)

    btn_calcular_minima = tk.Button(button_frame, text="Calcular Nota Mínima", command=acao_calcular_minima, font=("Helvetica", 10, "bold"), bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, relief="flat", padx=10, pady=5, image=imagem_calc, compound=tk.LEFT)
    btn_calcular_minima.grid(row=0, column=1, padx=5, pady=5)
    btn_calcular_minima.bind("<Enter>", on_enter)
    btn_calcular_minima.bind("<Leave>", on_leave)

    btn_limpar = tk.Button(button_frame, text="Limpar", command=limpar_campos, font=("Helvetica", 10), bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, relief="flat", padx=10, pady=5, image=imagem_clear, compound=tk.LEFT)
    btn_limpar.grid(row=1, column=0, columnspan=2, pady=5)
    btn_limpar.bind("<Enter>", on_enter)
    btn_limpar.bind("<Leave>", on_leave)

    label_resultado_media = tk.Label(result_frame, text="", font=("Helvetica", 12, "bold"), bg=BACKGROUND_COLOR, fg=LABEL_COLOR)
    label_resultado_media.pack(pady=5)

    label_resultado_minima = tk.Label(result_frame, text="", font=("Helvetica", 12, "bold"), bg=BACKGROUND_COLOR, fg=LABEL_COLOR)
    label_resultado_minima.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()