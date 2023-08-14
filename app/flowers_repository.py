from pydantic import BaseModel

class Flower(BaseModel):
    name: str
    count: int
    cost: int
    id: int = 0


class FlowersRepository:
    flowers: list[Flower]

    def __init__(self):
        self.flowers = []
        self.carts = []

    # необходимые методы сюда

    def get_all(self) -> list[Flower]:
        return self.flowers

    def get_one(self, id: int) -> Flower:
        for flower in self.flowers:
            if flower.id == id:
                return flower
        return None

    def minus_flower(self, id:int):
        for flower in self.flowers:
            if flower.id == id and flower.count != 0:
                flower.count -= 1

    def save(self, flower):
        flower.id = len(self.flowers) + 1
        self.flowers.append(flower)

    def get_next_id(self):
        return len(self.flowers) + 1

    def save_in_cart(self, flower_id, count):
        for flower in self.flowers:
            if flower.id == id and flower.count != 0:
                flower.count -= count
        self.carts.append(flower_id)

    def get_all_in_cart(self):
        return self.carts

    def get_by_id(self, flower_id):
        for i, flower in enumerate(self.flowers):
            if flower.id == flower_id:
                return self.flowers[i]