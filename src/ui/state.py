from enum import Enum, auto


class State(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    INSTRUCTION = auto()
    HIGHSCORE = auto()
    PAUSE_MENU = auto()
    END_MENU = auto()


class StateMachine:
    def __init__(self) -> None:
        self.current_state = State.MAIN_MENU

    def change_state(self, state: State) -> None:
        self.current_state = state
