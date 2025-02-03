import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(abs(n)**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 2:
        return False
    divisors = [i for i in range(1, abs(n)) if n % i == 0]
    return sum(divisors) == abs(n)

def is_armstrong(n):
    digits = [int(d) for d in str(abs(n))]
    length = len(digits)
    return sum(d**length for d in digits) == abs(n)

def get_properties(n):
    properties = []
    if is_prime(abs(n)):
        properties.append("prime")
    if is_perfect(n):
        properties.append("perfect")
    if is_armstrong(n):
        properties.append("armstrong")
    if n % 2 != 0:
        properties.append("odd")
    else:
        properties.append("even")
    return properties

def get_fun_fact(n):
    if is_armstrong(abs(n)):
        return f"{n} is an Armstrong number because {' + '.join(f'{d}^{len(str(abs(n)))}' for d in map(int, str(abs(n))))} = {abs(n)}"
    return f"{n} is a fascinating number with unique properties."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')
    if not number or not number.lstrip('-').isdigit():
        return jsonify({"number": number, "error": True}), 400

    number = int(number)
    properties = get_properties(number)
    digit_sum = sum(int(d) for d in str(abs(number)))
    fun_fact = get_fun_fact(number)

    response = {
        "number": number,
        "is_prime": is_prime(abs(number)),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }
    return jsonify(response), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)