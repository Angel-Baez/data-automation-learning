#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔢 Calculadora Básica - Semana 1
Proyecto del roadmap Data + Automation Engineer

Autor: Angel Baez
Fecha: Octubre 2025
Descripción: Calculadora interactiva con operaciones básicas
             y manejo de errores
"""


def mostrar_menu():
    """Muestra el menú principal de la calculadora"""
    print("\n" + "=" * 30)
    print("🔢 CALCULADORA BÁSICA")
    print("=" * 30)
    print("1. ➕ Sumar")
    print("2. ➖ Restar")
    print("3. ✖️  Multiplicar")
    print("4. ➗ Dividir")
    print("5. 🚪 Salir")
    print("-" * 30)


def obtener_numeros():
    """
    Solicita y valida dos números del usuario
    Returns:
        tuple: (numero1, numero2) o None si hay error
    """
    try:
        print("\nIngresa los números para la operación:")
        num1 = float(input("Primer número: "))
        num2 = float(input("Segundo número: "))
        return num1, num2
    except ValueError:
        print("❌ Error: Por favor ingresa números válidos")
        return None


def sumar(a, b):
    """Realiza la suma de dos números"""
    return a + b


def restar(a, b):
    """Realiza la resta de dos números"""
    return a - b


def multiplicar(a, b):
    """Realiza la multiplicación de dos números"""
    return a * b


def dividir(a, b):
    """
    Realiza la división de dos números
    Args:
        a (float): Dividendo
        b (float): Divisor
    Returns:
        float: Resultado de la división
    Raises:
        ZeroDivisionError: Si el divisor es cero
    """
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a / b


def obtener_opcion_menu():
    """
    Obtiene y valida la opción del menú seleccionada por el usuario
    Returns:
        int: Opción válida del menú (1-5)
    """
    while True:
        try:
            opcion = int(input("Elige una operación (1-5): "))
            if 1 <= opcion <= 5:
                return opcion
            else:
                print("❌ Por favor elige una opción entre 1 y 5")
        except ValueError:
            print("❌ Por favor ingresa un número válido")


def realizar_operacion(opcion, num1, num2):
    """
    Ejecuta la operación matemática según la opción elegida
    Args:
        opcion (int): Número de operación (1-4)
        num1 (float): Primer número
        num2 (float): Segundo número
    Returns:
        float: Resultado de la operación
    """
    operaciones = {
        1: (sumar, "suma", "➕"),
        2: (restar, "resta", "➖"),
        3: (multiplicar, "multiplicación", "✖️"),
        4: (dividir, "división", "➗"),
    }

    funcion, nombre, simbolo = operaciones[opcion]

    try:
        resultado = funcion(num1, num2)
        print(f"\n✅ Resultado de la {nombre}:")
        print(f"   {num1} {simbolo} {num2} = {resultado}")
        return resultado
    except ZeroDivisionError as e:
        print(f"❌ Error: {e}")
        return None


def preguntar_continuar():
    """
    Pregunta al usuario si desea realizar otra operación
    Returns:
        bool: True si quiere continuar, False si no
    """
    while True:
        continuar = input("\n¿Deseas realizar otra operación? (s/n): ").lower().strip()
        if continuar in ["s", "si", "sí", "y", "yes"]:
            return True
        elif continuar in ["n", "no"]:
            return False
        else:
            print("❌ Por favor responde con 's' para sí o 'n' para no")


def main():
    """Función principal de la calculadora"""
    print("🎉 ¡Bienvenido a la Calculadora Básica!")
    print("Proyecto: Data + Automation Engineer Journey - Semana 1")

    while True:
        mostrar_menu()
        opcion = obtener_opcion_menu()

        if opcion == 5:
            print("\n👋 ¡Gracias por usar la calculadora!")
            print("🚀 Continúa con tu journey de Data Engineering")
            break

        # Obtener números del usuario
        numeros = obtener_numeros()
        if numeros is None:
            continue  # Volver al menú si hubo error en la entrada

        num1, num2 = numeros

        # Realizar la operación
        resultado = realizar_operacion(opcion, num1, num2)

        # Preguntar si quiere continuar (solo si la operación fue exitosa)
        if resultado is not None:
            if not preguntar_continuar():
                print("\n👋 ¡Gracias por usar la calculadora!")
                print("🚀 Continúa con tu journey de Data Engineering")
                break


if __name__ == "__main__":
    main()
