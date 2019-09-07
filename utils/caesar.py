class Caesar:

    def __init__(self):

        self.characters = "".join(
            map(
                chr, 
                range(
                    ord(" "), 
                    ord("я") + 1
                )
            )
        )

        

    def encode(self, string: str, pos: int) -> str:

        return string.translate(
            str.maketrans(
                self.characters, 
                self.characters[pos:] + self.characters[:pos]
            )
        )

    def decode(self, string: str, pos: int) -> str:

        return string.translate(
            str.maketrans(
                self.characters[pos:] + self.characters[:pos], 
                self.characters
            )
        )
    
    def handle_inputs(self):

        while True:

            selection = int(
                input(
                    "Зашифровать (1), Расшифровать (2): "
                )
            )

            if selection not in (1, 2):

                print(
                    "Пожалуйста, введите 1 или 2"
                )
            
            elif selection == 1:

                st = input(
                    "Строка для зашифровки: "
                )

                mov = int(
                    input(
                        "Сдвиг: "
                    )
                )

                print(
                    self.encode(
                        st,
                        mov
                    )
                )
            
            else:

                st = input(
                    "Строка для расшифровки: "
                )

                mov = int(
                    input(
                        "Сдвиг: "
                    )
                )

                print(
                    self.decode(
                        st,
                        mov
                    )
                )

if __name__ == "__main__":

    Caesar()