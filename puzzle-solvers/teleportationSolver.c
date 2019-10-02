#include <stdio.h>
#include <stdlib.h>

int ackermann(int m, int n, int k, int **memo) {
    if (memo[m][n] != -1) return memo[m][n];

    int result;
    if (m == 0) {
        result = (n+1)%32768;
    } else if (n == 0) {
        result = ackermann(m-1, k, k, memo);
    } else {
        int x = ackermann(m, n-1, k, memo);
        result = ackermann(m-1, x, k, memo);
    }

    // Memoizing the result
    memo[m][n] = result;
    return memo[m][n];
}

int main() {
    // Initializing memo matrix
    int **memo = malloc(sizeof(int *) * 5);
    for (int i = 0; i < 5; i++) {
        memo[i] = malloc(sizeof(int) * 32768);
    }

    // Testing all possible values for $7
    for (int k = 1; k < 32768; k++) {
        // Resetting memo matrix
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 32768; j++) {
                memo[i][j] = -1;
            }
        }

        // Running the Ackermann function
        int result = ackermann(4, 1, k, memo);
        printf("ackermann(4, 1, %d) = %d\n", k, result);

        // Found the valid value
        if (result == 6) {
            printf("Found it! Try $7 = %d.\n", k);
            break;
        }
    }

    for (int i = 0; i < 5; i++) free(memo[i]);
    free(memo);
}