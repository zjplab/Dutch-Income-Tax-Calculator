import subprocess
import json
import tempfile
import os

def calculate_dutch_tax(income, allowance, social_security, older, hours, year, checked):
    # JavaScript code template
    js_code_template = """
const {{ SalaryPaycheck }} = require('dutch-tax-income-calculator');

const paycheck = new SalaryPaycheck({{
    income: {income},
    allowance: {allowance_str},
    socialSecurity: {social_security_str},
    older: {older_str},
    hours: {hours}
}}, 'Year', {year}, {{
    checked: {checked_str}
}});

console.log(JSON.stringify(paycheck));
"""

    js_code = js_code_template.format(
        income=income,
        allowance_str=str(allowance).lower(),
        social_security_str=str(social_security).lower(),
        older_str=str(older).lower(),
        hours=hours,
        year=year,
        checked_str=str(checked).lower()
    )

    # Specify the root directory of your project
    root_folder = '/Users/jiapengzhang/PersonalProject/Dutch-Income-Tax-Calculator'

    # Create a temporary JS file and write the JS code to it
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, dir=root_folder) as tmpfile:
        tmpfile.write(js_code)
        tmp_filename = tmpfile.name

    # Execute the temporary JS file using Node.js with the working directory set to the project root
    result = subprocess.run(['node', tmp_filename], capture_output=True, text=True, cwd=root_folder)

    # Cleanup the temporary JS file
    os.unlink(tmp_filename)

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

# Example usage
result = calculate_dutch_tax(36000, False, True, False, 40, 2020, False)
print(result)
