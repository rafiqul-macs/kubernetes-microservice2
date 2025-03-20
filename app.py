from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Define persistent volume directory
PV_DIR = "/rafiqul_PV_dir"
os.makedirs(PV_DIR, exist_ok=True)

@app.route('/calculate-product', methods=['POST'])
def calculate_product():
    data = request.get_json()
    
    # Validate input
    if not data or 'file' not in data or not data['file']:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400
        
    if 'product' not in data:
        return jsonify({"file": data['file'], "error": "Invalid JSON input."}), 400
        
    file_name = data['file']
    product_name = data['product']
    file_path = os.path.join(PV_DIR, file_name)
    
    # Check if file exists
    if not os.path.exists(file_path):
        return jsonify({
            "file": file_name,
            "error": "File not found."
        }), 404
    
    # Read and parse CSV
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        lines = content.strip().split('\n')
        if len(lines) < 2:
            return jsonify({
                "file": file_name,
                "error": "Input file not in CSV format."
            }), 400
        
        # Parse headers
        headers = [h.strip() for h in lines[0].split(',')]
        if 'product' not in headers or 'amount' not in headers:
            return jsonify({
                "file": file_name,
                "error": "Input file not in CSV format."
            }), 400
            
        # Find column indices
        product_idx = headers.index('product')
        amount_idx = headers.index('amount')
        
        # Calculate sum
        total = 0
        for i in range(1, len(lines)):
            row = [r.strip() for r in lines[i].split(',')]
            if len(row) <= max(product_idx, amount_idx):
                continue
                
            if row[product_idx] == product_name:
                try:
                    total += int(row[amount_idx])
                except ValueError:
                    pass
        
        return jsonify({
            "file": file_name,
            "sum": total
        })
            
    except Exception as e:
        print(f"Error in calculate: {e}")
        return jsonify({
            "file": file_name,
            "error": "Input file not in CSV format."
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)