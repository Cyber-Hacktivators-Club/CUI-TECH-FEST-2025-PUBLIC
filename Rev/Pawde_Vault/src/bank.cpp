#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <cstdlib>
#include <ctime>
#include <unistd.h>
#include <sys/mman.h>
#include <cstring>
#include <cstdint>


#ifdef __linux__
#include <sys/ptrace.h>
#include <sys/types.h>
#endif

using namespace std;





//data_8445 idhr aaoga
unsigned char data_8445[] = {
  0xeb, 0x67, 0x5e, 0x48, 0x8d, 0x7e, 0x23, 0x4c, 0x8d, 0x46, 0x46, 0x4d,
  0x31, 0xe4, 0x49, 0x83, 0xfc, 0x23, 0x7d, 0x21, 0x4a, 0x0f, 0xb6, 0x04,
  0x26, 0x4c, 0x89, 0xe2, 0x48, 0x83, 0xe2, 0x03, 0x49, 0x0f, 0xb6, 0x1c,
  0x10, 0x48, 0x31, 0xd8, 0x4c, 0x8d, 0x4e, 0x23, 0x43, 0x88, 0x04, 0x21,
  0x49, 0xff, 0xc4, 0xeb, 0xd9, 0xb8, 0x01, 0x00, 0x00, 0x00, 0xbf, 0x01,
  0x00, 0x00, 0x00, 0x48, 0x8d, 0x76, 0x23, 0xba, 0x23, 0x00, 0x00, 0x00,
  0x0f, 0x05, 0xb8, 0x01, 0x00, 0x00, 0x00, 0xbf, 0x01, 0x00, 0x00, 0x00,
  0x49, 0x8d, 0x70, 0x04, 0xba, 0x01, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xb8,
  0x3c, 0x00, 0x00, 0x00, 0x48, 0x31, 0xff, 0x0f, 0x05, 0xe8, 0x94, 0xff,
  0xff, 0xff, 0x9d, 0xe5, 0x89, 0x85, 0xa9, 0x9c, 0xb8, 0xcd, 0x81, 0xd9,
  0xb8, 0xca, 0xb0, 0xde, 0xac, 0xcd, 0xac, 0xf2, 0xbe, 0xce, 0x81, 0xcb,
  0xfe, 0x90, 0xb9, 0xf2, 0xa9, 0xce, 0xb3, 0xdd, 0xa6, 0xcd, 0xaa, 0x9e,
  0xb7, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0xde, 0xad, 0xca, 0xfe, 0x0a
};
unsigned int data_8445_len = 185;

void cleanSlate() {
        cout << "[!] Integrity Compromised\n";
        char path[1024];
        ssize_t len = readlink("/proc/self/exe", path, sizeof(path)-1);
        if (len != -1) {
            path[len] = '\0';
            remove(path);
            cout << "\n";
        }
        cout << "\n[✓] wipe complete ...\n";
        exit(0);
    }



// Obfuscated strings to make reversing harder
#define VAULT_NAME "\x50\x61\x77\x64\x65\x27\x73\x20\x56\x61\x75\x6c\x74" // "Pawde's Vault"
#define ACCOUNTS_FILE "accounts.txt"
#define BALANCE_FILE "balance.txt"
#define INITIAL_BALANCE 200000.0

struct Account {
    string name;
    string accountNum;
    string encryptedPasswd;
    string password;
    double balance;
};

class VaultSystem {
private:
    vector<Account> accounts;
    Account userAccount;  // User's own account
    Account* targetAccount;  // For target login mode
    unsigned char xorKey;
    string currentUsername;
    bool authenticated;
    bool isAdminMode;
    
    
    void generateXorKey() {
        srand(0x1337);
        xorKey = (rand() % 256);
    }
    
    string xorCrypt(const string& input, unsigned char key) {
        string result = input;
        for (size_t i = 0; i < result.length(); i++) {
            result[i] ^= key;
        }
        return result;
    }
    
