
# Ворог
class EnemyTank(Tank):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 0, 0))  # Червоний танк

    def update(self):
        # Проста логіка руху ворога (постійно вниз)
        self.move(0, 0.5)
