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

def read_begin(line, index):
    token = {'type': 'BEGIN'}
    return token, index + 1

def read_end(line, index):
    token = {'type': 'END'}
    return token, index + 1

def read_abs(line, index):
    token = {'type': 'ABS'}
    return token, index + 3

def read_int(line, index):
    token = {'type': 'INT'}
    return token, index + 3

def read_round(line, index):
    token = {'type': 'ROUND'}
    return token, index + 5

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
        elif line[index] == '(':
            (token, index) = read_begin(line, index)
        elif line[index] == ')':
            (token, index) = read_end(line, index)
        elif line[index: index+3] == 'abs':
            (token, index) = read_abs(line, index)
        elif line[index: index+3] == 'int':
            (token, index) = read_int(line, index)
        elif line[index: index+5] == 'round':
            (token, index) = read_round(line, index)            
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
            add_sub_div_tokens.pop(-1) #tokens[index-1]がelseの方を通りすでに格納されてしまっているので、除去する
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

def gain_group_from_tokens(tokens, index):
    group = []
    begin_counter = 1
    end_counter = 0
    while index < len(tokens) and begin_counter != end_counter:
        if tokens[index]['type'] == 'BEGIN':
            begin_counter += 1
        elif tokens[index]['type'] == 'END':
            end_counter += 1
        group.append(tokens[index])
        index += 1
    group.pop(-1)
    return group, index

def calculate_in_groups(tokens):
    index = 0
    simpler_tokens = []
    while index < len(tokens):
        if tokens[index]['type'] == 'BEGIN':
            group, index= gain_group_from_tokens(tokens, index+1)
            grouped = evaluate(group)
            simpler_tokens.append({'type': 'NUMBER', 'number': grouped})
        else:
            simpler_tokens.append(tokens[index])
            index += 1

    return simpler_tokens

def calculate_def(tokens):
    index = 0
    simpler_tokens = []
    while index < len(tokens):
        if tokens[index]['type'] == 'ABS' and tokens[index+1]['type'] == 'BEGIN':
            group, index = gain_group_from_tokens(tokens, index+2)
            grouped = evaluate(group)
            simpler_tokens.append({'type': 'NUMBER', 'number': abs(grouped)})
        elif tokens[index]['type'] == 'INT' and tokens[index+1]['type'] == 'BEGIN':
            group, index = gain_group_from_tokens(tokens, index+2)
            grouped = evaluate(group)
            simpler_tokens.append({'type': 'NUMBER', 'number': int(grouped)})
        elif tokens[index]['type'] == 'ROUND' and tokens[index+1]['type'] == 'BEGIN':
            group, index = gain_group_from_tokens(tokens, index+2)
            grouped = evaluate(group)
            simpler_tokens.append({'type': 'NUMBER', 'number': round(grouped)})
        else:
            simpler_tokens.append(tokens[index])
            index += 1
    return simpler_tokens
            

def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    only_number_tokens = calculate_def(tokens)
    simpler_tokens = calculate_in_groups(only_number_tokens)
    # print(simpler_tokens)
    add_sub_tokens = calculate_mul_and_div(simpler_tokens)
    index = 0
    while index < len(add_sub_tokens):
        if add_sub_tokens[index]['type'] == 'NUMBER':
            answer = calculate_add_sub(answer,  add_sub_tokens[index - 1]['type'],  add_sub_tokens[index]['number'])
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
    test("1")
    test("1+2")
    test("1.0+2.1-3")
    test("1.0*2.1-3")
    test("1.0+2.1/3")
    test("1.0*2.1+2.1/3")
    test("1.0*2.1/3")
    test("(1.0+2.1)*3")
    test("(1.0+2.1)*3+4/2+5*2")
    test("((1.0+2.1)+3)*2")
    test("abs(-1.0)")
    test("int(3.5)")
    test("round(3.5)")
    test("12+abs(int(round(-1.55)+abs(int(-2.3+4))))")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)