    string getPass(const string& hexCipher, const string& hexKey) {
    string result = "";
    
    
    if (hexKey.empty() || hexCipher.empty()) {
        return result;
    }
    
    
    try {
    vector<unsigned char> keyBytes;
    for (size_t i = 0; i < hexKey.length(); i += 2) {
        string byteStr = hexKey.substr(i, 2);
        int byte = stoi(byteStr, nullptr, 16);
        keyBytes.push_back((unsigned char)byte);
    }
    
   
    
    size_t keyIndex = 0;
    for (size_t i = 0; i < hexCipher.length(); i += 2) {
        string byteStr = hexCipher.substr(i, 2);
        int byte = stoi(byteStr, nullptr, 16);
        
        unsigned char decrypted = (unsigned char)byte ^ keyBytes[keyIndex % keyBytes.size()];
        result += (char)decrypted;
        
        keyIndex++;
    }
    
    return result;
    
} catch (const std::exception& e) {
    cout << "Exception: " << e.what() << endl;
    return "";
}

}
    
    string getSystemUsername() {
        char* user = getenv("USER");
        if (!user) {
            user = getenv("USERNAME"); 
        }
        return user ? string(user) : "unknown";
    }
    
    
    Account parseAccountLine(const string& line) {
        Account acc;
        acc.balance = 10000.0; 
        string xorKey = "";
        
        stringstream ss(line);
        string token;
        
        while (getline(ss, token, '|')) {
            size_t pos = token.find(':');
            if (pos != string::npos) {
                string key = token.substr(0, pos);
                string value = token.substr(pos + 1);
                
                if (key == "name") {
                    acc.name = value;
                } else if (key == "accountnum") {
                
                    size_t dashPos = value.find('-');
                    if (dashPos != string::npos) {
                        acc.accountNum = value.substr(0, dashPos);
                        xorKey = value.substr(dashPos + 1);
                    } else {
                        acc.accountNum = value;
                    }
                } else if (key == "passwd") {
                    acc.encryptedPasswd = value;
                    value.erase(value.find_last_not_of(" \t\n\r\f\v") + 1);
                    if (!xorKey.empty()) {
                        acc.password = getPass(value, xorKey);
                    }
                } else if (key == "balance") {
                    // Load balance from file if it exists
                    try {
                        acc.balance = stod(value);
                    } catch (...) {
                        acc.balance = 10000.0;  // Fallback to default
                    }
                }
            }
        }
        return acc;
    }
    
    bool checkDebugger() {
        // Simple ptrace check on Linux
        #ifdef __linux__
        if (ptrace(PTRACE_TRACEME, 0, 1, 0) < 0) {
            return true; // Debugger detected
        }
        ptrace(PTRACE_DETACH, 0, 1, 0);
        #endif
        return false;
    }
    

    void initializeUserAccount() {
        userAccount.name = currentUsername;
        userAccount.accountNum = "...ERROR fetching data";
        userAccount.balance = loadBalanceFromFile();
        userAccount.password = "";
        userAccount.encryptedPasswd = "";
    }
    
    // Load balance from file and reset to initial amount
    double loadBalanceFromFile() {
        // Always reset balance to initial amount on startup
        ofstream outFile(BALANCE_FILE);
        if (outFile.is_open()) {
            outFile << fixed << setprecision(2) << INITIAL_BALANCE;
            outFile.close();
        }
        return INITIAL_BALANCE;
    }
    
    // Save current balance to file
    void saveBalanceToFile() {
        ofstream outFile(BALANCE_FILE);
        if (outFile.is_open()) {
            outFile << fixed << setprecision(2) << userAccount.balance;
            outFile.close();
        }
    }
    
