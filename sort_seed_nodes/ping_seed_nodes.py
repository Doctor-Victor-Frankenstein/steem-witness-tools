from ping3 import ping, verbose_ping
from datetime import datetime, timedelta, date
import argparse

unofficial_seed_nodes = [
    {'url': 'steemseed-fin.privex.io', 'port': 2001, 'owner': 'privex'},
    {'url': 'gtg.steem.house', 'port': 2001, 'owner': 'gtg'},
    {'url': 'seed.steemnodes.com', 'port': 2001, 'owner': 'wackou'},
    {'url': '192.99.3.29', 'port': 2001, 'owner': 'joseph'},
    {'url': '5.9.18.213', 'port': 2001, 'owner': 'pfunk'},
    {'url': 'lafonasteem.com', 'port': 2001, 'owner': 'lafona'},
    {'url': 'seed.rossco99.com', 'port': 2001, 'owner': 'rossco99'},
    {'url': 'steem-seed.altcap.io', 'port': 40696, 'owner': 'ihashfury'},
    {'url': 'seed.steemfeeder.com', 'port': 2001, 'owner': 'au1nethyb1'},
    {'url': 'seed.roelandp.nl', 'port': 2001, 'owner': 'roelandp'},
    {'url': 'steem.global', 'port': 2001, 'owner': 'klye'},
    {'url': 'seed.esteem.ws', 'port': 2001, 'owner': 'good-karma'},
    {'url': '176.31.126.187', 'port': 2001, 'owner': 'timcliff'},
    {'url': 'seed.thecryptodrive.com', 'port': 2001, 'owner': 'thecryptodrive'},
    {'url': 'steem-id.altexplorer.xyz', 'port': 2001, 'owner': 'steem-id'},
    {'url': 'seed.bitcoiner.me', 'port': 2001, 'owner': 'bitcoiner'},
    {'url': '104.199.118.92', 'port': 2001, 'owner': 'clayop'},
    {'url': 'seed.steemviz.com', 'port': 2001, 'owner': 'ausbitbank'},
    {'url': 'steem-seed.lukestokes.info', 'port': 2001, 'owner': 'lukestokes'},
    {'url': 'seed.blackrift.net', 'port': 2001, 'owner': 'drakos'},
    {'url': 'seed.jerrybanfield.com', 'port': 2001, 'owner': 'jerrybanfield'},
    {'url': 'node.mahdiyari.info', 'port': 2001, 'owner': 'mahdiyari'},
    {'url': 'anyx.co', 'port': 2001, 'owner': 'anyx'},
]



if __name__ == "__main__":
    
    parser.add_argument('--input', nargs='?', const=1, type=str, default="seednodes.txt")
    parser.add_argument("--maxdelay", help="Defines the maximum allowed delay in ms", nargs='?', const=1, type=int, default=100)
    args = parser.parse_args()    
    
    seed_nodes_list = args.input
    allowed_max_delay_ms = args.maxdelay
    today = '%d/%d/%d' % (date.today().day, date.today().month, date.today().year)
    filename_out = "sorted_seednodes_%s.txt" % today
    
    
    with open(seed_nodes_list) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    seed_nodes = []
    for line in content:
        node = {}
        x = line.split(":")
        y = x[1].split("#")
        node["url"] = x[0].strip()
        node["port"] = int(y[0].strip())
        node["owner"] = y[1].strip()
        seed_nodes.append(node)
    for node in unofficial_seed_nodes:
        found = False
        for node_official in seed_nodes:
            if node_official["url"] == node["url"]:
                found = True
                break
        if not found:
            seed_nodes.append(node)
    
    
    
    node_list =[]
    for node in seed_nodes:
        hostname = node["url"]
        delay = ping(hostname, timeout=2)
        if delay is not None:
            print("%s: %.2f ms" %(hostname, delay*1000))
            node["delay_ms"] = delay*1000
        else:
            node["delay_ms"] = 100e3
        node_list.append(node)
    sorted_nodes = sorted(node_list, key=lambda node: node['delay_ms'], reverse=False)
    

    f = open(filename_out, 'w')
    
    for node in sorted_nodes:
        if node["delay_ms"] == 100e3:
            continue
        if node["delay_ms"] > allowed_max_delay_ms:
            continue
        spaces = 30 - len(node["url"]) - 1 - len(str(node["port"]))
        node_string = ("seed-node = %s:%d  %s # %s (%.2f ms)" % (node["url"], node["port"], ' ' * spaces, node["owner"], node["delay_ms"]))
        print(node_string)
        f.write(node_string+'\n')
    f.close()
