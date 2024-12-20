import unittest
import subprocess

class TestConfigLanguage(unittest.TestCase):
    
    def run_config_parser(self, yaml_content):
        """Helper method to run the config parser script on an input YAML content."""
        result = subprocess.run(
            ['python', 'main.py'], 
            input=yaml_content, text=True, capture_output=True
        )
        return result.stdout.strip()

    def test_web_server_config(self):
        yaml_content = """name: "Web Server Config"
version: 2.1
features:
  - logging
  - caching
  - compression
settings:
  host: "localhost"
  port: 8080
  ssl_enabled: True
max_connections: 100
expression: "|max_connections|"
"""
        expected_output = """name: @"Web Server Config"
version: 2.1
features: [
    0 => @"logging",
    1 => @"caching",
    2 => @"compression",
]
settings: [
    host => @"localhost",
    port => 8080,
    ssl_enabled => True,
]
max_connections: 100
expression: 100"""
        
        output = self.run_config_parser(yaml_content)
        
        # Выводим оба результата, если они не совпадают
        if output != expected_output:
            print(f"Expected Output:\n{expected_output}\n")
            print(f"Actual Output:\n{output}\n")
        
        self.assertEqual(output, expected_output)

    def test_game_config(self):
        yaml_content = """name: "Game Config"
max_level: 50
difficulty: "medium"
settings:
  resolution: "1920x1080"
  fullscreen: True
player_health: 100
expression: "|player_health|"
"""
        expected_output = """name: @"Game Config"
max_level: 50
difficulty: @"medium"
settings: [
    resolution => @"1920x1080",
    fullscreen => True,
]
player_health: 100
expression: 100"""
        
        output = self.run_config_parser(yaml_content)
        
        # Выводим оба результата, если они не совпадают
        if output != expected_output:
            print(f"Expected Output:\n{expected_output}\n")
            print(f"Actual Output:\n{output}\n")
        
        self.assertEqual(output, expected_output)

if __name__ == "__main__":
    unittest.main()