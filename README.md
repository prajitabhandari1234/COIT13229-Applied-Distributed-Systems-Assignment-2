# COIT13229 Applied Distributed Systems — Assignment 2
## Gold Miner: Distributed Game

**Student Name:** Prajita Bhandari  
**Student ID:** 12255441
**Unit:** COIT13229 Applied Distributed Systems  

---

## Overview

Gold Miner is a distributed, text-based game built in Python. A human player connects to a central server and competes against AI bots within a shared 20×20 grid. Players move across the grid to collect gold and increase their score.

The system demonstrates key distributed systems concepts such as **client-server architecture, sequential consistency, message ordering, and fault tolerance** for non-Byzantine faults including network lag and message loss.

---

## Technologies Used

| Technology | Role |
|---|---|
| Python 3 | Core implementation language |
| ZeroMQ (ZMQ) | Network communication (PUSH/PUB sockets) |
| Pytest | Automated test execution |
| GitHub | Version control and submission |

---

## System Architecture

The system uses a **client-server architecture** with a central sequencer server.

- The **client** sends player moves to the server
- The **server processes all moves in order**
- The **server broadcasts updated game state to clients**
- **Bots are simulated inside the server**

```
Human Client ──PUSH──▶ Server (Sequencer) ──PUB──▶ All Clients
```
---

## Consistency Model


The system implements **Sequential Consistency**.

### Properties:

- All moves are processed by a **single server**
- Moves are applied in strict **arrival order**
- All clients receive updates in the same order
- All players observe the **same game state**

### Trade-off:

- Single point of failure (server)
- No fault recovery implemented (prototype limitation)

---

## Project Structure

```
gold-miner/
├── src/
│   ├── server.py        # Central sequencer — handles bots and moves
│   ├── client.py        # Human player client
│   └── game.py          # Game logic
├── tests/
│   ├── test_game.py     # Core game logic tests (movement, gold collection)
│   └── test_faults.py   # Distributed fault simulation tests
├── requirements.txt
└── README.md
```

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the server (run first)

```bash
python src/server.py
```

### 3. Start the client (on new terminal)

```bash
python src/client.py
```

### Controls

| Key | Action |
|---|---|
| `W` | Move Up |
| `S` | Move Down |
| `A` | Move Left |
| `D` | Move Right |
| `Q` | Quit |

---

## Testing

Run all tests:

```bash
pytest
```

### Test Coverage

| Test            | Description                  | Fault Type         |
| --------------- | ---------------------------- | ------------------ |
| Movement tests  | Player movement correctness  | None               |
| Boundary tests  | Prevent moving outside grid  | None               |
| Gold collection | Score increases correctly    | None               |
| Lag simulation  | Delayed move still applied   | Network lag        |
| Lost message    | Only delivered moves applied | Packet loss        |
| Reordering test | Order affects final state    | Message reordering |
| Node crash test | Documents limitation         | Server crash       |

---

## Known Limitations (Prototype)

These limitations are accepted for this prototype submission as permitted by the assignment specification:

- **No server replication** — the server is a single point of failure
- **No crash recovery** — if the server crashes, the game session cannot be resumed
- **No peer restarts** — disconnected bot clients cannot rejoin a session in progress
- **No Byzantine fault tolerance** — the system does not handle malicious or corrupted messages
- **No security** — player identity is not authenticated

---

## Fault Tolerance Discussion

| Fault | Handling | How |
|---|---|---|
| Network lag | Accepted | Server accepts moves regardless of delay |
| Lost messages | Partial Handling | Game continues with delivered moves; no retry |
| Message reordering | Controlled | Sequential processing at server removes ordering issues |
| Server crash | Not Handled | Documented limitation; no backup server implemented |
| Bot disconnect | Not Handled | Session cannot recover; documented limitation |

---

## AI and Code Attribution

- Initial game logic developed manually
- Code refinement and documentation supported by AI tools
- All logic reviewed and understood before submission

---

## Repository

Repo link here: [https://github.com/prajitabhandari1234/COIT13229-Applied-Distributed-Systems-Assignment-2]