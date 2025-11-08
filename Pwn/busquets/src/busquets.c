//Description:
//Like Busquets on the pitch, this challenge keeps things simple - almost too simple. But just as he can pivot a match with one touch, a well-timed move here can completely shift the flow of execution. Stay calm, read the play, and find the moment where control quietly changes sides.

//gcc -fno-stack-protector -z execstack -no-pie -o busquets busquets.c 

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_ENTRIES 10
#define NAME_LEN 32
#define MSG_LEN 64

typedef struct data {
	char name[8]; 
 	char msg[64];
} data_t;

void menu() {
	puts("1. Add a player");
	puts("2. Add your opinion");
	puts("3. Leave this beautiful game");
}

int game() {
	char hateSpeech[8];
	data_t opinions[10];
	int total_entries = 0;
	int choice = -1;
	puts("Hello my fellow culer! I heard you hate Los Blancos as much as me, I allow you to write a player's name and express your opinion!");
	while (true) {
		menu();
		if (scanf("%d", &choice) != 1) exit(0);
		getchar();

		if (choice == 1) {
			choice = -1;	
			if (total_entries >= MAX_ENTRIES) { 
				puts("This is not bernabeu! You can't buy referees here!");
				continue;
			}

			puts("What's the player's name: ");
			fflush(stdin);
			fgets(opinions[total_entries].name, NAME_LEN, stdin);
			total_entries++;
			
		}

		else if (choice == 2) {
			choice = -1;
			puts("Which player would you like to send an opinion to? (write index)");
			if (scanf("%d", &choice) != 1) exit(0);
			getchar();

			if (choice >= total_entries) {
				puts("Take it easy, there's not such entry.");
				continue;
			}

			puts("What your opinion about the player?");
			fgets(opinions[choice].msg, MSG_LEN, stdin); 
		}
		else if (choice == 3) {
			choice = -1;
			puts("I hope you add fun playing the game! Repeat after me PUTA MADRID!!");
			fgets(hateSpeech, NAME_LEN, stdin); 
			hateSpeech[7] = '\0';
			break;
		}
		else {
			choice = -1;
			puts("Invalid option");
		}
	}
}

int main() {
	setvbuf(stdout, NULL, _IONBF, 0);  
	game();
	return 0;
}
