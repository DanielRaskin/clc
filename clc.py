def get_number(s, position):
    i = position + 1 if s[position] in ('+', '-') else position
    dot = False
    while i < len(s) and (s[i] == '.' or ord(s[i]) in range(ord('0'), ord('9') + 1)):
        if s[i] == '.':
            if dot:
                raise Exception('Number format error')
            dot = True
        i += 1
    return float(s[position : i]) if dot else int(s[position : i]), i


def get_close_bracket_position(s, position, s_len):
    bracket = 1
    i = position + 1
    while bracket > 0:
        if i == s_len:
            raise Exception('Brackets error')
        if s[i] == '(':
            bracket += 1
        if s[i] == ')':
            bracket -= 1
        i += 1
    return i - 1


def get_level(operation):
    if operation not in ('+', '-', '*', '/', '^'):
        raise Exception('Invalid operation sign')
    return 3 if operation == '^' else 2 if operation in ('*', '/') else 1


def calculate(operand1, operation, operand2):
    if operation is None:
        return operand2
    if operation not in ('+', '-', '*', '/', '^'):
        raise Exception('Invalid operation sign')
    if operation == '+':
        return operand1 + operand2
    if operation == '-':
        return operand1 - operand2
    if operation == '*':
        return operand1 * operand2
    if operation == '/':
        return operand1 / operand2
    if operation == '^':
        return operand1 ** operand2


def clc(s):
    result1, result2, operation1, operation2 = None, None, None, None
    result = 0
    operation = '+'
    level = 1
    s_len = len(s)
    i = 0
    while i < s_len:
        if s[i] == ' ':
            i += 1
            continue

        if operation is None:
            operation = s[i]
            i += 1
            continue

        if s[i] == '(':
            j = get_close_bracket_position(s, i, s_len)
            number = clc(s[i + 1 : j])
            i = j + 1
        else:
            number, i = get_number(s, i)

        new_level = get_level(operation)
        if new_level == level:
            prev_result = result
        if new_level > level:
            if level == 1:
                result1 = prev_result
                operation1 = prev_operation
            else:
                result2 = prev_result
                operation2 = prev_operation
            prev_result = prev_number
        if new_level < level:
            if new_level == 1:
                prev_result = calculate(result1, operation1, calculate(result2, operation2, result))
                operation1 = None
            else:
                prev_result = calculate(result2, operation2, result)
            operation2 = None
        result = calculate(prev_result, operation, number)
        level = new_level
        prev_number = number
        prev_operation = operation
        operation = None

    if operation is not None:
        raise Exception('Operand not found')

    return calculate(result1, operation1, calculate(result2, operation2, result))


if __name__ == '__main__':
    while True:
        s = input('Enter expression to calculate, q for quit >>> ')
        if s == 'q':
            break
        try:
            print('Result is: ' + str(clc(s)))
        except Exception as ex:
            print(ex)
