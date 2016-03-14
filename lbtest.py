#!/usr/bin/env python

import os
import sys
import socket
import argparse
import requests
import subprocess


def main(req, lb):
    results = doRequests(req, lb)
    printResult(results)


def setUpEnvironment(nodes):
    os.environ["WEB_NODES_NUMBER"] = str(nodes)

    try:
        print("Setting up environment...")
        subprocess.check_call(["vagrant", "up", "--provision"])
    except:
        print("Failed setting up the environment")
        sys.exit(1)


def tearDownEnvironment():
    try:
        print("Tearing down the environment...")
        subprocess.check_call(["vagrant", "halt"])
    except:
        print("Failed tearing down the environment")
        sys.exit(1)


def doRequests(req, lb):
    results = {}

    for request in range(1, req+1):
        try:
            r = requests.get("http://{}/".format(lb), timeout=5)
            if r.status_code == 200:
                node_id = r.headers['X-Web-Node-Id']
                if node_id in results:
                    results[node_id] = results[node_id]+1
                else:
                    results[node_id] = 1
            else:
                print("Request #{} failed, status {}"
                      .format(request, r.status_code))
        except requests.exceptions.Timeout:
            print("Request #{} failed, connection timed out".format(request))

    return results


def printResult(results):
    print("*************************************")
    print("* Load balancer distribusion result *")
    print("*************************************")

    for node, count in results.items():
        print("{}: {}".format(node, count))

    print("*************************************")


def getArgs():
    parser = argparse.ArgumentParser(description="Test how a load balancer is \
                                     distributing client requests across a \
                                     group of servers.")
    parser.add_argument("-n", "--nodes", help="number web server nodes",
                        type=int, default=3)
    parser.add_argument("-l", "--loadbalancer", help="load balancer ip address",
                        default="192.168.0.5")
    requiredNamed = parser.add_argument_group("required named arguments")
    requiredNamed.add_argument("-r", "--requests", help="number of http requests",
                               type=int, required=True)

    _validate(parser.parse_args())
    return parser.parse_args()


def _validate(args):
    try:
        socket.inet_aton(args.loadbalancer)
    except socket.error:
        print("Load balancer IP address is not valid!")
        sys.exit(1)

if __name__ == "__main__":
    args = getArgs()
    try:
        setUpEnvironment(args.nodes)
        main(args.requests, args.loadbalancer)
    finally:
        tearDownEnvironment()
