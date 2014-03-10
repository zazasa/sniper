#include <cstdio>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <string.h>
#include <unistd.h>




int              fSocket; // socket
struct sockaddr_in fReceiveSocketAddress;
int i;


int main()
{
    printf("Hello Wordl!\n");

    fSocket = socket(AF_INET, SOCK_DGRAM, 0);
    if(fSocket == -1){ printf("ERRORE 1\n"); };

    memset(&fReceiveSocketAddress, 0, sizeof(fReceiveSocketAddress));

    fReceiveSocketAddress.sin_addr.s_addr = inet_addr("127.0.0.1");
    fReceiveSocketAddress.sin_port = htons(8106);
    fReceiveSocketAddress.sin_family = AF_INET;
    
    int ret = bind(fSocket, (struct sockaddr*)&fReceiveSocketAddress, sizeof(fReceiveSocketAddress));
    if(ret != 0){ printf("ERRORE 2\n");  } 

    sleep(5);


    return 0;
}