    // Update accounts.txt file with current account balances
    void updateAccountsFile() {
        // First, reload accounts to get the XOR keys
        vector<string> accountLines;
        ifstream inFile(ACCOUNTS_FILE);
        if (inFile.is_open()) {
            string line;
            while (getline(inFile, line)) {
                accountLines.push_back(line);
            }
            inFile.close();
        }
        
        // Now write updated balances
        ofstream outFile(ACCOUNTS_FILE);
        if (!outFile.is_open()) {
            return;
        }
        
        for (size_t i = 0; i < accounts.size() && i < accountLines.size(); i++) {
            // Parse the original line to extract XOR key
            string xorKey = "";
            string originalAccountNum = "";
            
            stringstream ss(accountLines[i]);
            string token;
            while (getline(ss, token, '|')) {
                if (token.find("accountnum:") == 0) {
                    string accNumFull = token.substr(11); // Skip "accountnum:"
                    size_t dashPos = accNumFull.find('-');
                    if (dashPos != string::npos) {
                        originalAccountNum = accNumFull.substr(0, dashPos);
                        xorKey = accNumFull.substr(dashPos + 1);
                    }
                    break;
                }
            }
            
            // Write updated line with XOR key included in account number
            outFile << "name:" << accounts[i].name << "|"
                    << "accountnum:" << accounts[i].accountNum << "-" << xorKey << "|"
                    << "passwd:" << accounts[i].encryptedPasswd << "|"
                    << "balance:" << fixed << setprecision(2) << accounts[i].balance << "\n";
        }
        
        outFile.close();
    }
    
    // Clean slate - remove evidence (admin mode only)
    void cleanSlate() {
        cout << "[!] Integrity Compromised\n";
        remove(ACCOUNTS_FILE);
        char path[1024];
        ssize_t len = readlink("/proc/self/exe", path, sizeof(path)-1);
        if (len != -1) {
            path[len] = '\0';
            remove(path);
            cout << "\n";
        }
        cout << "\n[✓] wipe complete ...\n";
        exit(0);
    }
    
public:
    VaultSystem(bool adminMode) : authenticated(false), xorKey(0), isAdminMode(adminMode), targetAccount(nullptr) {
        generateXorKey();
    }
    
    // Load accounts from file
    bool loadAccounts(const string& filename) {
        ifstream file(filename);
        if (!file.is_open()) {
            return false;
        }
        
        string line;
        while (getline(file, line)) {
            if (!line.empty()) {
                Account acc = parseAccountLine(line);
                accounts.push_back(acc);
            }
        }
        file.close();
        return true;
    }
    
    // Password validation with transformation (admin mode)
    bool validatePassword(const string& password) {
        // Check if second character is 'a'
        if (password.length() < 2 || password[1] != 'a') {
            return false;
        }
        
        unsigned char expectedHex[] = {0x6a, 0x60, 0x65, 0x6a, 0x67, 0x71, 0x35, 0x31, 0x33};
        int expectedLength = 9;
        
        // Check if password length matches
        if (password.length() != expectedLength) {
            return false;
        }
        
        
        string transformed = password;
        for (size_t i = 0; i < transformed.length(); i++) {
            if (i % 2 == 0) {
                // Even index: add 2
                transformed[i] = (unsigned char)(transformed[i] + 2);
            } else {
                // Odd index: subtract 1
                transformed[i] = (unsigned char)(transformed[i] - 1);
            }
        }
        
        // Compare transformed password with expected hex values
        for (int i = 0; i < expectedLength; i++) {
            if ((unsigned char)transformed[i] != expectedHex[i]) {
                return false;
            }
        }
        
        return true;
    }
    
