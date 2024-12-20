import yaml
import sys
import re

class ConfigParser:
    def __init__(self):
        self.constants = {}

    def parse(self, yaml_data):
        return self._parse_node(yaml_data)

    def _parse_node(self, node):
        if isinstance(node, dict):
            return self._parse_dict(node)
        elif isinstance(node, list):
            return self._parse_list(node)
        elif isinstance(node, int) or isinstance(node, float):
            return str(node)
        elif isinstance(node, str):
            return f'@"{node}"'
        elif isinstance(node, bool):
            return "true" if node else "false"
        else:
            raise SyntaxError(f"Unsupported type: {type(node)}")

    def _parse_dict(self, node):
        result = []
        for key, value in node.items():
            if not re.match(r'^[a-zA-Z][_a-zA-Z0-9]*$', key):
                raise SyntaxError(f"Invalid key name: {key}")
            result.append(f"    {key} => {self._parse_node(value)},")
        return "[\n" + "\n".join(result) + "\n]"

    def _parse_list(self, node):
        result = [self._parse_node(value) for value in node]
        return "[\n" + "\n".join(f"    {i} => {value}," for i, value in enumerate(result)) + "\n]"

    def parse_expression(self, expression):
        # Обрабатываем вычисления вида |имя|
        expression = expression.strip()[1:-1]  # Убираем | и |
        if expression in self.constants:
            return str(self.constants[expression])
        else:
            raise SyntaxError(f"Undefined constant: {expression}")

def main():
    parser = ConfigParser()

    try:
        # Загружаем данные из стандартного ввода
        yaml_data = yaml.safe_load(sys.stdin.read())

        # Собираем все константы в один словарь для дальнейшей обработки
        for key, value in yaml_data.items():
            if isinstance(value, (int, float)):
                parser.constants[key] = value

        result = []
        for key, value in yaml_data.items():
            if isinstance(value, str) and value.startswith("|") and value.endswith("|"):
                # Обрабатываем выражения типа |имя|
                result.append(f"{key}: {parser.parse_expression(value)}")
            else:
                result.append(f"{key}: {parser._parse_node(value)}")

        # Выводим результат
        print("\n".join(result))

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()