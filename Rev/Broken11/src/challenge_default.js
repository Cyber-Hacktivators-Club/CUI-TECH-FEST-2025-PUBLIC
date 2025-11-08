'use strict';

const v8 = require('v8');
const readline = require('readline');

function rol8(x, n) {
  n &= 7;
  return (((x << n) | (x >>> (8 - n))) & 0xFF) >>> 0;
}

function check(flag) {
  if (!flag.startsWith("CHC{") || !flag.endsWith("}")) {
    console.log("Bad format");
    return false;
  }
  const inner = flag.slice(4, -1);
  if (inner.length !== 32) {
    console.log("Flag must have 32 characters inside braces.");
    return false;
  }
  const bytes = Array.from(Buffer.from(inner));


  let ok = true;
  ok = ok && ((((bytes[0] ^ bytes[2]) & 0xFF)) === 0x5e);
  ok = ok && ((((bytes[1] ^ bytes[5]) & 0xFF)) === 0x0e);
  ok = ok && ((((bytes[2] ^ bytes[8]) & 0xFF)) === 0x0e);
  ok = ok && ((((bytes[3] ^ bytes[18]) & 0xFF)) === 0x15);
  ok = ok && ((((bytes[4] ^ bytes[23]) & 0xFF)) === 0x3d);
  ok = ok && ((((bytes[5] ^ bytes[7]) & 0xFF)) === 0x52);
  ok = ok && ((((bytes[6] ^ bytes[25]) & 0xFF)) === 0x08);
  ok = ok && ((((bytes[7] ^ bytes[29]) & 0xFF)) === 0x46);
  ok = ok && ((((bytes[8] ^ bytes[31]) & 0xFF)) === 0x32);
  ok = ok && ((((bytes[9] ^ bytes[20]) & 0xFF)) === 0x34);
  ok = ok && ((((bytes[10] ^ bytes[18]) & 0xFF)) === 0x0f);
  ok = ok && ((((bytes[11] ^ bytes[25]) & 0xFF)) === 0x17);
  ok = ok && ((((bytes[12] ^ bytes[21]) & 0xFF)) === 0x6c);
  ok = ok && ((((bytes[13] ^ bytes[27]) & 0xFF)) === 0x52);
  ok = ok && ((((bytes[14] ^ bytes[10]) & 0xFF)) === 0x05);
  ok = ok && ((((bytes[15] ^ bytes[0]) & 0xFF)) === 0x44);
  ok = ok && ((((bytes[16] ^ bytes[10]) & 0xFF)) === 0x59);
  ok = ok && ((((bytes[17] ^ bytes[22]) & 0xFF)) === 0x00);
  ok = ok && ((((bytes[18] ^ bytes[11]) & 0xFF)) === 0x15);
  ok = ok && ((((bytes[19] ^ bytes[0]) & 0xFF)) === 0x03);
  ok = ok && ((((bytes[20] ^ bytes[9]) & 0xFF)) === 0x34);
  ok = ok && ((((bytes[21] ^ bytes[25]) & 0xFF)) === 0x57);
  ok = ok && ((((bytes[22] ^ bytes[1]) & 0xFF)) === 0x37);
  ok = ok && ((((bytes[23] ^ bytes[1]) & 0xFF)) === 0x0a);
  ok = ok && ((((bytes[24] ^ bytes[1]) & 0xFF)) === 0x5c);
  ok = ok && ((((bytes[25] ^ bytes[14]) & 0xFF)) === 0x08);
  ok = ok && ((((bytes[26] ^ bytes[1]) & 0xFF)) === 0x37);
  ok = ok && ((((bytes[27] ^ bytes[25]) & 0xFF)) === 0x02);
  ok = ok && ((((bytes[28] ^ bytes[19]) & 0xFF)) === 0x04);
  ok = ok && ((((bytes[29] ^ bytes[30]) & 0xFF)) === 0x2d);
  ok = ok && ((((bytes[30] ^ bytes[20]) & 0xFF)) === 0x34);
  ok = ok && ((((bytes[31] ^ bytes[26]) & 0xFF)) === 0x0a);
  ok = ok && ((((rol8(bytes[31], 2) ^ bytes[27]) & 0xFF)) === 0x33);
  ok = ok && ((((bytes[20] + bytes[27] + 48) & 0xFF)) === 0x01);
  ok = ok && (((((bytes[29] * 2) + bytes[23]) & 0xFF)) === 0x46);
  ok = ok && ((((bytes[1] + bytes[12] + 13) & 0xFF)) === 0xd4);
  ok = ok && (((((bytes[18] * 5) + bytes[27]) & 0xFF)) === 0x64);
  ok = ok && ((((rol8(bytes[11], 1) ^ bytes[27]) & 0xFF)) === 0x80);
  ok = ok && ((((rol8(bytes[20], 2) ^ bytes[5]) & 0xFF)) === 0xcb);
  ok = ok && (((((bytes[22] * 7) + bytes[10]) & 0xFF)) === 0x02);
  ok = ok && ((((rol8(bytes[2], 6) + (bytes[29] ^ bytes[27])) & 0xFF)) === 0x6e);
  ok = ok && ((((bytes[19] + bytes[2] + 35) & 0xFF)) === 0xc0);
  ok = ok && ((((rol8(bytes[23], 1) + (bytes[24] ^ bytes[1])) & 0xFF)) === 0x20);
  ok = ok && ((((bytes[14] + bytes[12] + 30) & 0xFF)) === 0xe9);
  ok = ok && ((((rol8(bytes[18], 2) ^ bytes[0]) & 0xFF)) === 0xae);
  ok = ok && ((((bytes[23] + bytes[9] + 17) & 0xFF)) === 0xd2);
  ok = ok && ((((rol8(bytes[25], 3) + (bytes[19] ^ bytes[19])) & 0xFF)) === 0x23);
  ok = ok && ((((rol8(bytes[14], 1) ^ bytes[8]) & 0xFF)) === 0xbf);
  ok = ok && ((((bytes[21] + bytes[8] + 2) & 0xFF)) === 0x9c);
  ok = ok && ((((bytes[28] + bytes[16] + 41) & 0xFF)) === 0x89);
  ok = ok && ((((rol8(bytes[16], 3) + (bytes[13] ^ bytes[18])) & 0xFF)) === 0xd3);
  ok = ok && ((((rol8(bytes[7], 3) ^ bytes[23]) & 0xFF)) === 0xc3);
  if (ok)
    console.log("✅ Correct! Flag accepted.");
  else
    console.log("❌ Wrong flag.");
  return ok;
}
function main(){
    const arg = process.argv[2];
    if (arg) check(arg.trim());
    else {
      const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
      rl.question("Enter flag: ", (f) => { check(f.trim()); rl.close(); });
    }
}

if (v8.startupSnapshot && v8.startupSnapshot.isBuildingSnapshot()) {
    v8.startupSnapshot.setDeserializeMainFunction(main);
} else {
    main();
}
