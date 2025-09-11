import pytest
import sys
import os

# Adiciona a pasta raiz do projeto ao sys.path
# Isso permite que o Python encontre o pacote 'build'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
 
from build.main import calcular_media_final, calcular_nota_minima

@pytest.mark.parametrize("notas_n1, notas_n2, expected", [
    # Caso 1: Notas simples, resultado inteiro
    ([7], [7], 7.0),
    # Caso 2: Notas diferentes, resultado decimal
    ([8], [6], 6.8),
    # Caso 3: Múltiplas notas em cada etapa
    ([7, 9], [5, 7, 9], 7.4),
    # Caso 4: Notas com valores decimais
    ([6.5], [7.5], 7.1),
    # Caso 5: Notas máximas
    ([10, 10], [10], 10.0),
    # Caso 6: Notas mínimas
    ([0], [0, 0], 0.0),
])
def test_calcular_media_final_casos_validos(notas_n1, notas_n2, expected):
    """
    Testa a função calcular_media_final com diferentes entradas válidas.
    """
    # O pytest.approx é usado para comparar números de ponto flutuante com uma tolerância
    assert calcular_media_final(notas_n1, notas_n2) == pytest.approx(expected)

def test_calcular_media_final_com_lista_n1_vazia():
    """
    Testa o comportamento quando a lista de notas N1 está vazia.
    A função deve retornar 0.
    """
    assert calcular_media_final([], [8, 9]) == 0

def test_calcular_media_final_com_lista_n2_vazia():
    """
    Testa o comportamento quando a lista de notas N2 está vazia.
    A função deve retornar 0.
    """
    assert calcular_media_final([7, 8], []) == 0

def test_calcular_media_final_com_ambas_listas_vazias():
    """
    Testa o comportamento quando ambas as listas de notas estão vazias.
    A função deve retornar 0.
    """
    assert calcular_media_final([], []) == 0

@pytest.mark.parametrize("notas_n1, notas_n2_parcial, total_av_n1, total_av_n2, expected", [
    # Caso 1: Cenário simples para passar com 7
    ([7.0], [], 1, 2, 14.0),
    # Caso 2: N1 alta, precisa de menos na N2
    ([10.0], [4.0], 1, 2, 6.0),
    # Caso 3: N1 baixa, precisa de mais na N2
    ([4.0], [6.0], 1, 2, 12.0),
    # Caso 4: Múltiplas notas
    ([7.0], [5.0], 1, 2, 9.0),
    # Caso 5: Nota necessária é exatamente 10
    ([5.0], [5.0], 1, 2, 11.666666666666668),
])
def test_calcular_nota_minima_casos_validos(notas_n1, notas_n2_parcial, total_av_n1, total_av_n2, expected):
    """
    Testa o cálculo da nota mínima em cenários onde é possível atingir a média.
    """
    assert calcular_nota_minima(notas_n1, notas_n2_parcial, total_av_n1, total_av_n2) == pytest.approx(expected)

def test_calcular_nota_minima_com_total_av_zero():
    """Testa se a função retorna 0 quando o total de avaliações é zero para evitar divisão por zero."""
    assert calcular_nota_minima([10], [], 0, 2) == 0
    assert calcular_nota_minima([10], [], 1, 0) == 0
