# ============================================================
# Data Structure and Algorithm Assignment
# Stack-Based Mathematical Expression Evaluator
# ============================================================

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0


def precedence(operator):
    if operator in ('+', '-'):
        return 1
    if operator in ('*', '/'):
        return 2
    return 0


def apply_operator(operator, left, right):
    if operator == '+':
        return left + right
    elif operator == '-':
        return left - right
    elif operator == '*':
        return left * right
    elif operator == '/':
        if right == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return left / right
    raise ValueError("Unknown operator: " + operator)


def evaluate_expression(expression):
    values = Stack()
    operators = Stack()
    i = 0

    while i < len(expression):
        if expression[i].isspace():
            i += 1
            continue

        if expression[i].isdigit() or expression[i] == '.':
            number = ""
            while (i < len(expression) and
                   (expression[i].isdigit() or expression[i] == '.')):
                number += expression[i]
                i += 1

            if number.count('.') > 1:
                raise ValueError("Invalid number: " + number)

            values.push(float(number) if '.' in number else int(number))
            continue

        if expression[i] == '(':
            operators.push(expression[i])

        elif expression[i] == ')':
            while not operators.is_empty() and operators.peek() != '(':
                operator = operators.pop()
                right = values.pop()
                left = values.pop()
                values.push(apply_operator(operator, left, right))

            if operators.is_empty():
                raise ValueError("Mismatched parentheses.")
            operators.pop()

        elif expression[i] in '+-*/':
            while (not operators.is_empty()
                   and operators.peek() != '('
                   and precedence(operators.peek()) >= precedence(expression[i])):
                operator = operators.pop()
                right = values.pop()
                left = values.pop()
                values.push(apply_operator(operator, left, right))
            operators.push(expression[i])

        else:
            raise ValueError("Invalid character: " + expression[i])

        i += 1

    while not operators.is_empty():
        if operators.peek() == '(':
            raise ValueError("Mismatched parentheses.")
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        values.push(apply_operator(operator, left, right))

    result = values.pop()

    if not values.is_empty():
        raise ValueError("Invalid expression.")

    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result


def process_input_file(input_file, output_file):
    expressions = []

    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if set(line) == {'-'}:
                continue
            expressions.append(line)

    with open(output_file, "w", encoding="utf-8") as file:
        for index, expression in enumerate(expressions):
            try:
                result = evaluate_expression(expression)
                file.write(str(result))
            except Exception as error:
                file.write("Error: " + str(error))

            if index < len(expressions) - 1:
                file.write("\n----------------\n")


if __name__ == "__main__":
    process_input_file("input.txt", "output.txt")
    print("Expression evaluation completed successfully.")
    print("Results have been saved to output.txt.")
