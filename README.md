# COIT13229 Applied Distributed Systems Assignment 2

## Project Title
Gold Miner Distributed Game

## Description
This project is a distributed text-based Gold Miner game developed in Python.
A human player can play against bots across a network. The system uses a server/sequencer architecture to order player moves and maintain a consistent game state.

## Technologies
- Python
- ZeroMQ
- Pytest
- GitHub

## Main Features
- Text-based 20x20 Gold Miner game
- Human player and bot players
- Server/client distributed architecture
- Sequential consistency using a sequencer server
- Fault tests for lag, lost messages, and node crashes

## How to Install

```bash
pip install -r requirements.txt