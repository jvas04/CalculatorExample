class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        print("Resultado:", result)
        return result

    def subtract(self, a, b):
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        print("Resultado:", result)
        return result

    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        print("Resultado:", result)
        return result

    def divide(self, a, b):
        if b == 0:
            print("Error: División por cero")
            return None
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        print("Resultado:", result)
        return result

    def show_history(self):
        print("\n--- Historial ---")
        for record in self.history:
            print(record)

    def save_history(self, filename):
        try:
            with open(filename, "w") as file:
                for record in self.history:
                    file.write(record + "\n")
            print("Historial guardado correctamente.")
        except Exception as e:
            print("Error al guardar historial:", e)


# ==============================
# Código ejecutable directamente
# ==============================

if __name__ == "__main__":
    calc = Calculator()

    while True:
        print("\n--- Calculadora ---")
        print("1. Sumar")
        print("2. Restar")
        print("3. Multiplicar")
        print("4. Dividir")
        print("5. Ver historial")
        print("6. Guardar historial")
        print("7. Salir")

        option = input("Seleccione una opción: ")

        if option == "7":
            print("Saliendo...")
            break

        if option in ["1", "2", "3", "4"]:
            try:
                a = float(input("Ingrese el primer número: "))
                b = float(input("Ingrese el segundo número: "))
            except ValueError:
                print("Entrada inválida.")
                continue

            if option == "1":
                calc.add(a, b)
            elif option == "2":
                calc.subtract(a, b)
            elif option == "3":
                calc.multiply(a, b)
            elif option == "4":
                calc.divide(a, b)

        elif option == "5":
            calc.show_history()

        elif option == "6":
            filename = input("Ingrese el nombre del archivo: ")
            calc.save_history(filename)

        else:
            print("Opción inválida.")
