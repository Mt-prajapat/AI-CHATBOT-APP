import re
import math
import random
from datetime import datetime, timedelta

class AdvancedProblemSolver:
    def __init__(self):
        self.setup_problem_solvers()
    
    def setup_problem_solvers(self):
        self.solvers = {
            'math': self.solve_math_problem,
            'physics': self.solve_physics_problem,
            'programming': self.solve_programming_problem,
            'logic': self.solve_logic_puzzle,
            'time_date': self.solve_time_date_problem,
            'conversion': self.solve_conversion_problem
        }
    
    def solve_general_problem(self, problem):
        problem_lower = problem.lower()
        
        # Mathematical problems
        if any(keyword in problem_lower for keyword in 
               ['calculate', 'solve', 'what is', 'how much', 'math', 'equation']):
            return self.solve_math_problem(problem)
        
        # Physics problems
        elif any(keyword in problem_lower for keyword in 
                ['velocity', 'acceleration', 'force', 'energy', 'physics']):
            return self.solve_physics_problem(problem)
        
        # Programming problems
        elif any(keyword in problem_lower for keyword in 
                ['code', 'program', 'function', 'algorithm', 'python', 'javascript']):
            return self.solve_programming_problem(problem)
        
        # Time and date problems
        elif any(keyword in problem_lower for keyword in 
                ['time', 'date', 'day', 'week', 'month', 'year']):
            return self.solve_time_date_problem(problem)
        
        # Conversion problems
        elif any(keyword in problem_lower for keyword in 
                ['convert', 'feet to meters', 'celsius to fahrenheit']):
            return self.solve_conversion_problem(problem)
        
        # Logic puzzles
        else:
            return self.solve_logic_puzzle(problem)
    
    def solve_math_problem(self, problem):
        # Enhanced math solver with more capabilities
        try:
            # Handle special cases
            if '0/0' in problem:
                return {
                    'answer': 'Indeterminate form (0/0)',
                    'explanation': '0 divided by 0 is undefined and considered an indeterminate form in mathematics. It requires limit analysis for proper evaluation.',
                    'type': 'mathematics',
                    'details': 'Use L\'Hôpital\'s rule or algebraic manipulation for limits'
                }
            
            if 'infinity' in problem.lower():
                return {
                    'answer': '∞ (Infinity)',
                    'explanation': 'Infinity represents an unbounded quantity larger than any real number.',
                    'type': 'mathematics',
                    'details': 'Infinity operations: ∞ + a = ∞, ∞ × ∞ = ∞, a/∞ = 0'
                }
            
            # Basic arithmetic
            if re.search(r'(\d+)\s*[\+\-]\s*(\d+)', problem):
                numbers = re.findall(r'\d+', problem)
                if '+' in problem:
                    result = sum(map(int, numbers))
                    return {
                        'answer': result,
                        'explanation': f'Addition: {" + ".join(numbers)} = {result}',
                        'type': 'arithmetic'
                    }
                elif '-' in problem:
                    result = int(numbers[0]) - int(numbers[1])
                    return {
                        'answer': result,
                        'explanation': f'Subtraction: {numbers[0]} - {numbers[1]} = {result}',
                        'type': 'arithmetic'
                    }
            
            # Multiplication and division
            if re.search(r'(\d+)\s*[\*\/]\s*(\d+)', problem):
                numbers = re.findall(r'\d+', problem)
                if '*' in problem:
                    result = int(numbers[0]) * int(numbers[1])
                    return {
                        'answer': result,
                        'explanation': f'Multiplication: {numbers[0]} × {numbers[1]} = {result}',
                        'type': 'arithmetic'
                    }
                elif '/' in problem and numbers[1] != '0':
                    result = int(numbers[0]) / int(numbers[1])
                    return {
                        'answer': result,
                        'explanation': f'Division: {numbers[0]} ÷ {numbers[1]} = {result}',
                        'type': 'arithmetic'
                    }
            
            # Area and volume calculations
            if 'area' in problem.lower():
                if 'circle' in problem.lower():
                    radius = self.extract_number(problem)
                    area = math.pi * radius ** 2
                    return {
                        'answer': f'{area:.2f}',
                        'explanation': f'Area of circle with radius {radius} = π × r² = {math.pi:.2f} × {radius}²',
                        'type': 'geometry'
                    }
                
                if 'rectangle' in problem.lower():
                    numbers = re.findall(r'\d+', problem)
                    if len(numbers) >= 2:
                        area = int(numbers[0]) * int(numbers[1])
                        return {
                            'answer': area,
                            'explanation': f'Area of rectangle: {numbers[0]} × {numbers[1]} = {area}',
                            'type': 'geometry'
                        }
            
            # Percentage calculations
            if '%' in problem or 'percent' in problem.lower():
                numbers = re.findall(r'\d+', problem)
                if len(numbers) >= 2:
                    percentage = (int(numbers[0]) / int(numbers[1])) * 100
                    return {
                        'answer': f'{percentage:.1f}%',
                        'explanation': f'Percentage: ({numbers[0]} ÷ {numbers[1]}) × 100 = {percentage:.1f}%',
                        'type': 'mathematics'
                    }
        
        except Exception as e:
            return {
                'answer': 'Unable to solve',
                'explanation': f'Error in calculation: {str(e)}',
                'type': 'error'
            }
        
        return {
            'answer': 'Complex mathematical problem',
            'explanation': 'This requires advanced mathematical analysis.',
            'type': 'mathematics'
        }
    
    def solve_physics_problem(self, problem):
        problem_lower = problem.lower()
        
        if 'velocity' in problem_lower:
            return {
                'answer': 'v = d/t',
                'explanation': 'Velocity = distance ÷ time',
                'type': 'physics',
                'formula': 'v = Δx/Δt'
            }
        
        elif 'acceleration' in problem_lower:
            return {
                'answer': 'a = Δv/Δt',
                'explanation': 'Acceleration = change in velocity ÷ time',
                'type': 'physics',
                'formula': 'a = (v_f - v_i)/t'
            }
        
        elif 'force' in problem_lower:
            return {
                'answer': 'F = m × a',
                'explanation': 'Force = mass × acceleration (Newton\'s Second Law)',
                'type': 'physics',
                'formula': 'F = ma'
            }
        
        elif 'energy' in problem_lower:
            return {
                'answer': 'E = m × c²',
                'explanation': 'Energy = mass × speed of light squared (Einstein\'s equation)',
                'type': 'physics',
                'formula': 'E = mc²'
            }
        
        return {
            'answer': 'Physics principle',
            'explanation': 'Applying fundamental physics laws and equations',
            'type': 'physics'
        }
    
    def solve_programming_problem(self, problem):
        problem_lower = problem.lower()
        
        if 'python' in problem_lower:
            solutions = {
                'hello world': 'print("Hello, World!")',
                'fibonacci': 'def fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)',
                'factorial': 'def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)',
                'prime check': 'def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0:\n            return False\n    return True'
            }
            
            for key, solution in solutions.items():
                if key in problem_lower:
                    return {
                        'answer': f'Python solution for {key}',
                        'explanation': solution,
                        'type': 'programming',
                        'language': 'Python'
                    }
        
        return {
            'answer': 'Programming solution',
            'explanation': 'Here\'s a general approach to solve this programming problem...',
            'type': 'programming'
        }
    
    def solve_time_date_problem(self, problem):
        now = datetime.now()
        
        if 'current time' in problem.lower():
            return {
                'answer': now.strftime('%H:%M:%S'),
                'explanation': f'Current time is {now.strftime("%I:%M %p")}',
                'type': 'time'
            }
        
        elif 'current date' in problem.lower():
            return {
                'answer': now.strftime('%Y-%m-%d'),
                'explanation': f'Today is {now.strftime("%A, %B %d, %Y")}',
                'type': 'date'
            }
        
        elif 'day of week' in problem.lower():
            return {
                'answer': now.strftime('%A'),
                'explanation': f'Today is {now.strftime("%A")}',
                'type': 'date'
            }
        
        return {
            'answer': 'Time/date information',
            'explanation': 'Based on current datetime calculations',
            'type': 'time_date'
        }
    
    def solve_conversion_problem(self, problem):
        problem_lower = problem.lower()
        
        if 'celsius to fahrenheit' in problem_lower:
            numbers = self.extract_numbers(problem)
            if numbers:
                celsius = numbers[0]
                fahrenheit = (celsius * 9/5) + 32
                return {
                    'answer': f'{fahrenheit:.1f}°F',
                    'explanation': f'{celsius}°C = ({celsius} × 9/5) + 32 = {fahrenheit:.1f}°F',
                    'type': 'conversion'
                }
        
        elif 'fahrenheit to celsius' in problem_lower:
            numbers = self.extract_numbers(problem)
            if numbers:
                fahrenheit = numbers[0]
                celsius = (fahrenheit - 32) * 5/9
                return {
                    'answer': f'{celsius:.1f}°C',
                    'explanation': f'{fahrenheit}°F = ({fahrenheit} - 32) × 5/9 = {celsius:.1f}°C',
                    'type': 'conversion'
                }
        
        return {
            'answer': 'Conversion result',
            'explanation': 'Unit conversion using standard formulas',
            'type': 'conversion'
        }
    
    def solve_logic_puzzle(self, problem):
        puzzles = {
            'what comes next': 'Analyzing the pattern...',
            'logic puzzle': 'Applying logical reasoning...',
            'riddle': 'Thinking creatively to solve...'
        }
        
        for key, response in puzzles.items():
            if key in problem.lower():
                return {
                    'answer': 'Logical solution',
                    'explanation': response,
                    'type': 'logic'
                }
        
        return {
            'answer': 'Analytical solution',
            'explanation': 'Using logical reasoning and pattern recognition',
            'type': 'logic'
        }
    
    def extract_number(self, text):
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else 1
    
    def extract_numbers(self, text):
        return [int(num) for num in re.findall(r'\d+', text)]