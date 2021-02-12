/* Try to find a suitable resistor combination because you don't have the correct one on hand and making a requisition 
    takes too long. It works. Far from pretty or usable.
*/
#include <iostream>
using namespace std;

const bool RCheck(const float R, const float desiredR, const float minR) {
    if (abs(R - desiredR) < desiredR) {
        if (minR == -1) {
            return true;
        }
        // minimize based on the error from the desired RTotal
        else if (abs(R - desiredR) < abs(minR - desiredR)) {
            return true;
        }
    }
    return false;
}

const bool powerCheck(const float P, const float maxPowerRating, const float minP) {
    // check if we are below the power rating of the resistors
    if (P < maxPowerRating) {
        // check if this is less than than the minP
        if (minP == -1) {
            return true;
        }
        else if (P < minP) {
            return true;
        }
    }
    return false;
}

int main() {
    float onHandR [] = {0, 1, 1.5, 4.7, 10, 47, 100, 220, 330, 470, 680}; // Ohm
    float desiredR = 120; // Ohm
    float circuitV = 5; // Volt
    float maxPowerRating = 0.25; // Watts

    // 2 resistors the hard way. I might make it smarter later. Works for now!
    float twoR[sizeof(onHandR)][sizeof(onHandR)];
    float minR = -1;
    float minP = -1;
    int minI, minJ;
    for (size_t i = 0; i < sizeof(onHandR); i++)
    {
        for (size_t j = 0; j < sizeof(onHandR); j++)
        {
            const float R = (onHandR[i] * onHandR[j]) / (onHandR[i] + onHandR[j]);
            twoR[i][j] = R;
            const float P = circuitV * circuitV / min(onHandR[i], onHandR[j]);
            if (RCheck(R, desiredR, minR) && powerCheck(P, maxPowerRating, minP)) {
                minR = R;
                minP = P;
                minI = i;
                minJ = j;
            }
        }
    }
    
    // Did we find something that works?
    if (minR != -1) {
        // winner winner chicken dinner
        printf("RDesire: %.1f\nRTotal: %.1f\nR1: %f\nR2: %f\nP: %.2f\n", desiredR, minR, onHandR[minI], onHandR[minJ], minP);
    }
    else {
        printf("Could not find suitable match.");
    }
}
