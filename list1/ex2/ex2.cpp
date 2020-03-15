#include <cstdio>
#include <iostream>
#include <cstdlib>
#include <bitset>

const int MAX_CAPACITY = 100;
int randomGenerated[MAX_CAPACITY];

int predict(int index)
{
    randomGenerated[index] =
        randomGenerated[index - 31] + randomGenerated[index - 3] % 2147483648;
    return randomGenerated[index];
}

int main()
{
    srand(1);
    int expected, predicted;
    float successRatio;
    unsigned int correctCounter = 0;
    int index;

    // prepare table to enable use of predict
    for (int index = 0; index < 30; index++)
    {
        randomGenerated[index] = rand();
    }

    // statistic test
    for (; index < MAX_CAPACITY; index++)
    {
        expected = rand();
        predicted = predict(index);

        std::bitset<32> bits(expected ^ ~predicted);
        correctCounter += bits.count();

        successRatio = (float)correctCounter / (float)((index + 1) * 32);
        // if success ratio is about 50% then generator is gclibs random() function
        std::cout << successRatio << std::endl;

        if (predicted != expected)
        {
            randomGenerated[index] = expected % 2147483648;
        }
    }
}