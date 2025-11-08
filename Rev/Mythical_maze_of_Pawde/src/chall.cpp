//  g++ chall.cpp -fvisibility=hidden -fvisibility-inlines-hidden -O2 -static -s -Wl,-T,sections.ld -o chall
// strip --strip-all chall
// sstrip chall
//


#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <ctime>
#include <functional>
#include <cstdlib>
#include <cstring>
#include <chrono>
#include <thread>
#include <string>
#include <sstream>
#include <iomanip>
#include <cstdint>
#include <signal.h>
#include <sys/ptrace.h>

const int o0 = 10;
std::string message = "1234567890abcdefghijkmnopqrstuvwxyz_.:;{}[]()ÖÄææ¨Å~";
std::string song1 = "CAN YOU SEE";
std::string song2 = "HERE ME  OUT!!!";
std::string song3 = "CAN YOU HEAR??";
std::string song4 = "IN ORDER TO GET the flag";
std::string song5 = "The p4th shall only be revealed once you";
std::string song6 = "Know how the true way to get the flag";

std::string song7 = "Youll need to ...... connection disrupted";

const char* FLAG = "heres your hint";

std::string longAssString = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_abcdefghijklmnopqrstuvwxyz{|}~";

// ---------------------- existing helper functions (unchanged) ----------------------
void generateSequence(char* sequence) {
    srand(time(0));  // Initialize random seed
    for (int i = 0; i < o0; i++) {
        sequence[i] = '2' + (rand() % 7);  // Random digit between 2 and 8
    }
}

int checkSequence(char* inputSequence, char* correctSequence) {
    for (int i = 0; i < o0; i++) {
        if (inputSequence[i] != correctSequence[i]) {
            return 0;  // Mismatch
        }
    }
    return 1;  // Match
}

void getbracket() {
    std::function<char(const std::string&)> get_first_char;
    get_first_char = [](const std::string& str) -> char {
        return str.at(39);
    };
    std::function<void(char)> printer;
    printer = [](char c) {
        std::cout << c;
    };
    char ch = get_first_char(message);
    printer(ch);
}

void grab(int index) {
    std::function<char(const std::string&, int)> get_char_at_index;
    get_char_at_index = [](const std::string& str, int idx) -> char {
        if (idx >= 0 && idx < (int)str.length()) {
            return str.at(idx);
        } else {
            std::cerr << "Index out of bounds\n";
            return '\0';
        }
    };
    std::function<void(char)> printer;
    printer = [](char c) {
        std::cout << c;
    };
    char ch = get_char_at_index(longAssString, index);
    if (ch != '\0') {
        printer(ch);
    }
}
void getNL() { std::cout << "\n"; }

void grab2(int index) {
    std::function<char(const std::string&, int)> get_char_at_index;
    get_char_at_index = [](const std::string& str, int idx) -> char {
        if (idx >= 0 && idx < (int)str.length()) {
            return str.at(idx);
        } else {
            std::cerr << "Index out of bounds\n";
            return '\0';
        }
    };
    std::function<void(char)> printer;
    printer = [](char c) {
        std::cout << c ;
    };
    char ch = get_char_at_index(message, index);
    if (ch != '\0') {
        printer(ch);
    }
}

const char* hnt = " yrnea gb gvzrfxvc vs lbh uniag lrg";

void getSpace() { std::cout << " "; }

void grab3(int index) {
    std::function<char(const std::string&, int)> get_char_at_index;
    get_char_at_index = [](const std::string& str, int idx) -> char {
        if (idx >= 0 && idx < (int)str.length()) {
            return str.at(idx);
        } else {
            std::cerr << "Index out of bounds\n";
            return '\0';
        }
    };
    std::function<void(char)> printer;
    printer = [](char c) {
        std::cout << c ;
    };
    char ch = get_char_at_index(song6, index);
    if (ch != '\0') {
        printer(ch);
    }
}

