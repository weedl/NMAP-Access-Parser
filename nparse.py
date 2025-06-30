import sys
import argparse
from ipaddress import ip_network, ip_address

def parse_gnmap(file_path):
    up_hosts = []

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("Host:") and "Status: Up" in line:
                parts = line.split()
                if len(parts) > 1:
                    ip = parts[1]
                    up_hosts.append(ip)

    return up_hosts

def load_target_subnets(file_path):
    subnets = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    net = ip_network(line)
                    subnets.append(net)
                except ValueError:
                    print(f"[-] Invalid subnet format: {line}")
    return subnets

def filter_reached_subnets(up_hosts, target_subnets):
    reached = set()
    for subnet in target_subnets:
        for host in up_hosts:
            if ip_address(host) in subnet:
                reached.add(str(subnet))
                break  # Found one host in this subnet, move to next subnet
    return sorted(reached)

def main():
    parser = argparse.ArgumentParser(description="Parse .gnmap file and find reachable subnets.")
    parser.add_argument("gnmap_file", help="Input .gnmap file from Nmap")
    parser.add_argument("-f", "--subnet-file", required=True, help="File containing list of subnets to check (CIDR format)")
    parser.add_argument("-o", "--output", default="reachable_subnets.txt", help="Output file for reachable subnets")
    args = parser.parse_args()

    up_hosts = parse_gnmap(args.gnmap_file)
    target_subnets = load_target_subnets(args.subnet_file)
    reached_subnets = filter_reached_subnets(up_hosts, target_subnets)

    with open(args.output, 'w') as f:
        for subnet in reached_subnets:
            f.write(subnet + '\n')

    print(f"[+] Found {len(up_hosts)} up hosts in gnmap file")
    print(f"[+] {len(reached_subnets)} subnets were reachable and written to {args.output}")

if __name__ == "__main__":
    main()

