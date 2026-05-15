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

- The **client sends player moves** to the server using PUSH
- The **server processes all moves in arrival order**
- The **server broadcasts updated game state** using PUB
- **Bots are controlled inside the server**
- Each move includes a **sequence number (seq)**
- The server tracks **last_move_seq per player**
- Clients wait until their move is processed before rendering

```
Human Client ──PUSH──▶ Server (Sequencer) ──PUB──▶ All Clients
```
---

## Consistency Model


The system implements **Sequential Consistency**.

### Properties:

- All moves are processed by a **single server**
- Moves are applied in strict **arrival order**
- The server defines the **global order of execution**
- All clients receive updates in the same order
- All players observe the **same game state**

### Trade-off:

- Single point of failure (server)
-  No crash recovery implemented (prototype limitation)

---

## Project Structure

```text
gold-miner/
├── docs/                         # Assignment documentation
├── plantuml code/                # PlantUML source files
│   ├── architectureDiagram.puml
│   ├── classDiagram.puml
│   ├── deploymentDiagram.puml
│   ├── faultSequenceDiagram.puml
│   └── sequenceDiagram.puml
│
├── Screenshots/                  # Runtime and testing screenshots
│   ├── client-gameplay.png
│   ├── fault-handling.png
│   ├── multi-client-sync.png
│   ├── pytest-results.png
│   ├── server-running.png
│   └── server-move-log-stopped.png
│
├── System Design Diagram/        # Exported PNG diagrams
│   ├── Architecture Diagram.png
│   ├── Class Diagram.png
│   ├── Deployment Diagram.png
│   ├── Fault Sequence Diagram.png
│   └── Sequence Diagram.png
│
├── src/
│   ├── server.py                 # Sequencer server
│   ├── client.py                 # Human player client
│   └── game.py                   # Shared game logic
│
├── tests/
│   ├── test_game.py              # Functional game tests
│   └── test_faults.py            # Distributed fault tolerance tests
│
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
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
Functional Testing

| Test Case         | Description                   | Expected Result                 |
| ----------------- | ----------------------------- | ------------------------------- |
| Movement tests    | Player movement correctness   | Position updates correctly      |
| Boundary tests    | Prevent leaving grid          | Player stays within grid        |
| Gold collection   | Collect gold                  | Score increases + gold respawns |
| Max player test   | 100-player limit              | Extra players rejected          |
| Bot movement test | Bot moves toward nearest gold | Correct direction selected      |
| Gold respawn test | Gold appears after collection | New position generated          |

Distributed Fault Testing
| Test Case        | Description              | Expected Result                |
| ---------------- | ------------------------ | ------------------------------ |
| Lag simulation   | Delayed move applied     | Move still processed           |
| Lost message     | Some moves dropped       | System continues correctly     |
| Sequential order | Ordered execution        | Correct final state            |
| Reordering test  | Different order of moves | Different result               |
| Multi-user test  | Multiple players move    | Independent positions          |
| Node crash test  | Server stops             | Client stops receiving updates |


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

| Fault              | Handling    | Explanation                               |
| ------------------ | ----------- | ----------------------------------------- |
| Network lag        | Accepted    | Server processes delayed messages         |
| Lost messages      | Partial     | Only delivered moves are applied          |
| Message reordering | Controlled  | Server enforces sequential consistency    |
| Client timeout     | Handled     | Client detects failure using ZMQ RCVTIMEO |
| Server crash       | Not handled | System stops (no recovery implemented)    |
| Bot disconnect     | Not handled | No restart/rejoin support                 |


---

## AI and Code Attribution

- Initial game logic developed manually
- Code refinement and documentation supported by AI tools
- All logic reviewed and understood before submission

---

## Repository

Repo link here: [https://github.com/prajitabhandari1234/COIT13229-Applied-Distributed-Systems-Assignment-2]

## Video
Video link here: [https://cqu365-my.sharepoint.com/:v:/g/personal/prajita_bhandari_cqumail_com/IQAXLTlFPh0mRajgeGwIN4feAVIUAGyS0Ozwu3ZswsAoyMY?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=qeog2U]