void getbracketclose() {
    std::function<char(const std::string&)> get_first_char;
    get_first_char = [](const std::string& str) -> char {
        return str.at(40);
    };
    std::function<void(char)> printer;
    printer = [](char c) {
        std::cout << c;
    };
    char ch = get_first_char(message);
    printer(ch);
}

void getHint() {
    getNL(); grab(82); grab(70); grab(67); getSpace(); grab(80); grab(67); grab(81); grab(82); getSpace();grab(77);
    grab(68);  getSpace(); grab(71); grab(82);  getSpace(); grab(71); grab(81);  getSpace(); grab(71); grab(76);  getSpace(); grab(82);
    grab(70); grab(67);  getSpace(); grab(81); grab(67); grab(79); grab(83); grab(67); grab(76);
    grab(65); grab(67);  getSpace(); grab(65); grab(70); grab(63); grab(74); grab(74);
}

void getChar(){ //test
    std::cout <<"\n";
    std::cout << song1.at(0);
    std::cout << song2.at(0);
    std::cout << song1.at(0);
}

void printMessage(int val) {
    std::cout << "You entered: " << val << std::endl;
}

void printFlag(int hash, int expectedHash) {
    std::cout << "Congratulations" << FLAG << hnt <<"\n"<<std::endl;
}

void printRapta2(int val) {
    std::cout << "Aik mun pe rapta mara na, din mein flag dikhai parhein ge"<< std::endl;
}

void sabr(int waqt){
     std::this_thread::sleep_for(std::chrono::seconds(waqt));
}

void getDaString() {
    //CHC{Th3_C0rrectt_p4th_shall_giv_y0u_th3_fl4g}
    grab(51);
    grab(70);
    grab2(2);
    grab2(35);
    grab(34);
    grab2(9);
    grab(80);
    grab2(26);
    grab2(14);
    grab(65);
    grab2(28);
    grab2(28);
}
extern "C" {
    extern const char __start_flagchk[]; // linker-provided
    extern const char __stop_flagchk[];
}



static const uint32_t EXPECTED_FLAGCHK_CRC = 0x10EDC0ED; // <-- REPLACE after build

static uint32_t crc32_table[256];
static bool crc_table_init = false;
static void crc32_init() {
    if (crc_table_init) return;
    for (uint32_t i = 0; i < 256; ++i) {
        uint32_t c = i;
        for (int j = 0; j < 8; ++j)
            c = c & 1 ? 0xEDB88320u ^ (c >> 1) : c >> 1;
        crc32_table[i] = c;
    }
    crc_table_init = true;
}
static uint32_t crc32(const uint8_t* buf, size_t len) {
    crc32_init();
    uint32_t c = 0xFFFFFFFFu;
    for (size_t i = 0; i < len; ++i){
        if (buf[i] == 0xCC)
            continue;
        c = crc32_table[(c ^ buf[i]) & 0xFFu] ^ (c >> 8);
    }
    return c ^ 0xFFFFFFFFu;
}


static void crash_on_tamper() {
    std::cerr << "Hoshiyari kar rya ae\n";
    raise(SIGILL);
}

void getDaString3() {
    grab(71);
    grab(84);
    grab2(35);
    grab2(33);
    grab(15);
    grab2(29);
    grab2(35);
    grab3(9);
    grab3(5);
    grab2(2);
    grab2(35);
    grab3(33);
    grab3(34);
    grab(19);
    grab3(36); getbracketclose();
}

void printRapta(int val) {
    std::cout << "Aik mun pe rapta mara na, din mein flag dikhai parhein ge"<< std::endl;
}

void getDaString2(){
    std::cout << message.at(35);
    std::cout << song5.at(4);
    std::cout << song5.at(5);
    std::cout << song5.at(6);
    std::cout << song5.at(7);
    std::cout << message.at(35);
    std::cout << song5.at(9);
    std::cout << song5.at(10);
    std::cout << song5.at(11);
    std::cout << song5.at(12);
    std::cout << song5.at(12);
    std::cout << message.at(35);
    std::cout << song4.at(12);
    getDaString3();
}

