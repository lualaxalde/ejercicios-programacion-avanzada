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

class Producto:
    def __init__(self, codigo_barras, nombre, precio, stock_disponible):
        self.id = codigo_barras
        self.nombre = nombre
        self.precio = precio
        self.stock = stock_disponible

    @property
    def precio(self):
        return self._precio
    
    @precio.setter
    def precio(self, precio):
        if precio<0:
            raise ValueError("el precio no puede ser negativo")
        self._precio= precio
    

    @property
    def stock(self):
        return self._stock

    # Validamos que el precio no pueda ser negativo usando el setter
    @stock.setter
    def stock(self, stock):
        if stock < 0:
            raise ValueError("el stock no puede ser negativo.")
        self._stock = stock
    

    def __str__(self):
        return f"[ID: {self.id}] {self.nombre} - {self.stock} | ${self.precio:.2f}"
    
class Inventario:
  
    def __init__(self):
        self.productos = {}

    @log_operacion("agregar producto")
    def alta_producto(self, codigo_barras, nombre, precio, stock_disponible):
        if codigo_barras in self.productos:
            print(f"error: ya existe el producto {codigo_barras}.")
            return False
        
        try:
            nuevo_producto = Producto (codigo_barras, nombre, precio, stock_disponible)
            self.productos[codigo_barras] = nuevo_producto
            print(f"producto agregado al gestor: {nuevo_producto.nombre}")
            return True
        except ValueError as e:
            print(f"Error de validación: {e}")
            return False
        
    @log_operacion("listado de productos")
    def mostrar_inventario(self):
        if not self.productos:
            print("no hay productos registrados en el sistema en este momento.")
            return
        
        print("\n--- lista de productos ---")
        for producto in self.productos.values():
            print(producto)
        print("-----------------------")

    @log_operacion("actualizar stock o precio producto")
    def modificar_stock_o_precio(self, codigo_barras, nuevo_producto=None, nuevo_precio=None, nuevo_stock=None):
        if codigo_barras not in self.productos:
            print(f"error: no se encontró un producto con el código de barras: {codigo_barras}.")
            return False

        producto= self.productos[codigo_barras]
        
        try:
            if nuevo_producto:
                producto.nombre = nuevo_producto
            if nuevo_precio:
                producto.precio = nuevo_precio
            if nuevo_stock is not None:
                producto.stock = nuevo_stock  # Esto pasa por la validación del setter
            print(f"producto {codigo_barras} actualizado correctamente.")
            return True
        except ValueError as e:
            print(f"error de validación al actualizar: {e}")
            return False

    @log_operacion("baja de producto")
    def baja_producto(self, codigo_barras):
        if codigo_barras in self.productos:
            producto = self.productos.pop(codigo_barras)
            print(f"producto eliminado del sistema: {producto.nombre}")
            return True
        else:
            print(f"error: no se encontró un producto con el código {codigo_barras}.")
            return False

def mostrar_menu():
    print("\n" + "="*35)
    print(" SISTEMA ABM DE PRODUCTOS ")
    print("="*35)
    print("[1] Agregar producto (Alta)")
    print("[2] Mostrar productos (Lectura)")
    print("[3] Actualizar producto (Modificación)")
    print("[4] Eliminar producto (Baja)")
    print("[5] Salir")
    print("="*35)

def main():
    gestor = Inventario()
    
    # Cargamos un par de datos de prueba al iniciar
    gestor.alta_producto(1, "alfajor", 300, 250)
    gestor.alta_producto(2, "fideos", 2000, 100)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            try:
                codigo_barras = int(input("escanee código de barras: "))
                if codigo_barras in Inventario:
                    print(f"error: ya existe un producto con el código {codigo_barras}.")
                    continue
                nombre = input("ingrese nombre: ").strip()
                precio = float(input("ingrese precio: ").strip())

                stock = float(input("ingrese stock: "))
                gestor.agregar_producto(codigo_barras, nombre, precio, stock)
            except ValueError:
                print("error: el código debe ser entero y el precio debe ser un número válido.")

        elif opcion == "2":
            gestor.mostrar_inventario()

        elif opcion == "3":
            try:
                codigo_barras = int(input("ingrese código del producto a modificar: "))
                if codigo_barras not in Inventario:
                    print(f"error: no se encontró un producto con el código {codigo_barras}.")
                    continue
                nombre = input("nuevo producto (presione Enter para dejar sin cambios): ").strip()
                precio = input("nuevo precio (presione Enter para dejar sin cambios): ").strip()
                stock_str = input("nuevo stock (presione Enter para dejar sin cambios): ").strip()
                
                nombre = nombre if nombre else None
                precio = precio if precio else None
                stock = float(stock_str) if stock_str else None
                
                gestor.modificar_stock_o_precio(codigo_barras, nombre, precio, stock)
            except ValueError:
                print("error: el codigo y el stock ingresados deben ser valores numéricos válidos.")

        elif opcion == "4":
            try:
                codigo_barras = int(input("ingrese código del producto a eliminar: "))
                gestor.baja_producto(codigo_barras)
            except ValueError:
                print("error: el código debe ser un número entero.")

        elif opcion == "5":
            print("Saliendo del sistema... ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione un número del 1 al 5.")


if __name__ == "__main__":
    main()