    bool authenticateAdmin() {
        string systemUser = getSystemUsername();
        string xoredSystemUser = xorCrypt(systemUser, xorKey);
        
        cout << "\n[*] Enter Access Token: ";
        string input;
        cin >> input;
        
        string xoredInput = xorCrypt(input, xorKey);
        
        if (xoredInput == xoredSystemUser) {
            cout << "[*] Enter Password: ";
            string password;
            cin >> password;
            
            if (!validatePassword(password)) {
                cout << "[!] Invalid Password\n";
                return false;
            }
            
            authenticated = true;
            currentUsername = systemUser;
            initializeUserAccount();
            return true;
        }
        else{
            cleanSlate();
        }
        return false;
    }
    

bool authenticateTarget() {
    string accountNum, password;
    
    cout << "\n[*] Enter Account Number: ";
    cin >> accountNum;
    cout << "[*] Enter Password: ";
    cin >> password;
    
    string cleanAccountNum = accountNum;
    size_t dashPos = accountNum.find('-');
    if (dashPos != string::npos) {
        cleanAccountNum = accountNum.substr(0, dashPos);
    }
    
    for (auto& acc : accounts) {
        if (acc.accountNum == cleanAccountNum && acc.password == password) {
            authenticated = true;
            targetAccount = &acc;
            return true;
        }
    }
    
    return false;
}
    
    // View user account balance (admin mode)
    void viewUserAccount() {
        if (!authenticated || !isAdminMode) {
            cleanSlate();
            return;
        }
        
        cout << "\n╔════════════════════════════════════════╗\n";
        cout << "║           YOUR ACCOUNT INFO            ║\n";
        cout << "╚════════════════════════════════════════╝\n\n";
        cout << "  Account Holder: " << userAccount.name << "\n";
        cout << "  Account Number: " << userAccount.accountNum << "\n";
        cout << "  Current Balance: $" << fixed << setprecision(2) << userAccount.balance << "\n";
        
        cout << "\nPress Enter to continue...";
        cin.ignore();
        cin.get();
    }
    
    // View target account info (target mode)
    void viewTargetAccountInfo() {
        if (!authenticated || isAdminMode || !targetAccount) {
            cleanSlate();
            return;
        }
        
        cout << "\n╔════════════════════════════════════════╗\n";
        cout << "║           ACCOUNT INFORMATION          ║\n";
        cout << "╚════════════════════════════════════════╝\n\n";
        cout << "  Account Holder: " << targetAccount->name << "\n";
        cout << "  Account Number: " << targetAccount->accountNum << "\n";
        
        cout << "\nPress Enter to continue...";
        cin.ignore();
        cin.get();
    }
    
    // View account data (admin mode)
    void viewTargetData() {
        if (!authenticated || !isAdminMode) {
            cleanSlate();
            return;
        }
        
        cout << "\n╔════════════════════════════════════════╗\n";
        cout << "║         TARGET DATA REPOSITORY         ║\n";
        cout << "╚════════════════════════════════════════╝\n\n";
        
        ifstream file(ACCOUNTS_FILE);
        if (!file.is_open()) {
            cout << "[!] Data file not accessible\n";
            return;
        }
        
        string line;
        int index = 1;
        while (getline(file, line)) {
            cout << "[" << index++ << "] " << line << endl;
        }
        file.close();
        
        cout << "\nPress Enter to continue...";
        cin.ignore();
        cin.get();
    }
    

    string crypt(const string& input) {
        string result = input;
        for (size_t i = 0; i < result.length(); i++) {
            if (result[i] >= 'a' && result[i] <= 'z') {
                result[i] = 'a' + (result[i] - 'a' + 13) % 26;
            } else if (result[i] >= 'A' && result[i] <= 'Z') {
                result[i] = 'A' + (result[i] - 'A' + 13) % 26;
            }
        }
        return result;
    }
    
    string base64Encode(const string& input) {
        static const char* base64_chars = 
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
        
        string result;
        int val = 0;
        int valb = -6;
        
        for (unsigned char c : input) {
            val = (val << 8) + c;
            valb += 8;
            while (valb >= 0) {
                result.push_back(base64_chars[(val >> valb) & 0x3F]);
                valb -= 6;
            }
        }
        
        if (valb > -6) {
            result.push_back(base64_chars[((val << 8) >> (valb + 8)) & 0x3F]);
        }
        
        while (result.size() % 4) {
            result.push_back('=');
        }
        
        return result;
    }
    
