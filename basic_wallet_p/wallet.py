import hashlib
import requests

import sys
import json
import random

id = None

def proof_of_work(block):
    print("Looking for proof...")
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    # Turn JSON into string
    block_str = json.dumps(block, sort_keys=True)
    proof = random.random()

    # Add to proof until have a valid proof
    while not valid_proof(block_str, proof):
        proof = random.random()

    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    guess_valid = guess_hash[:6] == "000000"
    if guess_valid:
        print(f"Found proof {proof} with hash {guess_hash}!")
    return guess_valid


def mine(*args):
    if len(args) < 1:
        print("Please enter a username.")
        return
    username = args[0]
    print(f"Welcome {username}! Mining a block...")
    r = requests.get(url=node + "/last_block")
    # Handle non-json response
    try:
        data = r.json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(r)
        return

    # Get data block
    new_proof = proof_of_work(data["block"])

    # When found, POST it to the server {"proof": new_proof, "id": id}
    post_data = {"proof": new_proof, "id": username}

    # Mine block
    r = requests.post(url=node + "/mine", json=post_data)
    data = r.json()

    # Return message
    if data["message"] == "New Block Forged":
        print(f"You found a coin!")
    else:
        print(data["message"])

CMDS = {
    "mine": mine,
}


if __name__ == "__main__":
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    node = "http://localhost:5000"
    if len(sys.argv) > 1:
        if sys.argv[1] in CMDS:
            cmd = sys.argv[1]
            CMDS[cmd](*sys.argv[2:])