import functools

def log_operacion(operacion):
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"\n>>> Iniciando operación: {operacion}")
            resultado = func(*args, **kwargs)
            print(f">>> Operación '{operacion}' finalizada exitosamente.")
            return resultado
        return wrapper
    return decorador

class Mascota:
    def __init__(self, numero_ficha, nombre, especie, peso_kg):
        self._id = numero_ficha
        self.nombre = nombre
        self.especie= especie
        self.peso_kg= peso_kg


    @property
    def id(self):
        return self._id

    @property
    def peso_kg(self):
        return self._peso_kg

    # Validamos que el precio no pueda ser negativo usando el setter
    @peso_kg.setter
    def peso_kg(self, valor):
        if valor <= 0:
            raise ValueError("el peso no puede ser negativo o igual a cero.")
        self._peso_kg = valor

    def __str__(self):
        return f"[ID: {self._id}] {self.nombre} - {self.especie} | {self.peso_kg:.2f}"
    
class Veterinaria:
  
    def __init__(self):
        self.mascotas = {}

    @log_operacion("agregar mascota")
    def agregar_mascota (self, numero_ficha, nombre, especie, peso_kg):
        if numero_ficha in self.mascotas:
            print(f"error: ya existe la mascota {numero_ficha}.")
            return False
        
        try:
            nueva_mascota = Mascota (numero_ficha, nombre, especie, peso_kg)
            self.mascotas[numero_ficha] = nueva_mascota
            print(f"mascota agregada al gestor: {nueva_mascota.nombre}")
            return True
        except ValueError as e:
            print(f"Error de validación: {e}")
            return False
        
    @log_operacion("listado de mascotas")
    def listar_mascotas(self):
        if not self.mascotas:
            print("no hay mascotas registradas en el sistema en este momento.")
            return
        
        print("\n--- lista de mascotas ---")
        for mascota in self.mascotas.values():
            print(mascota)
        print("-----------------------")

    @log_operacion("actualizar mascota")
    def actualizar_mascota(self, numero_ficha, nuevo_nombre= None, nuevo_especie=None, nuevo_peso_kg=None):
        if numero_ficha not in self.mascotas:
            print(f"error: no se encontró una mascota con el número de ficha: {numero_ficha}.")
            return False

        mascota= self.mascotas[numero_ficha]
        
        try:
            if nuevo_nombre:
                mascota.nombre = nuevo_nombre
            if nuevo_especie:
                mascota.especie = nuevo_especie
            if nuevo_peso_kg is not None:
                mascota.peso_kg = nuevo_peso_kg  # Esto pasa por la validación del setter
            print(f"mascota {numero_ficha} actualizado correctamente.")
            return True
        except ValueError as e:
            print(f"error de validación al actualizar: {e}")
            return False
        
    @log_operacion("listar por especie")
    def listar_por_especie(self, especie_buscada):
        coincidencias = [m for m in self.mascotas.values() if m.especie.lower() == especie_buscada.lower()]
    
        if not coincidencias:
            print(f"no se encontraron mascotas de la especie '{especie_buscada}'.")
            return
    
        print(f"\n--- mascotas de la especie '{especie_buscada}' ---")
        for mascota in coincidencias:
            print(mascota)
    print("-----------------------")

    @log_operacion("baja de mascota")
    def eliminar_mascota(self, numero_ficha):
        if numero_ficha in self.mascotas:
            mascota = self.mascotas.pop(numero_ficha)
            print(f"mascota eliminada del sistema: {mascota.nombre}")
            return True
        else:
            print(f"error: no se encontró una mascota con el número de ficha {numero_ficha}.")
            return False

def mostrar_menu():
    print("\n" + "="*35)
    print(" SISTEMA ABM DE VETERINARIA ")
    print("="*35)
    print("[1] Agregar mascota (Alta)")
    print("[2] Mostrar mascotas (Lectura)")
    print("[3] Actualizar mascota (Modificación)")
    print("[4] Eliminar mascota (Baja)")
    print("[5] Listar por especie")
    print("[6] Salir")
    print("="*35)

def main():
    gestor = Veterinaria()
    
    # Cargamos un par de datos de prueba al iniciar
    gestor.agregar_mascota(1, "miel", "gato", 5)
    gestor.agregar_mascota(2, "fifi", "gato", 4)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            try:
                numero_ficha = int(input("ingrese número de ficha de la mascota: "))
                if numero_ficha in gestor.mascotas:
                    print(f"error: ya existe una mascota con el número de ficha {numero_ficha}.")
                    continue
                nombre = input("ingrese nombre: ").strip()
                especie = input("ingrese especie: ").strip()
                peso_kg = float(input("ingrese peso (kg): "))
                gestor.agregar_mascota(numero_ficha, nombre, especie, peso_kg)
            except ValueError:
                print("error: el número de ficha ser entero y el peso debe ser un número válido.")

        elif opcion == "2":
            gestor.listar_mascotas()

        elif opcion == "3":
            try:
                numero_ficha = int(input("ingrese número de ficha a modificar: "))
                if numero_ficha not in gestor.mascotas:
                    print(f"error: no se encontró una mascota con el número de ficha {numero_ficha}.")
                    continue
                nombre = input("nueva mascota (presione Enter para dejar sin cambios): ").strip()
                especie = input("nueva especie (presione Enter para dejar sin cambios): ").strip()
                peso_kg_str = input("nuevo peso ingresado (presione Enter para dejar sin cambios): ").strip()
                
                nombre = nombre if nombre else None
                especie = especie if especie else None
                peso_kg = float(peso_kg_str) if peso_kg_str else None
                
                gestor.actualizar_mascota(numero_ficha, nombre, especie, peso_kg)
            except ValueError:
                print("error: el número de ficha y peso ingresados deben ser valores numéricos válidos.")

        elif opcion == "4":
            try:
                numero_ficha = int(input("ingrese número de ficha de la mascota a eliminar: "))
                gestor.eliminar_mascota(numero_ficha)
            except ValueError:
                print("error: el número de ficha debe ser un número entero.")

        elif opcion == "5":
            especie = input("ingrese especie a buscar (Perro/Gato): ").strip()
            gestor.listar_por_especie(especie)

        elif opcion == "6":
            print("Saliendo del sistema... ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione un número del 1 al 5.")


if __name__ == "__main__":
    main()