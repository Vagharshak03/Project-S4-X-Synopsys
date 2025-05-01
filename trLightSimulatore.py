import time

class TrafficLight:
    def __init__(self, green_duration, yellow_duration, red_duration):
        self.green_duration = green_duration
        self.yellow_duration = yellow_duration
        self.red_duration = red_duration
        self.state = "RED"

    def run_cycle(self):
        while True:
            self.switch_to_green()
            self.switch_to_yellow()
            self.switch_to_red()

    def countdown(self, duration, color):
        for remaining in range(duration, 0, -1):
            print(f"[{color}] - {remaining} seconds remaining", end="\r")
            time.sleep(1)
        print()  # Move to the next line after countdown finishes

    def switch_to_green(self):
        self.state = "GREEN"
        self.countdown(self.green_duration, self.state)

    def switch_to_yellow(self):
        self.state = "YELLOW"
        self.countdown(self.yellow_duration, self.state)

    def switch_to_red(self):
        self.state = "RED"
        self.countdown(self.red_duration, self.state)

def main():
    print("Welcome to the Traffic Signal Simulator!")
    try:
        green_time = int(input("Enter GREEN light duration (in seconds): "))
        yellow_time = int(input("Enter YELLOW light duration (in seconds): "))
        red_time = int(input("Enter RED light duration (in seconds): "))
    except ValueError:
        print("Invalid input! Please enter integer values.")
        return

    traffic_light = TrafficLight(green_time, yellow_time, red_time)
    traffic_light.run_cycle()

if __name__ == "__main__":
    main()
