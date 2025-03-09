class Hello:
    def __init__(self):
        self.name = "World"

    def say_hello(self):
        print(f"Hello, {self.name}!")


if __name__ == "__main__":
    hello = Hello()
    hello.say_hello()
