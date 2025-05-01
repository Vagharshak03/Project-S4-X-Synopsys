from flask import Flask, jsonify, request, render_template
from threading import Thread, Event
import time

app = Flask(__name__)

class TrafficLight:
    def __init__(self, green_duration, yellow_duration, red_duration):
        self.green_duration = green_duration
        self.yellow_duration = yellow_duration
        self.red_duration = red_duration
        self.state = "RED"
        self.remaining = 0
        self.running = False
        self._stop_event = Event()

    def start(self):
        if not self.running:
            self.running = True
            self._stop_event.clear()
            Thread(target=self.run_cycle, daemon=True).start()

    def stop(self):
        self.running = False
        self._stop_event.set()

    def run_cycle(self):
        while self.running:
            self.switch_to_green()
            if self._stop_event.is_set(): break
            self.switch_to_yellow()
            if self._stop_event.is_set(): break
            self.switch_to_red()
            if self._stop_event.is_set(): break

    def countdown(self, duration, color):
        self.state = color
        self.remaining = duration
        for _ in range(duration):
            if self._stop_event.is_set():
                break
            time.sleep(1)
            self.remaining -= 1

    def switch_to_green(self):
        self.countdown(self.green_duration, "GREEN")

    def switch_to_yellow(self):
        self.countdown(self.yellow_duration, "YELLOW")

    def switch_to_red(self):
        self.countdown(self.red_duration, "RED")

@app.route('/')
def home():
    return render_template('index.html')

# Initialize with default durations (can be set via query)
traffic_light = TrafficLight(5, 2, 5)

@app.route('/start', methods=['POST'])
def start():
    durations = request.json
    traffic_light.green_duration = durations.get('green', 5)
    traffic_light.yellow_duration = durations.get('yellow', 2)
    traffic_light.red_duration = durations.get('red', 5)
    traffic_light.start()
    return jsonify({"message": "Simulation started"})

@app.route('/stop', methods=['POST'])
def stop():
    traffic_light.stop()
    return jsonify({"message": "Simulation stopped"})

@app.route('/status')
def status():
    return jsonify({
        "state": traffic_light.state,
        "remaining": traffic_light.remaining
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
