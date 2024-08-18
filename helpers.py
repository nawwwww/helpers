a = {
    "key1": {
        "a": 1,
        "b": True,
        "c": "string",
        "d": {(1,2): "tuple"}
    },
    "key2": [
        '1',
        2,
        True,
        (1,2,"some string"),
        {
            "key": "value",
            (
                'wierd tuple',
                True,
                False,
                ('1', 2, "this")
            ): {'key1': 'value1', ('key2', 1, True, False, '123141224141'): {
                'abc': {
                    'key': 'value',
                    'key2': {
                        'key3': 'value'
                    }
                }
            }
            }
        }],
    "key3": {
        (),
        1,
        2,
        3,
        "Long string"
    }
}

def write_variable_to_file(variable, filePath='file_with_variable.py', indent=4):
    file = open(filePath, 'w')  # Open the file once at the beginning
    
    def do_writing(variable, file, indent):
        indent_str = " " * indent  # Adjust indentation for each level

        if isinstance(variable, dict):
            file.write("{\n")
            for key, value in variable.items():
                if isinstance(key, tuple):
                    file.write(indent_str)
                    file.write(str(key))
                    file.write(": ")
                    do_writing(value, file, indent + 4)  # Recursive call with the same file object
                    file.write(",\n")
                else:
                    file.write(f'{indent_str}"{key}": ')
                    do_writing(value, file, indent + 4)  # Recursive call with the same file object
                    file.write(",\n")
            file.write(indent_str[:-4] + "}")  # Close the dict

        elif isinstance(variable, list):
            file.write("[\n")
            for value in variable:
                file.write(indent_str)
                do_writing(value, file, indent + 4)
                file.write(",\n")
            file.write(indent_str[:-4] + "]")  # Close the list

        elif isinstance(variable, tuple):
            file.write("(\n")
            for value in variable:
                file.write(indent_str)
                do_writing(value, file, indent + 4)
                file.write(",\n")
            file.write(indent_str[:-4] + ")")  # Close the tuple

        elif isinstance(variable, set):
            file.write("{\n")
            for value in variable:
                file.write(indent_str)
                do_writing(value, file, indent + 4)
                file.write(",\n")
            file.write(indent_str[:-4] + "}")  # Close the set

        elif isinstance(variable, str):
            file.write(f'"{variable}"')

        elif isinstance(variable, (int, float, bool)):
            file.write(str(variable))

    do_writing(variable, file, indent)  # Start the writing process
    file.close()  # Close the file at the end

def convert_string_to_tuple(s):
    def parse_value(s, start):
        if s[start] == "'":
            end = s.find("'", start + 1)
            return s[start+1:end], end + 1
        elif s[start] == '"':
            end = s.find('"', start + 1)
            return s[start+1:end], end + 1
        elif s[start].isdigit() or (s[start] == '-' and s[start + 1].isdigit()):
            end = start
            while end < len(s) and (s[end].isdigit() or s[end] == '.'):
                end += 1
            return int(s[start:end]) if '.' not in s[start:end] else float(s[start:end]), end
        elif s[start] == '{':
            return parse_dict(s, start)
        elif s[start] == '[':
            return parse_list(s, start)
        else:
            raise ValueError(f"Unexpected character '{s[start]}' in input string.")
    
    def parse_dict(s, start):
        result = {}
        key, pos = parse_value(s, start + 1)
        while s[pos] != '}':
            if s[pos] != ':':
                raise ValueError("Expected ':' in dictionary.")
            value, pos = parse_value(s, pos + 1)
            result[key] = value
            if s[pos] == ',':
                pos += 1
                key, pos = parse_value(s, pos)
            elif s[pos] == '}':
                pos += 1
            else:
                raise ValueError("Expected ',' or '}' in dictionary.")
        return result, pos
    
    def parse_list(s, start):
        result = []
        value, pos = parse_value(s, start + 1)
        while s[pos] != ']':
            result.append(value)
            if s[pos] == ',':
                pos += 1
                value, pos = parse_value(s, pos)
            elif s[pos] == ']':
                pos += 1
            else:
                raise ValueError("Expected ',' or ']' in list.")
        return result, pos
    
    s = s.strip()
    if not (s.startswith('(') and s.endswith(')')):
        raise ValueError("Input string must start and end with parentheses.")
    
    elements = []
    i = 1  # Skip the opening '('
    while i < len(s) - 1:  # Skip the closing ')'
        value, i = parse_value(s, i)
        elements.append(value)
        if s[i] == ',':
            i += 1
    
    return tuple(elements)

# Example usage
# tuple_str = "(1, 2, 'hello', 4.5, 'world', {'key1': 1, 'key2': [2, 3]}, {1, 2, 3})"
# result = convert_string_to_tuple(tuple_str)
# print(result)