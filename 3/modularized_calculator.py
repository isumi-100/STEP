#! /usr/bin/python3

def read_number(line, index): # 少数含め、数字を得る
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_mul(line, index):
    token = {'type': 'MUL'}
    return token, index + 1

def read_div(line, index):
    token = {'type': 'DIV'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_mul(line, index)
        elif line[index] == '/':
            (token, index) = read_div(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def calculate_mul_and_div(tokens):
    index = 0
    add_sub_div_tokens = []
    add_sub_tokens = []
    # 割り算と掛け算のループを分けないと、3*6/2などが正しくできない
    while index < len(tokens): # 掛け算のみを行うループ
        if tokens[index]['type'] == 'MUL':
            mul_answer = tokens[index - 1]['number'] * tokens[index + 1]['number']
            add_sub_div_tokens.pop(-1)
            add_sub_div_tokens.append({'type': 'NUMBER', 'number': mul_answer})
            index += 2            
        else:
            add_sub_div_tokens.append(tokens[index])
            index += 1

    index = 0
    while index < len(add_sub_div_tokens): # 割り算のみを行うループ
        if add_sub_div_tokens[index]['type'] == 'DIV':
            div_answer = add_sub_div_tokens[index - 1]['number'] / add_sub_div_tokens[index + 1]['number']
            add_sub_tokens.pop(-1)
            add_sub_tokens.append({'type': 'NUMBER', 'number': div_answer})
            index += 2            
        else:
            add_sub_tokens.append(add_sub_div_tokens[index])
            index += 1
    # print(add_sub_tokens)
    return add_sub_tokens

def calculate_add_sub(answer, operator, number):
    if operator == 'PLUS':
        answer += number
    elif operator == 'MINUS':
        answer -= number
    else:
        print('Invalid syntax')
        exit(1)
    return answer

def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    simpler_tokens = calculate_mul_and_div(tokens)
    index = 0
    while index < len(simpler_tokens):
        if tokens[index]['type'] == 'NUMBER':
            answer = calculate_add_sub(answer, simpler_tokens[index - 1]['type'], simpler_tokens[index]['number'])
        index += 1
    return answer

def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("1.0*2.1-3")
    test("1.0+2.1/3")
    test("1.0*2.1+2.1/3")
    test("1.0*2.1/3")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)