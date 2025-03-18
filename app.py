from flask import Flask, request, jsonify
import os
import csv

app = Flask(__name__)

# Define the persistent volume directory path
PV_DIR = "/john_PV_dir"  # Replace with your first name

# Create the directory if it doesn't exist (for local testing)
os.makedirs(PV_DIR, exist_ok=True)

@app.route('/calculate-product', methods=['POST'])
def calculate_product():
    try:
        # Parse request JSON
        data = request.get_json()
        
        # Validate JSON input
        if not data or 'file' not in data or not data['file']:
            return jsonify({
                "file": None,
                "error": "Invalid JSON input."
            }), 400
            
        if 'product' not in data:
            return jsonify({
                "file": data['file'],
                "error": "Invalid JSON input."
            }), 400
            
        file_name = data['file']
        product_name = data['product']
        file_path = os.path.join(PV_DIR, file_name)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({
                "file": file_name,
                "error": "File not found."
            }), 404
            
        # Read the CSV file and calculate the sum for the given product
        try:
            product_sum = 0
            csv_format_valid = False
            
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
                # Check if file has at least one header line
                if len(lines) == 0:
                    return jsonify({
                        "file": file_name,
                        "error": "Input file not in CSV format."
                    }), 400
                
                # Process CSV data
                try:
                    reader = csv.DictReader([line.strip() for line in lines])
                    
                    # Check if 'product' and 'amount' columns exist
                    if 'product' not in reader.fieldnames or 'amount' not in reader.fieldnames:
                        return jsonify({
                            "file": file_name,
                            "error": "Input file not in CSV format."
                        }), 400
                    
                    csv_format_valid = True
                    
                    # Calculate the sum for the requested product
                    for row in reader:
                        # Skip rows with missing data
                        if not row['product'] or not row['amount']:
                            continue
                            
                        # Strip any whitespace
                        row_product = row['product'].strip()
                        
                        # If this row contains the requested product, add its amount to the sum
                        if row_product == product_name:
                            try:
                                product_sum += int(row['amount'].strip())
                            except ValueError:
                                app.logger.error(f"Invalid amount value in CSV: {row['amount']}")
                                # Continue processing other rows
                except Exception as e:
                    app.logger.error(f"Error parsing CSV: {str(e)}")
                    return jsonify({
                        "file": file_name,
                        "error": "Input file not in CSV format."
                    }), 400
            
            if not csv_format_valid:
                return jsonify({
                    "file": file_name,
                    "error": "Input file not in CSV format."
                }), 400
                
            # Return the calculated sum
            return jsonify({
                "file": file_name,
                "sum": product_sum
            })
            
        except Exception as e:
            app.logger.error(f"Error calculating product sum: {str(e)}")
            return jsonify({
                "file": file_name,
                "error": "Error calculating product sum."
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error in calculate_product: {str(e)}")
        return jsonify({
            "file": None,
            "error": "Invalid JSON input."
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)