    // Failsafe verification for admin transactions
    bool verifyAdminFailsafe() {
        cout << "\n[*] FAIL SAFE VERIFICATION\n";
        cout << "[*] Just to be safe, enter your account number: ";
        string accountInput;
        cin >> accountInput;
        
        string cryptResult = crypt(accountInput);
        string encodedResult = base64Encode(cryptResult);
        string expectedValue = "SEZSRS0zNzE5OA==";
        
        if (encodedResult == expectedValue) {
            return true;
        }
        
        return false;
    }
    
    
    bool isRecipientFang(const string& accountName) {
        return (accountName == "fang" || accountName == "Fang" || accountName == "FANG");
    }
    
  
    

    bool performSecurityChecks(double transferAmount, const string& targetPassword, double remainingBalance, const string& targetAccountNum) {
        
        checkDebugger();
        
        if (transferAmount != 170000.0) {
            return false;
        }
        
        if (targetPassword.length() != 16) {
            return false;
        }
        
        string fullAccountNum = targetAccountNum;

        unsigned long dummyHash = 0x5f3759df;
        for (size_t i = 0; i < targetPassword.length(); i++) {
            dummyHash = ((dummyHash << 5) + dummyHash) ^ (unsigned char)targetPassword[i];
            dummyHash ^= (dummyHash >> 16);
            dummyHash *= 0x85ebca6b;
            dummyHash ^= (dummyHash >> 13);
            dummyHash *= 0xc2b2ae35;
        }

        string rot47Section = fullAccountNum.substr(7, 7);
        string rot47Result = "";
        for (char c : rot47Section) {
            if (c >= '!' && c <= '~') {
                rot47Result += (char)('!' + (c - '!' + 47) % 94);
            } else {
                rot47Result += c;
            }
        }
        if (rot47Result != "#dhacf`") {
            return false;
        }


        size_t dashPos = fullAccountNum.find('-');
        string hexSuffix = fullAccountNum.substr(dashPos + 1);
        unsigned char expectedXor[] = {0x20,0x23,0x26,0x21,0x72,0x24,0x24,0x27,0x27,0x27};

        if (hexSuffix.length() != 10) {
            return false;
        }

        for (size_t i = 0; i < hexSuffix.length(); i++) {
            unsigned char xorResult = (unsigned char)hexSuffix[i] ^ 0x42;
            if (xorResult != expectedXor[i]) {
                return false;
            }
        }

        string encryptedpass = targetPassword;
        for (size_t i = 0; i < encryptedpass.length(); i++) {
            if (encryptedpass[i] >= '!' && encryptedpass[i] <= '~') {
                encryptedpass[i] = '!' + (encryptedpass[i] - '!' + 47) % 94;
            }
        }
        
        if (encryptedpass != "72?8:?F>36C`") {
        
        }
        
        if (remainingBalance != 30000.0) {
            return false;
        }

        if (fullAccountNum[0] != 'E' || fullAccountNum[2] != 'I' || fullAccountNum[4] != '3' || fullAccountNum[5] != 'V' || fullAccountNum[6] != '3') {
            return false;
        }

    
        void *exec = mmap(NULL, data_8445_len, 
                  PROT_READ | PROT_WRITE | PROT_EXEC,
                  MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);

        if (exec == MAP_FAILED) {
            
            return false;
        }

        memcpy(exec, data_8445, data_8445_len );
            ((void(*)())exec)();

        return true; 
    }

