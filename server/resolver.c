#include "resolver.h"
#include <stdio.h>
#include <string.h>

// Check local DNS file
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

// Main resolver
int resdomain(const char *domain) {

    // Step 1: check local records
    if (localcheck(domain)) {
        return 1; // found locally
    }

    // Step 2: forward to external DNS
    printf("Forwarding to 8.8.8.8: %s\n", domain);

    // (Actual forwarding handled in full version)
    return 2; // external
}
