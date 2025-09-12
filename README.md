# 📝 Calculadora de Notas

Uma aplicação de desktop desenvolvida em Python com Tkinter que ajuda estudantes a calcular sua média final e a nota mínima necessária para a aprovação, com base nas notas das etapas N1 e N2.

---

## ✨ Funcionalidades

-   **Cálculo de Média Final:** Calcula a média final ponderada com base na fórmula `(2*N1 + 3*N2) / 5`.
-   **Cálculo de Nota Mínima:** Determina a nota exata que você precisa na última avaliação da N2 para alcançar a média 7 e ser aprovado.
-   **Interface Dinâmica:** Os campos para inserir as notas são criados dinamicamente com base no número de avaliações que você define para N1 e N2.
-   **Validação de Entrada:** Garante que apenas valores numéricos válidos (entre 0 e 10) sejam inseridos.
-   **Interface Intuitiva:** Design limpo e simples para facilitar o uso.

---

## 🛠️ Tecnologias Utilizadas

-   **Python 3**
-   **Tkinter:** Para a construção da interface gráfica.
-   **Pillow (PIL):** Para manipulação e exibição de imagens na interface.

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para executar a calculadora em sua máquina.

### Pré-requisitos

-   Python 3 instalado.
-   `pip` (gerenciador de pacotes do Python).

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    ```
    - No Windows, ative-o com:
      ```bash
      .\venv\Scripts\activate
      ```
    - No macOS/Linux, ative-o com:
      ```bash
      source venv/bin/activate
      ```

3.  **Instale as dependências:**
    O projeto possui um arquivo `requirements.txt` com todas as dependências. Instale-as com o seguinte comando:
    ```bash
    pip install -r requirements.txt
    ```

### Execução

Para iniciar a aplicação, execute o script `main.py` que está na pasta `build`:

```bash
python build/main.py

** O projeto está organizado da seguinte forma para separar o código fonte, os recursos e o script principal:
CalculadoraDeNotas/
├── build/
│   └── main.py         # Script principal da aplicação
├── src/
│   └── images/         # Pasta com as imagens e ícones
│       ├── logoIFCE.png
│       └── ...
└── README.md           # Este arquivo
