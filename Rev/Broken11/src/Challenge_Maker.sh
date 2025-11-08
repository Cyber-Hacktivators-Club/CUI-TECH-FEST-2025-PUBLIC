#Node version v23.11.1
$Flag="Fin4lly_P_c0d3_0r_c0d3_c4v3_d0n3"
$Fake_Flag="7his_fl4g_is_4ls0_f4k3_b4d_f0r_U"
$Filename="challenge.js"
python SMT_2_js.py $Fake_Flag 
python SMT_2_js.py $Flag $Filename
node --experimental-sea-config sea-config.json
node -e "require('fs').copyFileSync(process.execPath, 'challenge2.exe')" 
npx postject challenge2.exe NODE_SEA_BLOB sea-prep.blob --sentinel-fuse NODE_SEA_FUSE_fce680ab2cc467b6e072b8b5df1996b2
#pip install node-sea-scallop
scallop repack  challenge2.exe challenge_default.js --stomp
cp challenge2.exe "../dist/challenge2.exe"
cp solver.py "../writeup/solver.py"