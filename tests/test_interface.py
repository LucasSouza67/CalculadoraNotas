import pytest
import tkinter as tk
from unittest.mock import MagicMock, patch, call
import sys
import os

# Adiciona a pasta raiz do projeto ao sys.path para encontrar o módulo 'build'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa a função a ser testada
from build.main import criar_campos_entrada

@pytest.fixture
def mock_ui(monkeypatch):
    """
    Fixture do Pytest para criar e injetar mocks para os componentes de UI globais
    usados pela função `criar_campos_entrada`.
    """
    # Mock para os campos de entrada do número de avaliações
    mock_entry_n1 = MagicMock()
    mock_entry_n2 = MagicMock()

    # Mock para o frame que contém os campos de nota
    mock_frame = MagicMock()
    mock_frame.winfo_children.return_value = [MagicMock(), MagicMock()] # Simula widgets existentes

    # Mock para a lista global de entries
    mock_entries_list = []

    # Mock para a função messagebox
    mock_messagebox = MagicMock()

    # Usa monkeypatch para substituir as variáveis e módulos globais no `build.main`
    monkeypatch.setattr("build.main.entry_num_n1", mock_entry_n1)
    monkeypatch.setattr("build.main.entry_num_n2", mock_entry_n2)
    monkeypatch.setattr("build.main.input_frame_notas", mock_frame)
    monkeypatch.setattr("build.main.entries", mock_entries_list)
    monkeypatch.setattr("build.main.messagebox", mock_messagebox)
    
    # Mock para os construtores de widgets Tkinter
    monkeypatch.setattr("build.main.tk.Label", MagicMock())
    monkeypatch.setattr("build.main.tk.Entry", MagicMock())

    # Retorna os mocks para que possam ser usados nos testes
    return {
        "entry_n1": mock_entry_n1,
        "entry_n2": mock_entry_n2,
        "frame": mock_frame,
        "entries_list": mock_entries_list,
        "messagebox": mock_messagebox,
    }

def test_criar_campos_entrada_sucesso(mock_ui):
    """
    Testa o caminho de sucesso: entradas válidas que geram os campos de nota.
    """
    # Configura o valor retornado pelos mocks dos campos de entrada
    mock_ui["entry_n1"].get.return_value = "2"
    mock_ui["entry_n2"].get.return_value = "3"

    # Chama a função
    criar_campos_entrada()

    # 1. Verifica se os widgets antigos foram destruídos
    mock_ui["frame"].winfo_children.assert_called_once()
    assert mock_ui["frame"].winfo_children.return_value[0].destroy.called
    assert mock_ui["frame"].winfo_children.return_value[1].destroy.called

    # 2. Verifica se a lista de entries foi limpa
    assert len(mock_ui["entries_list"]) == 5 # 2 para N1 + 3 para N2

    # 3. Verifica se nenhuma caixa de erro foi mostrada
    mock_ui["messagebox"].showerror.assert_not_called()

def test_criar_campos_entrada_falha_valor_invalido(mock_ui):
    """
    Testa o cenário onde a entrada não é um número (ValueError).
    """
    mock_ui["entry_n1"].get.return_value = "dois" # Valor inválido
    mock_ui["entry_n2"].get.return_value = "3"

    criar_campos_entrada()

    # Verifica se a mensagem de erro correta foi exibida
    mock_ui["messagebox"].showerror.assert_called_once_with(
        "Erro", "Por favor, digite números válidos para as avaliações."
    )

def test_criar_campos_entrada_falha_fora_do_intervalo(mock_ui):
    """
    Testa o cenário onde o número de avaliações está fora do intervalo permitido.
    """
    mock_ui["entry_n1"].get.return_value = "1"
    mock_ui["entry_n2"].get.return_value = "0" # Inválido, precisa ser >= 1

    criar_campos_entrada()

    # Verifica se a mensagem de erro correta foi exibida
    mock_ui["messagebox"].showerror.assert_called_once_with(
        "Erro", "O número total de avaliações deve ser entre 2 e 6, com pelo menos uma avaliação para N1 e N2."
    )