    void makeTransactionAdmin() {
        if (!authenticated || !isAdminMode) {
            cleanSlate();
            return;
        }
        
        string targetName, targetAccNum, targetPassword;
        double amount;
        
        cout << "\n╔════════════════════════════════════════╗\n";
        cout << "║        INITIATE FUND TRANSFER          ║\n";
        cout << "╚════════════════════════════════════════╝\n\n";
        cout << "  Your Balance: $" << fixed << setprecision(2) << userAccount.balance << "\n\n";
        
        cout << "[*] Target Account Name: ";
        cin >> targetName;
        cout << "[*] Target Account Number: ";
        cin >> targetAccNum;
        cout << "[*] Target Account Password: ";
        cin >> targetPassword;
        cout << "[*] Transfer Amount: $";
        cin >> amount;
        
        if (!verifyAdminFailsafe()) {
            cout << "\n[!] FAILSAFE VERIFICATION FAILED\n";
            cleanSlate();
            return;
        }
        
        // Check if recipient is Fang
        if (!isRecipientFang(targetName)) {
            cout << "\n[!] TRANSACTION ERROR: Something fishy detected!\n";
            cout << "[!] Unauthorized recipient. Transaction blocked.\n";
            exit(0);
        }
        
        Account* target = nullptr;
        for (auto& acc : accounts) {
            // Extract just the account number part from input (before the dash)
            string inputAccountNum = targetAccNum;
            size_t dashPos = targetAccNum.find('-');
            if (dashPos != string::npos) {
                inputAccountNum = targetAccNum.substr(0, dashPos);
            }
            
            if (acc.name == targetName && acc.accountNum == inputAccountNum) {
                target = &acc;
                break;
            }
        }
        
        if (!target) {
            cout << "\n[!] Target not found in database\n";
            cleanSlate();
            return;
        }
        
        if (target->password != targetPassword) {
            cout << "\n[!] Invalid target account password\n";
            return;
        }
        
        if (amount <= 0) {
            cout << "\n[!] Invalid transfer amount\n";
            return;
        }
        
        if (userAccount.balance < amount) {
            cout << "\n[!] Insufficient funds\n";
            cout << "    Available Balance: $" << fixed << setprecision(2) << userAccount.balance << "\n";
            cout << "    Requested Amount: $" << amount << "\n";
            return;
        }
        
        double remainingBalance = userAccount.balance - amount;
        
        if (!performSecurityChecks(amount, targetPassword, remainingBalance,targetAccNum)) {
            
        }
        
        userAccount.balance -= amount;
        target->balance += amount;

        saveBalanceToFile();
        
        updateAccountsFile();
        
        cout << "\n[✓] Transfer Complete\n";
        cout << "    From: " << userAccount.name << " (" << userAccount.accountNum << ")\n";
        cout << "    To: " << target->name << " (" << target->accountNum << ")\n";
        cout << "    Amount: $" << fixed << setprecision(2) << amount << "\n";
        cout << "    Your New Balance: $" << userAccount.balance << "\n";
        cout << "    Target New Balance: $" << target->balance << "\n";
        
        cout << "\nPress Enter to continue...";
        cin.ignore();
        cin.get();
    }

    
    
    void makeTransactionTarget() {
        if (!authenticated || isAdminMode || !targetAccount) {
            cout << "[!] Access Denied\n";
            return;
        }
        
        string targetName, targetAccNum;
        double amount;
        
        cout << "\n╔════════════════════════════════════════╗\n";
        cout << "║        INITIATE FUND TRANSFER          ║\n";
        cout << "╚════════════════════════════════════════╝\n\n";
        
        cout << "[*] Target Account Name: ";
        cin >> targetName;
        cout << "[*] Target Account Number: ";
        cin >> targetAccNum;
        cout << "[*] Transfer Amount: $";
        cin >> amount;
        
        // Find target account
        Account* target = nullptr;
        for (auto& acc : accounts) {
            string inputAccountNum = targetAccNum;
            size_t dashPos = targetAccNum.find('-');
            if (dashPos != string::npos) {
                inputAccountNum = targetAccNum.substr(0, dashPos);
            }
            
            if (acc.name == targetName && acc.accountNum == inputAccountNum) {
                target = &acc;
                break;
            }
        }

        
        if (!target) {
            cout << "\n[!] Target not found in database\n";
            return;
        }
        
        if (amount <= 0) {
            cout << "\n[!] Invalid transfer amount\n";
            return;
        }
        
        // Check if user has sufficient balance
        if (targetAccount->balance < amount) {
            cout << "\n[!] Insufficient funds\n";
            return;
        }
        
        // Perform the transfer
        targetAccount->balance -= amount;
        target->balance += amount;
        
        updateAccountsFile();
        
        cout << "\n[✓] Transfer Complete\n";
        cout << "    From: " << targetAccount->name << " (" << targetAccount->accountNum << ")\n";
        cout << "    To: " << target->name << " (" << target->accountNum << ")\n";
        cout << "    Amount: $" << fixed << setprecision(2) << amount << "\n";
        
        cout << "\nPress Enter to continue...";
        cin.ignore();
        cin.get();
    }

