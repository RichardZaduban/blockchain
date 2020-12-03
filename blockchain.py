#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 21:02:37 2020

@author: richard
"""

import datetime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        self.chain = []
        self.createBlock(proof = 1, previous_hash = '0')
        
    def createBlock(self, proof, previous_hash):
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block
    
    def getPreviousBlock(self):
        return self.chain[-1]
    
    def proofOfWork(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hesh(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def isChainValid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hesh(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block  = block
            block_index += 1
        return True
    
    
app = Flask(__name__)


blockchain = Blockchain()


@app.route('/mine_block', methods = ['GET'])
def mineBlock():
    previous_block = blockchain.getPreviousBlock()
    previous_proof = previous_block['proof']
    proof = blockchain.proofOfWork(previous_proof)
    previous_hash = blockchain.hesh(previous_block)
    block = blockchain.createBlock(proof, previous_hash)
    response = {'message': 'Congratulations you just mine a block',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

@app.route('/get_chain', methods = ['GET'])
def getChain():
    response = {'chain': blockchain.chain,
                'lenght': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/is_valid', methods = ['GET'])
def isValid():
    is_valid = blockchain.isChainValid(blockchain.chain)
    if is_valid:
        response = {'message': 'Blockchain is valid'}
    else:
        response = {'message': 'Blockchain is not valid'}
    return jsonify(response), 200
        

app.run(host= '0.0.0.0', port= 5000)