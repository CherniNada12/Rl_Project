from flask import Flask, render_template, jsonify, request
from environment import GridEnvironment
from agent import RLAgent
from trainer import Trainer

app = Flask(__name__)

env = GridEnvironment()
agent = RLAgent(env)
trainer = Trainer(env, agent)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/grid")
def get_grid():
    return jsonify({
        "grid": env.grid.tolist(),
        "agent": agent.env.start_position
    })

@app.route("/train", methods=["POST"])
def train():
    algo = request.json.get("algorithm","qlearning")
    result = trainer.train_episode(algo)
    return jsonify(result)

if __name__=="__main__":
    app.run(debug=True)