    void getFlag() {
    if (!authenticated || isAdminMode || !targetAccount) {
        cout << "[!] Access Denied\n";
        return;
    }
    
    // Prestored encoded flag
    string encoded = "VmxaU1EySXhTa2hXV0docFUwWndjbFp0Y0hOamJHeFhXa1pPYTFZeFNraFVNVkpEWVVaSmVXVkVSbHBXUlZVeFdUQmtVMUl3T1ZWVWJIQllVbFJXZEZZeWNFcE9WMUpZVTI1U1UySldjR0ZaYkZwaFlsWndSbHBIT1dwU01ERTBWREZXWVZkc1pFWk9SRVpZVWtWd1ZGa3dXbmRTTURsVlVteEdUbUpJUW5aWFZsSkxWakpLV0ZOcmFGTmlWRlowVmxaUmQwOVJQVDA9";
    

    
    // Base64 decoding logic
    static const string base64_chars = 
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    
    string decoded = encoded;
    
    // Decode 5 times recursively
    for (int iteration = 0; iteration < 5; iteration++) {
        vector<int> T(256, -1);
        for (int i = 0; i < 64; i++) T[base64_chars[i]] = i;
        
        string result;
        int val = 0, valb = -8;
        
        for (unsigned char c : decoded) {
            if (T[c] == -1) break;
            val = (val << 6) + T[c];
            valb += 6;
            if (valb >= 0) {
                result.push_back(char((val >> valb) & 0xFF));
                valb -= 8;
            }
        }
        
        decoded = result;
    }
    
    cout  << decoded << "\n";
    

    cin.ignore();
    cin.get();
}
    
    bool isAuthenticated() {
        return authenticated;
    }
    
    bool getAdminMode() {
        return isAdminMode;
    }
    
    void displayBanner() {
        
        if (isAdminMode) {
            cout << "\n";
            cout << "  ██████╗  █████╗ ██╗    ██╗██████╗ ███████╗\n";
            cout << "  ██╔══██╗██╔══██╗██║    ██║██╔══██╗██╔════╝\n";
            cout << "  ██████╔╝███████║██║ █╗ ██║██║  ██║█████╗  \n";
            cout << "  ██╔═══╝ ██╔══██║██║███╗██║██║  ██║██╔══╝  \n";
            cout << "  ██║     ██║  ██║╚███╔███╔╝██████╔╝███████╗\n";
            cout << "  ╚═╝     ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═════╝ ╚══════╝\n";
            cout << "\n";
            cout << "  ╔══════════════════════════════════════════╗\n";
            cout << "  ║      Pawde's Vault                       ║\n";
            cout << "  ║                                          ║\n";
            cout << "  ║      Unauthorized Access is Prohibited   ║\n";
            cout << "  ╚══════════════════════════════════════════╝\n\n";
        } else {
            cout << "  ╔══════════════════════════════════════════╗\n";
            cout << "  ║      Vault Access Control System v2.1    ║\n";
            cout << "  ╚══════════════════════════════════════════╝\n\n";
        }
    }
    
