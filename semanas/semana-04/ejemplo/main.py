"""Aula Estratégica — juego humano-máquina con Minimax y poda alfa-beta.

Instalación: pip install PySide6
Ejecución: python main.py
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from functools import lru_cache

try:
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QColor, QFont
    from PySide6.QtWidgets import (
        QApplication, QFrame, QGridLayout, QHBoxLayout, QLabel, QMainWindow,
        QMessageBox, QPushButton, QScrollArea, QSpinBox, QVBoxLayout, QWidget,
    )
except ImportError:
    print('Falta PySide6. Instálalo con: pip install PySide6')
    raise SystemExit(1)

N = 4
ROUNDS = 3  # tres asientos para cada jugador
# Valores por asiento: cercanía a pizarra, enchufe, ventana, tranquilidad.
SEATS = tuple(
    (4-r, 1 if c in (0, 3) else 0, 1 if c == 0 else 0, 1 if r >= 2 else 0)
    for r in range(N) for c in range(N)
)
# Preferencias asimétricas para que la elección tenga un conflicto real.
HUMAN_WEIGHTS = (4, 1, 3, 1)
AI_WEIGHTS = (2, 5, 1, 3)


def seat_score(index: int, player: str) -> int:
    weights = AI_WEIGHTS if player == 'ai' else HUMAN_WEIGHTS
    return sum(a*b for a, b in zip(SEATS[index], weights))


def utility(human: tuple[int, ...], ai: tuple[int, ...]) -> int:
    """Utilidad de suma cero desde el punto de vista de la IA."""
    return sum(seat_score(i, 'ai') for i in ai) - sum(seat_score(i, 'human') for i in human)


@dataclass
class SearchStats:
    nodes: int = 0
    prunes: int = 0


def minimax(human: tuple[int, ...], ai: tuple[int, ...], ai_turn: bool,
            depth: int, alpha: float, beta: float, stats: SearchStats) -> int:
    stats.nodes += 1
    if depth == 0 or (len(human) == ROUNDS and len(ai) == ROUNDS):
        return utility(human, ai)
    occupied = set(human) | set(ai)
    moves = [i for i in range(N*N) if i not in occupied]
    if not moves:
        return utility(human, ai)
    # El ordenamiento mejora la poda; desempate estable por posición.
    moves.sort(key=lambda i: (-seat_score(i, 'ai' if ai_turn else 'human'), i))
    if ai_turn:
        best = -float('inf')
        for move in moves:
            best = max(best, minimax(human, ai+(move,), False, depth-1, alpha, beta, stats))
            alpha = max(alpha, best)
            if alpha >= beta:
                stats.prunes += 1
                break
    else:
        best = float('inf')
        for move in moves:
            best = min(best, minimax(human+(move,), ai, True, depth-1, alpha, beta, stats))
            beta = min(beta, best)
            if alpha >= beta:
                stats.prunes += 1
                break
    return int(best)


def choose_ai_move(human: tuple[int, ...], ai: tuple[int, ...], depth: int):
    """Devuelve mejor movimiento, evaluación, estadísticas y valores de cada candidato.

    Se busca al menos la siguiente respuesta humana, salvo si termina la partida.
    """
    occupied = set(human) | set(ai)
    moves = [i for i in range(N*N) if i not in occupied]
    moves.sort(key=lambda i: (-seat_score(i, 'ai'), i))
    stats = SearchStats()
    candidates = []
    best_move, best_value = None, -float('inf')
    alpha = -float('inf')
    for move in moves:
        value = minimax(human, ai+(move,), False, depth-1, alpha,
                        float('inf'), stats)
        candidates.append((move, value))
        if value > best_value:
            best_move, best_value = move, value
        alpha = max(alpha, best_value)
    return best_move, int(best_value), stats, candidates


def label_for(i: int) -> str:
    return f'{chr(65+i//N)}{i%N+1}'


STYLE = '''
QMainWindow, QWidget#root {background: #0b1220; color: #edf4ff;}
QLabel {color: #e6edf7;}
QLabel#title {font-size: 29px; font-weight: 800; color: #f8fafc;}
QLabel#subtitle {font-size: 12px; color: #9eb0c8;}
QLabel#section {font-size: 17px; font-weight: 700; color: #dbeafe;}
QFrame#panel {background: #152237; border: 1px solid #2b415d; border-radius: 14px;}
QLabel#stat {font-size: 21px; font-weight: 800; color: #7dd3fc;}
QPushButton#seat {background: #243850; color: #edf4ff; border: 1px solid #4b6583;
 border-radius: 12px; font-size: 16px; font-weight: 700; min-height: 74px;}
QPushButton#seat:hover:enabled {background: #335575; border: 2px solid #7dd3fc;}
QPushButton#seat:disabled {color: #b7c4d8;}
QPushButton#primary {background: #0ea5e9; color: #061526; border: 0; border-radius: 9px;
 font-weight: 800; padding: 11px 18px;}
QPushButton#primary:hover {background: #38bdf8;}
QSpinBox {background: #23354e; border: 1px solid #56708d; color: white; padding: 6px; border-radius: 7px;}
'''


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Aula Estratégica | Minimax + Alfa-Beta')
        self.resize(1080, 790)
        self.human: tuple[int, ...] = ()
        self.ai: tuple[int, ...] = ()
        self.finished = False
        self.seat_buttons = []
        self.build_ui()
        self.refresh()

    def panel(self):
        frame = QFrame()
        frame.setObjectName('panel')
        return frame

    def build_ui(self):
        root = QWidget(objectName='root')
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(24, 18, 24, 20)
        outer.setSpacing(15)
        heading = QLabel('AULA ESTRATÉGICA', objectName='title')
        outer.addWidget(heading)
        outer.addWidget(QLabel('Juego humano–máquina · 3 turnos por jugador · Minimax y poda Alfa-Beta', objectName='subtitle'))
        body = QHBoxLayout()
        body.setSpacing(18)
        outer.addLayout(body, 1)
        left = self.panel()
        left.setMinimumWidth(520)
        l = QVBoxLayout(left)
        l.setContentsMargins(20, 18, 20, 18)
        l.setSpacing(13)
        l.addWidget(QLabel('ELIGE TUS ASIENTOS', objectName='section'))
        board_hint = QLabel('PIZARRA / PROFESOR  ↑')
        board_hint.setAlignment(Qt.AlignCenter)
        board_hint.setStyleSheet('background:#30587b; padding:11px; border-radius:8px; font-weight:800;')
        l.addWidget(board_hint)
        grid = QGridLayout()
        grid.setSpacing(9)
        for i in range(N*N):
            button = QPushButton(objectName='seat')
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(lambda checked=False, j=i: self.pick_human(j))
            grid.addWidget(button, i//N, i%N)
            self.seat_buttons.append(button)
        l.addLayout(grid)
        legend = QLabel('● Azul: disponible     ● Verde: tú     ● Violeta: IA')
        legend.setStyleSheet('color:#bac9dc; font-size:12px;')
        l.addWidget(legend)
        self.status = QLabel()
        self.status.setWordWrap(True)
        self.status.setStyleSheet('font-size:14px; font-weight:650; color:#e5f2ff;')
        l.addWidget(self.status)
        l.addStretch()
        control = QHBoxLayout()
        control.addWidget(QLabel('Profundidad de búsqueda:'))
        self.depth = QSpinBox()
        self.depth.setRange(2, 4)
        self.depth.setValue(3)
        self.depth.setToolTip('3 = IA → humano → IA; 4 añade otra respuesta humana.')
        control.addWidget(self.depth)
        reset = QPushButton('Nueva partida', objectName='primary')
        reset.clicked.connect(self.reset)
        control.addWidget(reset)
        l.addLayout(control)
        body.addWidget(left, 3)

        right = self.panel()
        r = QVBoxLayout(right)
        r.setContentsMargins(19, 18, 19, 18)
        r.setSpacing(13)
        r.addWidget(QLabel('CENTRO DE DECISIONES', objectName='section'))
        self.scores = QLabel(objectName='stat')
        self.scores.setWordWrap(True)
        r.addWidget(self.scores)
        self.metrics = QLabel('Nodos: —   |   Podas: —')
        self.metrics.setStyleSheet('color:#9dddf7; font-weight:700;')
        r.addWidget(self.metrics)
        r.addWidget(QLabel('¿POR QUÉ ELIGIÓ ESE ASIENTO?', objectName='section'))
        self.explanation = QLabel()
        self.explanation.setWordWrap(True)
        self.explanation.setAlignment(Qt.AlignTop)
        self.explanation.setStyleSheet('color:#cbd8e8; line-height:1.5;')
        r.addWidget(self.explanation)
        r.addWidget(QLabel('EVALUACIÓN DE CANDIDATOS', objectName='section'))
        self.candidates = QLabel()
        self.candidates.setWordWrap(True)
        self.candidates.setAlignment(Qt.AlignTop)
        self.candidates.setTextFormat(Qt.PlainText)
        self.candidates.setStyleSheet('font-family:monospace; color:#cbd8e8; font-size:12px;')
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet('background:transparent;')
        scroll.setWidget(self.candidates)
        r.addWidget(scroll, 1)
        note = QLabel('UTILIDAD = puntos IA − puntos humanos. La IA maximiza; el rival minimiza.\n'
                      'Las podas son cortes de búsqueda, no asientos eliminados.')
        note.setWordWrap(True)
        note.setStyleSheet('color:#93a8c3; font-size:11px;')
        r.addWidget(note)
        body.addWidget(right, 2)

    def refresh(self):
        for i, button in enumerate(self.seat_buttons):
            if i in self.human:
                button.setText(f'{label_for(i)}\nTÚ')
                button.setStyleSheet('background:#176b57; border:2px solid #34d399;')
                button.setEnabled(False)
            elif i in self.ai:
                button.setText(f'{label_for(i)}\nIA')
                button.setStyleSheet('background:#574293; border:2px solid #c4b5fd;')
                button.setEnabled(False)
            else:
                button.setText(f'{label_for(i)}\nT:{seat_score(i,"human")} · IA:{seat_score(i,"ai")}')
                button.setStyleSheet('')
                button.setEnabled(not self.finished and len(self.human) == len(self.ai))
        h = sum(seat_score(i, 'human') for i in self.human)
        a = sum(seat_score(i, 'ai') for i in self.ai)
        self.scores.setText(f'TÚ  {h}   :   {a}  IA')
        if self.finished:
            outcome = '¡Ganaste!' if h > a else 'La IA ganó' if a > h else 'Empate'
            self.status.setText(f'Partida finalizada: {outcome}  ·  Pulsa «Nueva partida» para repetir.')
        else:
            self.status.setText(f'Tu turno: elige el asiento {len(self.human)+1} de {ROUNDS}. '
                                'Los números T e IA muestran el valor de cada asiento para cada jugador.')

    def pick_human(self, i: int):
        if self.finished or i in self.human or i in self.ai or len(self.human) != len(self.ai):
            return
        self.human += (i,)
        self.refresh()
        QApplication.processEvents()
        # Con 3 elecciones por jugador, tras el turno humano siempre responde la IA.
        move, value, stats, candidates = choose_ai_move(self.human, self.ai, self.depth.value())
        if move is not None:
            self.ai += (move,)
            self.metrics.setText(f'Nodos evaluados: {stats.nodes:,}   |   Cortes Alfa-Beta: {stats.prunes:,}')
            self.explanation.setText(
                f'La IA eligió {label_for(move)} (valor propio: {seat_score(move,"ai")}). '
                f'Minimax estima una utilidad de {value:+d} tras explorar respuestas posibles. '
                'El valor representa puntos de la IA menos puntos humanos; no es una probabilidad. '
                'Las preferencias de ambos jugadores son diferentes, por eso el asiento con más '
                'puntos inmediatos no siempre produce la mejor decisión futura.'
            )
            ordered = sorted(candidates, key=lambda x: (-x[1], x[0]))
            self.candidates.setText('\n'.join(
                f'{"★" if j == move else " "} {label_for(j):<4}  utilidad {v:+4d}  '
                f'(valor IA {seat_score(j,"ai")})' for j, v in ordered
            ))
        self.finished = len(self.human) == ROUNDS and len(self.ai) == ROUNDS
        self.refresh()

    def reset(self):
        self.human, self.ai, self.finished = (), (), False
        self.metrics.setText('Nodos: —   |   Podas: —')
        self.explanation.setText('Elige un asiento. La IA evaluará los espacios disponibles '
                                 'anticipando tus siguientes decisiones con Minimax y poda Alfa-Beta.')
        self.candidates.setText('Los valores de cada candidato aparecerán después de tu primera elección.')
        self.refresh()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(STYLE)
    window = MainWindow()
    window.reset()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
