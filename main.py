import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from models import VoterModel

# Tworzenie modelu
model = VoterModel(num_agents=100)
num_steps = 50

# Historia opinii
history_pos = []
history_neg = []

# Przeprowadzenie symulacji
for _ in range(num_steps):
    model.step()
    opinions = [agent.opinion for agent in model.agents]
    history_pos.append(opinions.count(1))
    history_neg.append(opinions.count(-1))

# Utworzenie figury do animacji
fig, ax = plt.subplots()
line1, = ax.plot([], [], label="Opinia +1")
line2, = ax.plot([], [], label="Opinia -1")
ax.set_xlim(0, num_steps)
ax.set_ylim(0, model.num_agents)
ax.set_xlabel("Krok czasowy")
ax.set_ylabel("Liczba agentów")
ax.set_title("Dynamika opinii w modelu głosowania")
ax.legend()

# Funkcja aktualizacji animacji
def update(frame):
    x = list(range(frame + 1))
    y1 = history_pos[:frame + 1]
    y2 = history_neg[:frame + 1]
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    return line1, line2

# Tworzenie animacji
ani = FuncAnimation(fig, update, frames=num_steps, interval=200, blit=True)

# Zapis do pliku MP4
ani.save("symulacja_opinii.mp4", writer="ffmpeg")

# Alternatywnie: zapis do GIF
# ani.save("symulacja_opinii.gif", writer="pillow")

print("Animacja zapisana jako symulacja_opinii.mp4")
