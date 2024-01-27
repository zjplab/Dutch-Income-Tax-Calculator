import subprocess
import json
import os

# Specify the root directory of your project
root_folder = os.path.dirname(os.path.abspath(__file__))

def calculate_dutch_tax(income, allowance, social_security, older, hours, year, checked, choice="young"):
    # JavaScript code as a single string, correctly escaped for shell execution
    js_code = f"""
const {{ SalaryPaycheck }} = require('dutch-tax-income-calculator');

const paycheck = new SalaryPaycheck({{
    income: {income},
    allowance: {str(allowance).lower()},
    socialSecurity: {str(social_security).lower()},
    older: {str(older).lower()},
    hours: {hours}
}}, 'Year', {year}, {{
    checked: {str(checked).lower()},
    choice: "{str(choice).lower()}"
}});

console.log(JSON.stringify(paycheck));
"""

    # Execute the JS code directly using `node -e`
    result = subprocess.run(['node', '-e', js_code], capture_output=True, text=True, cwd=root_folder)
    # print(js_code)
    # Error handling and JSON output parsing
    if result.stderr or not result.stdout.strip():
        print("Error running Node.js script:", result.stderr)
        return None

    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print("Failed to decode JSON output:", e)
        return None

    return output

if __name__ == '__main__':
    # Example usage
    result = calculate_dutch_tax(150000, False, True, False, 40, 2023, True)
    pretty_result = json.dumps(result, indent=4)
    print(pretty_result)
