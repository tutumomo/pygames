class Level:
    def __init__(self, number):
        self.number = number
        self.layouts = {
            1: [
                "BBBBBBBBBBBBBBBBBBBBBBBB",
                "B                      B",
                "B  S  B  S  B  S  B   B",
                "B     B     B     B   B",
                "B  B  S  B  S  B  S   B",
                "B     B     B     B   B",
                "B  S  B  S  B  S  B   B",
                "B                      B",
                "B    E     E     E     B",
                "B                      B",
                "B  B     B  B     B   B",
                "B    B B    B B    B   B",
                "B     B      B     B   B",
                "B  B     B      B      B",
                "B    B B    B B    B   B",
                "B     B      B     B   B",
                "B  BBBBB  BBBBB  BBBB B",
                "B                      B",
                "BBBBBBBB    P   BBBBBBB",
            ],
            2: [
                "SSSSSSSSSSSSSSSSSSSSSSSS",
                "S                      S",
                "S  B  S  B  S  B  S   S",
                "S     S     S     S   S",
                "S  S  B  S  B  S  B   S",
                "S     S     S     S   S",
                "S  B  S  B  S  B  S   S",
                "S                      S",
                "S    E     E     E     S",
                "S                      S",
                "S  S     S  S     S   S",
                "S    S S    S S    S   S",
                "S     S      S     S   S",
                "S  S     S      S      S",
                "S    S S    S S    S   S",
                "S     S      S     S   S",
                "S  SSSSS  SSSSS  SSSS S",
                "S                      S",
                "SSSSSSSS    P   SSSSSSS",
            ]
        }

    def get_layout(self):
        # Return the layout for the current level, or level 1 if not found
        return self.layouts.get(self.number, self.layouts[1])

    def get_enemy_count(self):
        # Count number of enemy spawn points in current level
        layout = self.get_layout()
        return sum(row.count('E') for row in layout)