void nikal()
{
    getChar();
    getbracket();
    getDaString();
    getHint();
    exit(0);
}

void xor_mutate_string(std::string &s, const char* seq, size_t seq_len) {
    if (!seq || seq_len == 0) return;

    for (size_t i = 0; i < s.size(); ++i) {
        uint8_t a = static_cast<uint8_t>(s[i]);
        uint8_t b = static_cast<uint8_t>(seq[i % seq_len]);
        s[i] = static_cast<char>(a ^ b);
    }
}

// XOR all global strings (encryption)
void xor_encrypt_globals(const char* seq, size_t seq_len) {
    std::vector<std::reference_wrapper<std::string>> targets = {
        message,
        longAssString,
        song1,
        song2,
        song3,
        song4,
        song5,
        song6,
        song7
    };

    for (auto &ref : targets) {
        xor_mutate_string(ref.get(), seq, seq_len);
    }
}

void path2_explored(){
    int time = 604800;
    std::cout << "Ab sabr karo beta"  << std::endl;
    sabr(time);
    std::cout << "thanks for waiting, now exiting"  << std::endl;
    nikal();
    return;
}

void xor_decrypt_globals(const char* seq, size_t seq_len) {
    xor_encrypt_globals(seq, seq_len); // same operation decrypts
}

// ---------------------- transformInput (unchanged MBA obfuscation) ----------------------
void transformInput(char* input) {
    if (!input || o0 == 0) return;

    // XOR-swap first and last (keeps original behavior)
    input[0] ^= input[9];
    input[9] ^= input[0];
    input[0] ^= input[9];

    // --- copy to var2 (same size as before) ---
    char var2[256] = {0};
    std::memcpy(var2, input, o0 > 255 ? 255 : o0);
    var2[o0 < 255 ? o0 : 255] = '\0';

    // --- reverse var2 using XOR-swap ---
    for (size_t i = 0; i < o0 / 2; ++i) {
        size_t j = o0 - i - 1;
        uint8_t *a = reinterpret_cast<uint8_t*>(&var2[i]);
        uint8_t *b = reinterpret_cast<uint8_t*>(&var2[j]);
        *a ^= *b;
        *b ^= *a;
        *a ^= *b;
    }

    // --- original MBA-style transformation on input ---
    for (size_t i = 0; i < o0; ++i) {
        uint8_t uc = static_cast<uint8_t>(input[i]);
        uint8_t ge = static_cast<uint8_t>(((uint8_t)(uc - (uint8_t)'5') >> 7) ^ 1u);
        uint8_t mask = static_cast<uint8_t>(0u - ge);
        uint8_t dec = static_cast<uint8_t>(uc + static_cast<uint8_t>(~0u));
        uint8_t inc = static_cast<uint8_t>((uc ^ 1u) + static_cast<uint8_t>((uc & 1u) << 1));
        uint8_t res = static_cast<uint8_t>((dec & mask) | (inc & static_cast<uint8_t>(~mask)));
        input[i] = static_cast<char>(res);
    }

    // --- dummy check modify var2 using branchless / MBA patterns (even: +1, odd: -1) ---
    for (size_t i = 0; i < o0; ++i) {
        uint8_t v = static_cast<uint8_t>(var2[i]);
        uint8_t even = static_cast<uint8_t>(((uint8_t)i & 1u) ^ 1u);
        uint8_t m = static_cast<uint8_t>(0u - even);
        uint8_t dec = static_cast<uint8_t>(v + static_cast<uint8_t>(~0u));
        uint8_t inc = static_cast<uint8_t>((v ^ 1u) + static_cast<uint8_t>((v & 1u) << 1));
        uint8_t out = static_cast<uint8_t>((inc & m) | (dec & static_cast<uint8_t>(~m)));
        var2[i] = static_cast<char>(out);
    }

    // --- dummy checks (MBA-ish guarded loads) ---
    auto load_or_one = [&](size_t idx) -> int {
        uint8_t in_bounds = static_cast<uint8_t>(idx < o0);
        uint8_t mask = static_cast<uint8_t>(0u - in_bounds);
        uint8_t val = static_cast<uint8_t>(var2[idx]);
        return static_cast<int>((val & mask) | (1 & static_cast<uint8_t>(~mask)));
    };

    auto load_or_zero = [&](size_t idx) -> int {
        uint8_t in_bounds = static_cast<uint8_t>(idx < o0);
        uint8_t mask = static_cast<uint8_t>(0u - in_bounds);
        uint8_t val = static_cast<uint8_t>(var2[idx]);
        return static_cast<int>((val & mask) | (0 & static_cast<uint8_t>(~mask)));
    };

    int a = load_or_one(1);
    int b = load_or_one(3);
    int c = load_or_one(6);
    int prod = a * b;
    prod = prod * c;
    int s1 = load_or_zero(5);
    int s2 = load_or_zero(4);
    int s3 = load_or_zero(3);
    int sum = (s1 & 0xFFFF) + (s2 & 0xFFFF) + (s3 & 0xFFFF);
    if (prod == 100 && sum == 21) {
        volatile int sink = prod ^ sum; (void)sink;
    }
}


