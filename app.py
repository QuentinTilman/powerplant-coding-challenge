from flask import Flask, jsonify, request
import production_plan
app = Flask(__name__)


@app.route('/productionplan', methods=['POST'])
def productionplan():
    data = request.get_json()
    production = production_plan.culculate_production(data)
    return jsonify(production)
    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8888)