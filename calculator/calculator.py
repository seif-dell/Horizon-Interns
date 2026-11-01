"""Command-Line Calculator with advanced math operations."""

import math

history = []

MENU = """
========== ADVANCED CALCULATOR ==========
 Basic            Advanced
 1. Add           6. Power (a ^ b)
 2. Subtract      7. Square root
 3. Multiply      8. Nth root
 4. Divide        9. Factorial
 5. Modulo       10. Logarithm (any base)
                 11. Natural log (ln)
 Trigonometry    13. Percentage (a% of b)
 12. sin / cos / tan (degrees)

 H. Show history   C. Clear history   Q. Quit
=========================================
"""


def read_number(prompt):
    """Keep asking until the user enters a valid number."""
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("  ! Invalid number, please try again.")


def fmt(x):
    """Show integers without a trailing .0."""
    if isinstance(x, float) and x.is_integer() and abs(x) < 1e15:
        return str(int(x))
    return f"{x:.10g}" if isinstance(x, float) else str(x)


def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


def modulo(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot take modulo by zero.")
    return a % b


def power(a, b):
    result = a ** b
    if isinstance(result, complex):
        raise ValueError("Result is not a real number.")
    return result


def square_root(a):
    if a < 0:
        raise ValueError("Cannot take the square root of a negative number.")
    return math.sqrt(a)


def nth_root(a, n):
    if n == 0:
        raise ValueError("Root degree cannot be zero.")
    if a < 0 and n % 2 == 0:
        raise ValueError("Even root of a negative number is not real.")
    if a < 0:
        return -((-a) ** (1 / n))
    return a ** (1 / n)


def factorial(a):
    if a < 0 or not float(a).is_integer():
        raise ValueError("Factorial needs a non-negative integer.")
    if a > 1000:
        raise ValueError("Number too large (max 1000).")
    return math.factorial(int(a))


def logarithm(a, base):
    if a <= 0:
        raise ValueError("Logarithm needs a positive number.")
    if base <= 0 or base == 1:
        raise ValueError("Base must be positive and not equal to 1.")
    return math.log(a, base)


def natural_log(a):
    if a <= 0:
        raise ValueError("ln needs a positive number.")
    return math.log(a)


def trig(func, degrees):
    rad = math.radians(degrees)
    if func == "sin":
        return math.sin(rad)
    if func == "cos":
        return math.cos(rad)
    if func == "tan":
        if abs(math.cos(rad)) < 1e-12:
            raise ValueError("tan is undefined at this angle.")
        return math.tan(rad)
    raise ValueError("Unknown function.")


def percentage(p, total):
    return p / 100 * total


def record(expression, result):
    entry = f"{expression} = {fmt(result)}"
    history.append(entry)
    print(f"  => {entry}")


def show_history():
    if not history:
        print("  (history is empty)")
        return
    print("\n--- History ---")
    for i, entry in enumerate(history, 1):
        print(f" {i}. {entry}")


def run_choice(choice):
    if choice in {"1", "2", "3", "4", "5", "6"}:
        a = read_number("  First number : ")
        b = read_number("  Second number: ")
        ops = {
            "1": (add, "+"), "2": (subtract, "-"), "3": (multiply, "*"),
            "4": (divide, "/"), "5": (modulo, "%"), "6": (power, "^"),
        }
        func, sym = ops[choice]
        record(f"{fmt(a)} {sym} {fmt(b)}", func(a, b))
    elif choice == "7":
        a = read_number("  Number: ")
        record(f"sqrt({fmt(a)})", square_root(a))
    elif choice == "8":
        a = read_number("  Number: ")
        n = read_number("  Root degree (n): ")
        record(f"{fmt(n)}th root of {fmt(a)}", nth_root(a, n))
    elif choice == "9":
        a = read_number("  Number: ")
        record(f"{fmt(a)}!", factorial(a))
    elif choice == "10":
        a = read_number("  Number: ")
        base = read_number("  Base: ")
        record(f"log base {fmt(base)} of {fmt(a)}", logarithm(a, base))
    elif choice == "11":
        a = read_number("  Number: ")
        record(f"ln({fmt(a)})", natural_log(a))
    elif choice == "12":
        func = input("  Function (sin/cos/tan): ").strip().lower()
        if func not in {"sin", "cos", "tan"}:
            raise ValueError("Please choose sin, cos or tan.")
        angle = read_number("  Angle in degrees: ")
        record(f"{func}({fmt(angle)}°)", trig(func, angle))
    elif choice == "13":
        p = read_number("  Percentage: ")
        total = read_number("  Of number : ")
        record(f"{fmt(p)}% of {fmt(total)}", percentage(p, total))
    else:
        print("  ! Invalid option.")


def main():
    print("Welcome to the Advanced Calculator!")
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip().lower()
        if choice == "q":
            print("Goodbye!")
            break
        if choice == "h":
            show_history()
        elif choice == "c":
            history.clear()
            print("  History cleared.")
        else:
            try:
                run_choice(choice)
            except (ValueError, ZeroDivisionError, OverflowError) as err:
                print(f"  ! Error: {err}")


if __name__ == "__main__":
    main()
