import base64
import datetime
import requests
from bs4 import BeautifulSoup

LOOKED_NODES = set()


def decode_and_print_flag(encoded_flag):
    # Found the flag in base64 format (it is double encoded)
    print(f'>>> FLAG NODE FOUND')
    print(f'Raw node: {encoded_flag}')
    decode_1 = base64.b64decode(encoded_flag)
    print(f'First b64 decoding: {decode_1}')
    flag = base64.b64decode(decode_1)
    print(f'Final Flag: {flag}')


def get_nodes_from_content(content):
    parsed_html = BeautifulSoup(content, features='lxml')

    paste_urls_location = parsed_html.body.find('td', attrs={'class': 'code'}).find('pre')
    paste_urls = paste_urls_location.contents[1].split('\n')
    node_urls = [url.strip() for url in paste_urls if url]
    
    return node_urls


def recursive_solve():
    initial_node = 'http://paste.ubuntu.com/p/HnGHwGk4rQ/'
    _recursive_solve(initial_node)


def _recursive_solve(node_url):
    if node_url in LOOKED_NODES:
        print(f'> Repeated node {node_url}')
        return
    
    LOOKED_NODES.add(node_url)
    print(f'> Doing request to {node_url}')
    response = requests.get(node_url)
    
    if response.status_code == 200:
        for node in get_nodes_from_content(response.text):
            if 'http://' in node:
                found = _recursive_solve(node)
                if found:
                    return True
            if node.endswith('=='):
                # Flag found!
                decode_and_print_flag(node)
                return True


def while_solve():
    looked_nodes = set()
    continue_scrapping = True

    initial_node = 'http://paste.ubuntu.com/p/HnGHwGk4rQ/'
    nodes = [initial_node]

    while nodes and continue_scrapping:
        next_node = nodes.pop(0)

        if next_node.endswith('=='):
            # Flag found!
            decode_and_print_flag(next_node)
            continue_scrapping = False

        else:
            if next_node in looked_nodes:
                print(f'> Repeated node {next_node}')
            
            looked_nodes.add(next_node)
            print(f'> Doing request to {next_node}')
            response = requests.get(next_node)

            if response.status_code == 200:
                nodes += get_nodes_from_content(response.text)


if __name__ == "__main__":
    begin_time = datetime.datetime.now()
    #recursive_solve()
    while_solve()
    print(f'Total execution time: {datetime.datetime.now() - begin_time}')