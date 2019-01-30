#include <stdio.h>


struct hash_map{

    int size;

}


int hash(char *input, int mod){
    char *c;
    int sum;
    for (c=input;*c;c++){
        sum += 5*c + 1;
    }
    return sum % mod;
}

int main(){
    char *a = "abcde";
    char *b = "defgh";

    printf("%d\n",hash(a,12));
    printf("%d\n",hash(b,12));

}