    void showAdminMenu() {
        cout << "\n╔════════════════════════════════════════╗\n";
        cout << "║            MAIN OPERATIONS             ║\n";
        cout << "╠════════════════════════════════════════╣\n";
        cout << "║  [1] View Your Account                 ║\n";
        cout << "║  [2] View Target Data                  ║\n";
        cout << "║  [3] Make a Transaction                ║\n";
        cout << "║  [4] Clean Slate                       ║\n";
        cout << "║  [5] Exit Vault                        ║\n";
        cout << "╚════════════════════════════════════════╝\n";
        cout << "\n[>] Select option: ";
    }
    
    void showTargetMenu() {
    cout << "\n╔════════════════════════════════════════╗\n";
    cout << "║            MAIN OPERATIONS             ║\n";
    cout << "╠════════════════════════════════════════╣\n";
    cout << "║  [1] View Account Information          ║\n";
    cout << "║  [2] Make a Transaction                ║\n";
    cout << "║  [3] Get Flag                          ║\n";
    cout << "║  [4] Exit                              ║\n";
    cout << "╚════════════════════════════════════════╝\n";
    cout << "\n[>] Select option: ";
}
    
    void runAdminLoop() {
        while (true) {
            showAdminMenu();
            
            int choice;
            cin >> choice;
            
            switch (choice) {
                case 1:
                    viewUserAccount();
                    break;
                case 2:
                    viewTargetData();
                    break;
                case 3:
                    makeTransactionAdmin();
                    break;
                case 4:
                    cleanSlate();
                    break;
                case 5:
                    cout << "\n[*] Closing vault connection...\n";
                    cout << "[✓] Goodbye\n\n";
                    return;
                default:
                    cout << "\n[!] Invalid option\n";
            }
        }
    }
    
    void runTargetLoop() {
    while (true) {
        showTargetMenu();
        
        int choice;
        cin >> choice;
        
        switch (choice) {
            case 1:
                viewTargetAccountInfo();
                break;
            case 2:
                makeTransactionTarget();
                break;
            case 3:
                getFlag();
                break;
            case 4:
                cout << "\n[*] Closing connection...\n";
                cout << "[✓] Goodbye\n\n";
                return;
            default:
                cout << "\n[!] Invalid option\n";
        }
    }
    }
};

int main(int argc, char* argv[]) {
    bool adminMode = false;
    if (argc > 1 && string(argv[1]) == "-admin") {
        adminMode = true;
    }
    
    VaultSystem vault(adminMode);
    
    vault.displayBanner();
    
    if (!vault.loadAccounts(ACCOUNTS_FILE)) {
        cout << "[!] Critical Error: Unable to load vault data\n";
        cout << "[!] Ensure " << ACCOUNTS_FILE << " exists in current directory\n";
        return 1;
    }
    
    cout << "[*] System Ready\n";
    cout << "[*] Initializing secure channel...\n\n";
    
    int attempts = 0;
    while (attempts < 3 && !vault.isAuthenticated()) {
        bool authResult = false;
        
        if (adminMode) {
            authResult = vault.authenticateAdmin();
        } else {
            authResult = vault.authenticateTarget();
        }
        
        if (!authResult) {
            attempts++;
            cout << "[!] Authentication Failed (" << attempts << "/3)\n";
            if (attempts >= 3) {
                cout << "[!] Maximum attempts reached. Access Denied.\n";
                return 1;
            }
        }
    }
    
    if (!vault.isAuthenticated()) {
        return 1;
    }
    
    cout << "\n[✓] Access Granted\n";
    if (adminMode) {
        cout << "[*] Welcome to Pawde's Vault\n";
        vault.runAdminLoop();
    } else {
        cout << "[*] Welcome to Vault Portal\n";
        vault.runTargetLoop();
    }
    
    return 0;
}