// Verify the .flagchk section at runtime and die if mismatch

static uint32_t crc32_region_ignore_int3(const uint8_t* buf, size_t len) {
    crc32_init();
    uint32_t c = 0xFFFFFFFFu;
    for (size_t i = 0; i < len; ++i) {
        uint8_t b = buf[i];
        if (b == 0xCC) continue;               // ignore software breakpoints inserted by gdb
        c = crc32_table[(c ^ b) & 0xFFu] ^ (c >> 8);
    }
    return c ^ 0xFFFFFFFFu;
}

static void verify_flagchk_allow_int3() {
    const char* start = __start_flagchk;
    const char* stop  = __stop_flagchk;
    size_t len = (size_t)(stop - start);
    if (len == 0) crash_on_tamper();
    uint32_t actual = crc32_region_ignore_int3(reinterpret_cast<const uint8_t*>(start), len);
    if (actual != EXPECTED_FLAGCHK_CRC) crash_on_tamper();
}

static void verify_flagchk_once_or_die() {
    const char* start = __start_flagchk;
    const char* stop  = __stop_flagchk;
    size_t len = (size_t)(stop - start);
    if (len == 0) {
        // nothing to check -> be conservative and abort
        crash_on_tamper();
    }
    uint32_t actual = crc32(reinterpret_cast<const uint8_t*>(start), len);
    if (actual != EXPECTED_FLAGCHK_CRC) {
        crash_on_tamper();
    }
}

// --- IMPORTANT CHANGES: noinline, used, section(".flagchk") and a memory barrier to prevent optimization ---
extern "C" __attribute__((noinline, used, section(".flagchk")))
void protected_tamper_assign(int userHash, int expectedHash, int y, volatile int* tamperCheck, void* expected_ret) {
    asm volatile("" ::: "memory");
    void* caller_ret = __builtin_return_address(0);
    if (caller_ret != expected_ret) crash_on_tamper();
    if (userHash == expectedHash) {
        *tamperCheck = y;
    }
}

