#!/usr/bin/env python3

import sys
import os

# usage:  ./wg-cmaker.py <server_public_key> <starting_index> <ending_index> <output_base_name>
# output: ./clients/<output_base_name>{<client_index>}


def write_file(path: str, text: str):
    f = open(path, "w")
    f.write(text)
    f.close()
    pass


def read_file(path: str) -> str:
    f = open(path)
    text = f.read()
    f.close()
    return text


# returns the peer string to be added to
# the wireguard server configuration
def generate_client(index: int, server_public_key: str, output_base_name: str):
    os.system("cd tmp-files; wg genkey | tee privatekey | wg pubkey > publickey")

    private_key = read_file("tmp-files/privatekey").strip()
    public_key = read_file("tmp-files/publickey").strip()

    client_config = (
        read_file("client-config-base.txt")
        .strip()
        .format(
            client_private_key=private_key,
            client_index=index,
            server_public_key=server_public_key,
        )
    )
    host_peer = (
        read_file("host-peer-base.txt")
        .strip()
        .format(client_public_key=public_key, client_index=index)
    )

    os.system("rm -rf tmp-files/*")
    write_file(f"clients/{output_base_name}{index}.conf", client_config)
    return host_peer

def create_folders():
    os.system("mkdir tmp-files; mkdir clients")
    pass


def check_argv() -> (str, int, str):
    if len(sys.argv) < 5:
        print(
            "usage:  ./wg-cmaker.py <server_public_key> <starting_index> <ending_index> <output_base_name>"
        )
        exit(1)
        pass

    server_public_key = sys.argv[1]
    starting_index = int(sys.argv[2])
    ending_index = int(sys.argv[3])
    output_base_name = sys.argv[4]

    return server_public_key, ending_index, starting_index, output_base_name


if __name__ == "__main__":
    server_public_key, ending_index, starting_index, output_base_name = check_argv()
    create_folders()

    print("Add the following block of text to your wireguard server configuration:")
    print("")
    for i in range(starting_index, ending_index + 1):
        print(generate_client(i, server_public_key, output_base_name))
        print("")
        pass
    pass
