import argparse
#python main.py test.txt -t -o result.bin

def parse_line(line):
    line = line.strip()
    if not line:
        return None
    parts = line.split()
    cmd = parts[0]
    args = parts[1:]
    nums = []
    for a in args:
        a = a.rstrip(',')
        if a.startswith('r'):
            nums.append(int(a[1:]))
        elif a.startswith('0x'):
            nums.append(int(a, 16))
        else:
            nums.append(int(a))
    return cmd, nums

def to_ir(cmd, nums):
    if cmd == 'load_const':
        return {'op': 20, 'b': nums[0], 'c': nums[1]}
    elif cmd == 'read_mem':
        return {'op': 28, 'b': nums[0], 'c': nums[2], 'd': nums[1]}
    elif cmd == 'write_mem':
        return {'op': 12, 'b': nums[0], 'c': nums[1], 'd': nums[2]}
    elif cmd == 'shift_right':
        return {'op': 18, 'b': nums[1], 'c': nums[0]}

def encode(ir):
    op = ir['op']
    b = ir['b']
    c = ir['c']
    if op == 20:
        value = op + (b << 5) + (c << 10)
    elif op == 28:
        d = ir['d']
        value = op + (b << 5) + (c << 10) + (d << 15)
    elif op == 12:
        d = ir['d']
        value = op + (b << 5) + (c << 10) + (d << 15)
    elif op == 18:
        value = op + (b << 5) + (c << 10)
    else:
        value = 0
    return value.to_bytes(5, byteorder='little')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Путь к исходному файлу с текстом программы')
    parser.add_argument('-o', '--output', help='Путь к двоичному файлу-результату')
    parser.add_argument('-t', '--test', action='store_true', help='Режим тестирования')
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        lines = [parse_line(line) for line in f if parse_line(line)]

    program = [to_ir(cmd, nums) for cmd, nums in lines]

    if args.test:
        print("Промежуточное представление ассемблированной программы:")
        for i, ir in enumerate(program):
            if ir['op'] == 20:
                print(f'Команда {i + 1}: A = {ir["op"]}, B = {ir["b"]}, C = {ir["c"]}')
                binary = encode(ir)
                hex_bytes = ', '.join(f'0x{b:02X}' for b in binary)
                print(f'  Бинарно: {hex_bytes}')
            elif ir['op'] == 28:
                print(f'Команда {i + 1}: A = {ir["op"]}, B = {ir["b"]}, C = {ir["c"]}, D = {ir["d"]}')
                binary = encode(ir)
                hex_bytes = ', '.join(f'0x{b:02X}' for b in binary)
                print(f'  Бинарно: {hex_bytes}')
            elif ir['op'] == 12:
                print(f'Команда {i + 1}: A = {ir["op"]}, B = {ir["b"]}, C = {ir["c"]}, D = {ir["d"]}')
                binary = encode(ir)
                hex_bytes = ', '.join(f'0x{b:02X}' for b in binary)
                print(f'  Бинарно: {hex_bytes}')
            elif ir['op'] == 18:
                print(f'Команда {i + 1}: A = {ir["op"]}, B = {ir["b"]}, C = {ir["c"]}')
                binary = encode(ir)
                hex_bytes = ', '.join(f'0x{b:02X}' for b in binary)
                print(f'  Бинарно: {hex_bytes}')

    if args.output:
        with open(args.output, 'wb') as f:
            for ir in program:
                f.write(encode(ir))

if __name__ == '__main__':
    main()  