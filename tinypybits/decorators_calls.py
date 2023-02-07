class PowerInput:
    def power_input(self, t: int):
        print("im power input")

    def __call__(self, other):
        other.power_input = self.power_input
        print(f"Received {other}")
        return other


class H2Output:
    def h2_output(self, t: int):
        print("im h2 output")

    def __call__(self, other):
        other.h2_output = self.h2_output
        print(f"Received {other}")
        return other


@PowerInput()
@H2Output()
class Electrolyzer:
    def __init__(self):
        print("elect initialized")


electrolyzer = Electrolyzer()
electrolyzer.h2_output(t=1)
electrolyzer.power_input(t=1)
