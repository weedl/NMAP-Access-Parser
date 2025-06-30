# NMAP-Access-Parser
A tool that parses nmap output to create files that may be interesting for further testing, or simply for documentation purposes.

The tool is very convinent if you are testing a large network and do not want to perform a port scan on all available hosts on the network.
My preffered workflow is to first do a pingsweep with `nmap -sn [x.x.x.x/x] -oA [outfile]`. Thereafter, I use this tool to parse out all hosts that are alive with `nparser.py [gnmap_file]`.
This will output a file containing all hosts that are alive. From here, you can run an nmap scan of all alive hosts with `nmap -iL [live_hosts.txt] -sC -sV` or your preffered scanning method. 

-o | output filename. Defaults to "live_hsots.txt" if the flag is not used.  
-f | Subnet file. Give the tool a list of subnets and allow it to output which subnets you are able to reach based on the nmap output.
