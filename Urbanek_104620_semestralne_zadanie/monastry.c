#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

#define MAX_LENGTH 10000
#define MAX(a,b) ((a)>(b)?(a):(b))

void remove_stars(char* string) {
    /*Removing stars from given string
    Args:gccc -
        char* string -- entered string
    */
    int i, j;
    int len = strlen(string);

    //Iterate through string and rewrites it without stars
    for (i = 0, j = 0; i < len; i++) {
        if (string[i] != '*') {
            string[j++] = string[i];
        }
    }
    string[j] = '\0';
}

void lcs(char* sourceA, char* sourceB, int m, int n) {
    /*Removing stars from given string
    Args:
        char* sourceA -- entered first string input
        char* sourceB -- entered second string input
        int m -- length of soruceA
        int n -- length of sourceB
    */
    int* dp = (int*)calloc((m + 1) * (n + 1), sizeof(int));
    int i, j;

    // Calculate dp matrix using wavefront parallelism
    for (int sum = 0; sum <= m + n; sum++) {
        #pragma omp parallel for
        for (i = 0; i <= m; i++) {
            j = sum - i;
            if (j >= 0 && j <= n) {
                if (i == 0 || j == 0) {
                    dp[i * (n + 1) + j] = 0;
                }
                else if (sourceA[i - 1] == sourceB[j - 1]) {
                    dp[i * (n + 1) + j] = dp[(i - 1) * (n + 1) + (j - 1)] + 1;
                }
                else {
                    dp[i * (n + 1) + j] = MAX(dp[(i - 1) * (n + 1) + j], dp[i * (n + 1) + (j - 1)]);
                }
            }
        }
    }

    // Construct the longest common subsequence
    int index = dp[m * (n + 1) + n];
    char* lcs = (char*)malloc((index + 1) * sizeof(char));
    lcs[index] = '\0'; // Set the terminating character

    i = m, j = n;
    while (i > 0 && j > 0) {
        if (sourceA[i - 1] == sourceB[j - 1]) {
            lcs[--index] = sourceA[i - 1];
            i--; j--;
        }
        else if (dp[(i - 1) * (n + 1) + j] > dp[i * (n + 1) + (j - 1)]) {
            i--;
        }
        else {
            j--;
        }
    }

    printf("Output: %s\n", lcs);

    free(lcs);
    free(dp);
}

int main() {
    omp_set_num_threads(8);
    double start, end;
    
    char str1[MAX_LENGTH], str2[MAX_LENGTH];
    printf("Enter the first string: ");
    scanf("%s", str1);
    printf("Enter the second string: ");
    scanf("%s", str2);

    remove_stars(str1);
    remove_stars(str2);

    int m = strlen(str1);
    int n = strlen(str2);

    printf("LCS of %s and %s is: \n", str1, str2);
    start = omp_get_wtime();
    lcs(str1, str2, m, n);
    end = omp_get_wtime();

    printf("Time = %.6f\n", end - start);

    printf("Max threads = %d\n", omp_get_max_threads());
    return 0;
}