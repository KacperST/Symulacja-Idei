import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from models import VoterModel

# Parametry
num_agents = 200
initial_ratio = 0.5  # np. 50% agentów z opinią +1
num_steps = 250

# Inicjalizacja modelu
model = VoterModel(num_agents=num_agents, initial_ratio=initial_ratio)

history_pos = []
history_neg = []

for _ in range(num_steps):
    model.step()
    opinions = [agent.opinion for agent in model.agents]
    history_pos.append(opinions.count(1))
    history_neg.append(opinions.count(-1))
    if model.running is False:
        break

# Wykres animowany
fig, ax = plt.subplots()
line1, = ax.plot([], [], label="Opinia +1", color="red")
line2, = ax.plot([], [], label="Opinia -1", color="blue")
ax.set_xlim(0, num_steps)
ax.set_ylim(0, num_agents)
ax.set_xlabel("Krok czasowy")
ax.set_ylabel("Liczba agentów")
ax.set_title("Dynamika opinii (Majority Rule)")
ax.legend()

def update(frame):
    x = list(range(frame + 1))
    y1 = history_pos[:frame + 1]
    y2 = history_neg[:frame + 1]
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    return line1, line2

ani = FuncAnimation(fig, update, frames=len(history_pos), interval=200, blit=True)
ani.save("symulacja_opinii.mp4", writer="ffmpeg")
print("Animacja zapisana jako symulacja_opinii.mp4")
