So basically this binary has 3 paths which run at random

flag is in 2 of the paths

in the first where the user get a message "ab sabr karo beta", the program basically sleeps for a long time, to solve youll have to patch it or jump over the function call

the rest of the flag is in the sequence challenge, for that youll have to, get the randomly generated sequence at runtime,
the user input will be transformed then compared to the correctSequence, so the user will have to either patch the transformation function or reverse the transformation function logic, 


```c 
00405b60  uint32_t sub_405b60(char* arg1)

00405b60  {
00405b67      char rax = arg1[9];
00405b6b      char rdx = *(uint8_t*)arg1;
00405b72      int128_t s;
00405b72      __builtin_memset(&s, 0, 0x100);
00405b77      int128_t* i_1 = &s;
00405b81      *(uint8_t*)arg1 = rax;
00405b83      int64_t rax_1 = *(uint64_t*)arg1; //swaps first and last number of the sequence
00405b86      int128_t* i = &s;
00405b89      arg1[9] = rdx;
00405b8c      int128_t* rdx_1 = &s;
00405b8f      s = rax_1;
00405b9d      *(uint16_t*)((char*)s)[8] = *(uint16_t*)(arg1 + 8);
00405c06      void var_10d;
00405c06      
00405c06      do
00405c06      {
00405bee          char rax_3 = (*(uint8_t*)rdx_1 ^ *(uint8_t*)((char*)i + 9));  
00405bf1          i -= 1;
00405bf5          *(uint8_t*)rdx_1 = rax_3;
00405bf7          rax_3 ^= *(uint8_t*)((char*)i + 0xa);
00405bfa          *(uint8_t*)((char*)i + 0xa) = rax_3;
00405bfd          *(uint8_t*)rdx_1 ^= rax_3;
00405bff          rdx_1 += 1;
00405c06      } while (i != &var_10d);
00405c06      
00405c77      do
00405c77      {
00405c40          char rdx_2 = *(uint8_t*)arg1;
00405c43          arg1 = &arg1[1];
00405c71          arg1[-1] = (((((rdx_2 * 2) & 2) + (rdx_2 ^ 1)) & ((rdx_2 - 0x35) >> 7)) | ((rdx_2 - 1) & (((rdx_2 - 0x35) >> 7) - 1))); //actually important part
00405c77      } while (arg1 != &arg1[0xa]);
00405c77      
00405cf2      uint32_t var_10c;
00405cf2      
00405cf2      do
00405cf2      {
00405cc0          char rdx_5 = *(uint8_t*)i_1;
00405cc6          int32_t rcx_3 = (((int32_t)&*(uint32_t*)((char*)var_10c)[3]) - i_1);
00405cc8          i_1 += 1;
00405cd1          int32_t rcx_4 = (rcx_3 & 1);
00405cec          *(uint8_t*)((char*)i_1 - 1) = (((((rdx_5 * 2) & 2) + (rdx_5 ^ 1)) & ((int8_t)-(rcx_4))) | ((rdx_5 - 1) & (rcx_4 - 1)));
00405cf2      } while (i_1 != &*(uint128_t*)((char*)s)[0xa]);
00405cf2      
00405cf4      uint32_t rcx_6 = ((uint32_t)*(uint8_t*)((char*)s)[3]);
00405d0f      uint32_t rax_18 = ((((uint32_t)*(uint8_t*)((char*)s)[5]) + ((uint32_t)*(uint8_t*)((char*)s)[4])) + rcx_6);
00405d0f      
00405d14      if (rax_18 == 0x15)
00405d14      {
00405d1b          rax_18 = (((uint32_t)*(uint8_t*)((char*)s)[6]) * (((uint32_t)*(uint8_t*)((char*)s)[1]) * rcx_6));
00405d1b          
00405d21          if (rax_18 == 0x64)
00405d21          {
00405d23              var_10c = 0x71;
00405d2b              return var_10c;
00405d21          }
00405d14      }
00405d14      
00405d36      return rax_18;
00405b60  }

```

The code is quiet obfuscated, but when running it we can see it just changes our input

```c
do
00405c77      {
00405c40          char rdx_2 = *(uint8_t*)arg1;
00405c43          arg1 = &arg1[1];
00405c71          arg1[-1] = (((((rdx_2 * 2) & 2) + (rdx_2 ^ 1)) & ((rdx_2 - 0x35) >> 7)) | ((rdx_2 - 1) & (((rdx_2 - 0x35) >> 7) - 1))); //actually important part
00405c77      } while (arg1 != &arg1[0xa]);
```
basically transforms the input by incrementing if number <5 and decrementing if number is >5

once you've decoded this grab the correct sequence at runtime, give youre input to match correct sequence after transformation, and get the flag

jumping may or may not work here, since it causes sometimes cause seg faults and patching can be done here too.