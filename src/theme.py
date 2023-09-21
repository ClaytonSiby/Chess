from color import Color

class Theme:
    def __init__(self, light_background, dark_background, light_trace, dark_trace, light_moves, dark_moves):
        self.background_color = Color(light_background, dark_background)
        self.trace = Color(light_trace, dark_trace)
        self.moves = Color(light_moves, dark_moves)
