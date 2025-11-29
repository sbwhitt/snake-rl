class Keys:
    def __init__(self) -> None:
        self.down: dict[int, bool] = {}

    def is_down(self, key: int) -> None:
        return self.down.get(key)

    def handle_down(self, key: int) -> None:
        if not self.down.get(key) or not self.down[key]:
            self.down[key] = True

    def handle_up(self, key: int) -> None:
        if not self.down.get(key) or self.down[key]:
            self.down[key] = False
