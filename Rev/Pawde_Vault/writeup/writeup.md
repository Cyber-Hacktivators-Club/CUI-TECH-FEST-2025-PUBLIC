In order to solve this youll need to transfer 170000 to fangs account

Recovering Account: 

in the perform securitycheck function, youll need to reverse the account checks - 

```c
00406cb1                                    if (*std::string::operator[](this: &var_88, __pos: 0)
00406cb1                                            != 0x45)
00406d13                                        rax_67 = 1
00406cb1                                    else if (*
00406cb1                                            std::string::operator[](this: &var_88, __pos: 2)
00406cb1                                            != 0x49)
00406d13                                        rax_67 = 1
00406cc9                                    else if (*
00406cc9                                            std::string::operator[](this: &var_88, __pos: 4)
00406cc9                                            != 0x33)
00406d13                                        rax_67 = 1
00406ce1                                    else if (*
00406ce1                                            std::string::operator[](this: &var_88, __pos: 5)
00406ce1                                            != 0x56)
00406d13                                        rax_67 = 1
00406cf9                                    else if (*
00406cf9                                            std::string::operator[](this: &var_88, __pos: 6)
00406cf9                                            == 0x33)

```

this gives us "E I 3VE"
```c

v25 = *(_BYTE *)__gnu_cxx::__normal_iterator<char *,std::string>::operator*(&v16);
        if ( v25 <= 32 || v25 == 127 )
          std::string::operator+=(v20, (unsigned int)v25);
        else
          std::string::operator+=(v20, (unsigned int)(char)((v25 + 14) % 94 + 33));
        __gnu_cxx::__normal_iterator<char *,std::string>::operator++(&v16);
      }
      if ( (unsigned __int8)std::operator!=<char>(v20, "#dhacf`") )
      {
        v5 = 0;

```

this is a simple ROT which on the substring gives us the string "R592471"
    account: "E I 3VER592471"

```c
v28 = std::string::find(v22, 45LL, 0LL);
        std::string::substr(v19, v22, v28 + 1, -1LL);
        qmemcpy(v18, " #&!r$$'''", sizeof(v18));
        if ( std::string::length(v19) == 10 )
        {
          for ( j = 0LL; ; ++j )
          {
            v8 = std::string::length(v19);
            if ( j >= v8 )
              break;
            v26 = *(_BYTE *)std::string::operator[](v19, j) ^ 0x42;
            if ( v26 != v18[j] )
            {
              v5 = 0;
              goto LABEL_48;
            }
          }
        }    
```
this part gives us the last part of the account number badc0ffeee

final account number "E I 3VER592471-badcoffeee"

the empty spaces arent checked

Note: various dummy operations are used so be careful also avoid the clean slate function

place this in the file and login in normal mode to get the passwd
(you can get that at runtime or by analyzing the binary as well)

lastly login with "./vault -admin"

enter token which is the username of the device yr using
and admin passwd can be found by decoding the authadmin function

transfer the amount to fangs account and get the flag