// ---------------------- path1 now calls verify + protected function ----------------------
void path1() {
    char correctSequence[o0 + 1] = {0};
    char userSequence[o0 + 1] = {0};
    int userInput = -1;
    int userSequenceIndex = 0;
    int y = 425319839;
    std::string userSequenceStr = "";

    generateSequence(correctSequence);

    std::cout << "Welcome to the sequence challenge! Enter a sequence of 10 numbers (1-9):" << std::endl;
    xor_encrypt_globals(correctSequence, o0);

    while (userSequenceIndex < o0) {
        std::cout << "Enter your option (1-9): ";
        std::cin >> userInput;

        if (userInput < 1 || userInput > 9) {
            std::cout << "Ye kya kar raha h pawde." << std::endl;
            continue;
        }

        userSequenceStr += std::to_string(userInput);
        printMessage(userInput);
        userSequenceIndex++;
    }

    strncpy(userSequence, userSequenceStr.c_str(), o0);

    transformInput(userSequence);

    int userHash = std::hash<std::string>{}(std::string(userSequence, o0));
    int expectedHash = std::hash<std::string>{}(std::string(correctSequence, o0));

    volatile int tamperCheck = 0;

if (userHash == expectedHash) {
        tamperCheck = y;
    }


    if (tamperCheck != y) {
        std::cout << "Hoshiyari kar rya ae pawde" << std::endl;
        *((volatile int*)nullptr) = 0;  // Crash the program
    } else {
        xor_decrypt_globals(userSequence, o0);
        printFlag(userHash, expectedHash);
        getDaString2();
        std::cout << "\nSamajhdar ho gya hhh" << std::endl;
    }
}

// path2 unchanged (won't call verifier)
void path2() {
    path2_explored();
}

// rest unchanged
char rot13_char(char c) {
    if ('a' <= c && c <= 'z') return 'a' + (c - 'a' + 13) % 26;
    if ('A' <= c && c <= 'Z') return 'A' + (c - 'A' + 13) % 26;
    return c;
}

std::string apply_rot13_n_times(std::string input, int n) {
    for (int i = 0; i < n; ++i) {
        for (char &c : input) {
            c = rot13_char(c);
        }
    }
    return input;
}

std::vector<uint8_t> hex_string_to_bytes(const std::string& hex) {
    std::vector<uint8_t> bytes;
    std::string cleaned = hex.substr(2); // Remove "0x"
    for (size_t i = 0; i < cleaned.length(); i += 2) {
        std::string byteString = cleaned.substr(i, 2);
        uint8_t byte = static_cast<uint8_t>(std::stoul(byteString, nullptr, 16));
        bytes.push_back(byte);
    }
    return bytes;
}

std::vector<uint8_t> xor_with_input(const std::vector<uint8_t>& data, const std::string& key) {
    std::vector<uint8_t> result;
    for (size_t i = 0; i < data.size(); ++i) {
        result.push_back(data[i] ^ key[i % key.length()]);
    }
    return result;
}

void path3() {
    const std::string expected = "Paure";
    std::string user_input;
    std::cout << "Enter the key: ";
    std::cin >> user_input;

    std::string transformed = apply_rot13_n_times(user_input, 5);

    std::string encMSG = "0x300f0915522a0f0c125e631a190103631b0d451922090c45163207050102631a0e03102654474a1b2a07460e1324080f0b036d01091c5d2a030e0a067c065515312a5a015c3b30240726";
    if (transformed == expected) {
        std::cout << "Correct! .\n";
        std::cout << "Correct! decrypting data...\n";

        auto data_bytes = hex_string_to_bytes(encMSG);
        auto result = xor_with_input(data_bytes, user_input);

        std::cout << "XOR Result (ASCII): ";
        for (uint8_t b : result) {
            std::cout << (isprint(b) ? static_cast<char>(b) : '.');
        }
        std::cout << "\n";

    } else {
        std::cout << "Wrong key. Try again.\n";
    }
}

int main() {
    std::vector<std::function<void()>> paths = { path1, path2, path3 };

    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(paths.begin(), paths.end(), g);
    std::cout << "Welcome to Pawde's maze\n";
    std::cout << "2/3 paths shall get you the flag\n\n";
    std::cout << "Choose a path:\n";
    std::cout << "1. Path A\n2. Path B\n3. Path C\n";
    int choice;
    std::cin >> choice;

    if (choice < 1 || choice > 3) {
        std::cout << "Invalid choice.\n";
        return 1;
    }

    paths[choice - 1]();
    return 0;
}
