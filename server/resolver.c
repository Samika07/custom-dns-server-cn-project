#include "resolver.h"
#include <stdio.h>
#include <string.h>

int localcheck(const char *domain) {
    FILE *f = fopen("dns.txt", "r");
    if (!f) return 0;

    char d[100], ip[50];

    while (fscanf(f, "%s %s", d, ip) != EOF) {
        if (strcmp(d, domain) == 0) {
            printf("Local: %s -> %s\n", domain, ip);
            fclose(f);
            return 1;
        }
    }

    fclose(f);
    return 0;
}

int resdomain(const char *domain) {
    if (localcheck(domain))
        return 1;

    printf("Forwarding to 8.8.8.8: %s\n", domain);
    return 2;
}

int main() {
    char domain[100];

    printf("Enter domain: ");
    scanf("%s", domain);

    resdomain(domain);

    return 0;
}
