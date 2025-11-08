Full Writeup coming soon

1. Use scallop to extract the code cache
2. Reverse the NodeJS Bytecode to build the logic backwards to find constraints (https://swarm.ptsecurity.com/guide-to-p-code-injection/ , https://github.com/PositiveTechnologies/ghidra_nodejs/) , 
3. Second way of solving it is reconstructing hash of code_Cache by analyzing code-serializer.cc from nodejs source code , below script will be a good starting point: https://x64.ooo/posts/2025-04-21-nodejs-sea-script-stomping/
4. Use solver script to solve the challenge 