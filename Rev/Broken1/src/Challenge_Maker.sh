$Flag="N0d3_S34_4pps_4r3_r34lly_c00l_DD"
$Filename="challenge.js"
python SMT_2_js.py $Flag $Filename
node --experimental-sea-config sea-config.json
node -e "require('fs').copyFileSync(process.execPath, 'challenge1.exe')" 
npx postject challenge1.exe NODE_SEA_BLOB sea-prep.blob --sentinel-fuse NODE_SEA_FUSE_fce680ab2cc467b6e072b8b5df1996b2
cp challenge1.exe "../dist/challenge1.exe"
cp solver.py "../writeup/solver.py"