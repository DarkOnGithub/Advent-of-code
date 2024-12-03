import re

MUL_EXPRESSION : str = r"mul\((\d{1,3}),(\d{1,3})\)"

def parse_instructions(memory_string):
    instructions = sorted(
        [{'index': m.start(), 'type': 'do'} for m in re.finditer(r'do\(\)', memory_string)] +
        [{'index': m.start(), 'type': 'dont'} for m in re.finditer(r"don't\(\)", memory_string)],
        key=lambda x: x['index']
    )
    return instructions

def main(input: str) -> str:
    matches = re.findall(MUL_EXPRESSION, input)
    output_1 = sum(int(a) * int(b) for a, b in matches)

    instructions = parse_instructions(input)
    pattern = re.compile(MUL_EXPRESSION)
    output_2 = 0
    current_instruction = "do"

    for match in pattern.finditer(input):
        while instructions and instructions[0]['index'] <= match.start():
            current_instruction = instructions.pop(0)['type']
        if current_instruction == "do":
            a, b = map(int, match.groups())
            output_2 += a * b

    return output_1, output_2

if __name__ == "__main__":
    with open("./input.txt", "r") as f:
        print(main(f.read()))