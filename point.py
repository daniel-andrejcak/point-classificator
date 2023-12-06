class Point:
    def __init__(self, x: int, y: int, color: str) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.coords = [self.x, self.y]

    def __len__(self):
        return len(self.coords)

    def __getitem__(self, i):
        return self.coords[i]


    def __hash__(self) -> int:
        prime_x = 31
        prime_y = 37
        
        hash_value = (self.x ^ prime_x) * 997 + (self.y ^ prime_y)
        
        return hash_value
            

    def __eq__(self, __value: object) -> bool:
        return self.x == __value.x and self.y == __value.y
