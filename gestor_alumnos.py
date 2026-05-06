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

class Alumno:
    def __init__(self, id_alumno, nombre, curso, promedio):
        self._id = id_alumno
        self.nombre = nombre
        self.curso= curso
        self.promedio= promedio


    @property
    def id(self):
        return self._id

    @property
    def promedio(self):
        return self._promedio

    # Validamos que el precio no pueda ser negativo usando el setter
    @promedio.setter
    def promedio(self, valor):
        if valor < 0:
            raise ValueError("el promedio no puede ser negativo.")
        self._promedio= valor

    def __str__(self):
        return f"[ID: {self._id}] {self.nombre} - {self.curso} | ${self.promedio:.2f}"
    
class GestorAlumnos:
  
    def __init__(self):
        self.alumnos = {}

    @log_operacion("agregar alumno")
    def agregar_alumno(self, id_alumno, nombre, curso, promedio):
        if id_alumno in self.alumnos:
            print(f"error: ya existe el alumno {id_alumno}.")
            return False
        
        try:
            nuevo_alumno = Alumno (id_alumno, nombre, curso, promedio)
            self.alumnos[id_alumno] = nuevo_alumno
            print(f"alumno agregado al gestor: {nuevo_alumno.nombre}")
            return True
        except ValueError as e:
            print(f"Error de validación: {e}")
            return False
        
    @log_operacion("listado de alumnos")
    def listar_alumnos(self):
        if not self.alumnos:
            print("no hay alumnos registrados en el sistema en este momento.")
            return
        
        print("\n--- lista de alumnos ---")
        for alumno in self.alumnos.values():
            print(alumno)
        print("-----------------------")

    @log_operacion("actualizar alumno")
    def actualizar_alumno(self, id_alumno, nuevo_alumno=None, nuevo_curso=None, nuevo_promedio=None):
        if id_alumno not in self.alumnos:
            print(f"error: no se encontró un alumno con el ID: {id_alumno}.")
            return False

        alumno= self.alumnos[id_alumno]
        
        try:
            if nuevo_alumno:
                alumno.nombre = nuevo_alumno
            if nuevo_curso:
                alumno.curso = nuevo_curso
            if nuevo_promedio is not None:
                alumno.promedio = nuevo_promedio  # Esto pasa por la validación del setter
            print(f"alumno {id_alumno} actualizado correctamente.")
            return True
        except ValueError as e:
            print(f"error de validación al actualizar: {e}")
            return False

    @log_operacion("baja de alumno")
    def eliminar_alumno(self, id_alumno):
        if id_alumno in self.alumnos:
            alumno = self.alumnos.pop(id_alumno)
            print(f"alumno eliminado del sistema: {alumno.nombre}")
            return True
        else:
            print(f"error: no se encontró un alumno con el ID {id_alumno}.")
            return False

def mostrar_menu():
    print("\n" + "="*35)
    print(" SISTEMA ABM DE ALUMNOS ")
    print("="*35)
    print("[1] Agregar Alumno (Alta)")
    print("[2] Mostrar Alumnos (Lectura)")
    print("[3] Actualizar Alumno (Modificación)")
    print("[4] Eliminar Alumno (Baja)")
    print("[5] Salir")
    print("="*35)

def main():
    gestor = GestorAlumnos()
    
    # Cargamos un par de datos de prueba al iniciar
    gestor.agregar_alumno(1, "jorgito", "2do b", 20)
    gestor.agregar_alumno(2, "martina", "5to a", 10)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            try:
                id_alumno = int(input("ingrese ID numérico del alumno: "))
                if id_alumno in gestor.alumnos:
                    print(f"error: ya existe un alumno con el ID {id_alumno}.")
                    continue
                nombre = input("ingrese nombre: ").strip()
                curso = input("ingrese curso: ").strip()
                promedio = float(input("ingrese promedio: "))
                gestor.agregar_alumno(id_alumno, nombre, curso, promedio)
            except ValueError:
                print("error: el ID debe ser entero y el promedio debe ser un número válido.")

        elif opcion == "2":
            gestor.listar_alumnos()

        elif opcion == "3":
            try:
                id_alumno = int(input("ingrese ID del alumno a modificar: "))
                if id_alumno not in gestor.alumnos:
                    print(f"error: no se encontró un alumno con el ID {id_alumno}.")
                    continue
                nombre = input("nuevo alumno (presione Enter para dejar sin cambios): ").strip()
                curso = input("nuevo curso (presione Enter para dejar sin cambios): ").strip()
                promedio_str = input("nuevo promedio (presione Enter para dejar sin cambios): ").strip()
                
                nombre = nombre if nombre else None
                curso = curso if curso else None
                promedio = float(promedio_str) if promedio_str else None
                
                gestor.actualizar_alumno(id_alumno, nombre, curso, promedio)
            except ValueError:
                print("error: el ID y promedio ingresados deben ser valores numéricos válidos.")

        elif opcion == "4":
            try:
                id_alumno = int(input("ingrese ID del alumno a eliminar: "))
                gestor.eliminar_alumno(id_alumno)
            except ValueError:
                print("error: el ID debe ser un número entero.")

        elif opcion == "5":
            print("Saliendo del sistema... ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione un número del 1 al 5.")


if __name__ == "__main__":
    main()
