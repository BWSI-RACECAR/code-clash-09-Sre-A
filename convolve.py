"""
Copyright MIT BWSI Autonomous RACECAR Course
MIT License
Summer 2023

Code Clash #9 - Racecar code design (convolve.py)


Author: Paul Johnson

Difficulty Level: 7/10

Prompt: You’ve made it to a mini Grand Prix sprint race with only two obstacles, 
and you’ve only had enough time to test each obstacle separately in your labs. 
In your lab you found the average time to complete an obstacle event for each 
code design A and B for each obstacle 1 (a complex feature) and 2 (a straightaway).
You want to be 90% confident that one code design is better than another for the final run for both obstacles 1 and 2. 

See the background below for the tools you will use to figure this out. In the prompt below data

Background: Exponential, uniform probability distributions and convolutions

1) Exponential distribution - constant times
- An exponential probability distribution is used to find the distribution of
times around an average time until an event. It requires an input of the average
event rate per second: r (events/second), and outputs a measure of probability density.

- It’s probability density function (PDF) is f(t) = r  exp (-r t) and PDF literally says:
The probability of an event occurring between [t, t+t] is the event rate per second r, 
times the probability that an event has not occurred yet exp( -r t), known as the survival function.

2) Uniform distribution - widely distributed times
A uniform distribution has many applications when any value is expected between t[a,b] with 
no clear preferred value.
Statistical methods exist beyond the scope of this problem to identify if a data set belongs to
a symmetrical uniform and normal distributions.


3) Convolution
Given the prompt below, complete the convolution integral for the equation given in the picture. 

Prompt
[TODO] #1 Complete the convolution integral for design , validate the test case.
[TODO] #2 Implement a search algorithm given probModelAX to determine the time to completion (timeModelAX) with 90% probability of confidence. 
"""

class DataInput:
    def __init__(self):
        self.probModel = float(input("Enter the probability model: "))
        self.timesObs1A = list(map(float, input("Enter the times for Obstacle 1 Design A (comma-separated): ").split(',')))
        self.mean1A = sum(self.timesObs1A) / len(self.timesObs1A)
        self.timesObs2A = list(map(float, input("Enter the times for Obstacle 2 Design A (comma-separated): ").split(',')))
        self.mean2A = sum(self.timesObs2A) / len(self.timesObs2A)
        self.T = 50
        self.ti = [t for t in range(self.T)]


class Solution:
    def __init__(self, data):
        self.data = data
        self.f1A = [self.uniformPDF(fti, min(self.data.timesObs1A), max(self.data.timesObs1A)) for fti in self.data.ti]
        self.f2A = [self.exponentialPDF(fti, 1 / self.data.mean2A) for fti in self.data.ti]
        self.convolutionA = self.compute_convolution()
        self.mean1A = self.data.mean1A
        self.mean2A = self.data.mean2A
        self.timeModelA = self.search_ppf(self.compute_cdf(), self.data.probModel, epsilon=1e-4)

    def exp(self, x, terms=100):
        # ... (Same as before)

    def exponentialPDF(self, t, r):
        # ... (Same as before)

    def uniformPDF(self, t, a, b):
        # ... (Same as before)

    def integrateTrapz(self, f, x):
        # ... (Same as before)

    def compute_convolution(self):
        convolutionA = []
        for i in range(len(self.data.ti)):
            t_i = self.data.ti[i]
            f_t_i = self.uniformPDF(t_i, min(self.data.timesObs1A), max(self.data.timesObs1A))
            g_t = self.exponentialPDF(t_i, 1 / self.data.mean2A)
            I = [f_t_i * g_t_tau for g_t_tau in self.f2A[: i + 1]]
            convolutionA.append(self.integrateTrapz(I, self.data.ti[: i + 1]))
        return convolutionA

    def compute_cdf(self):
        A = self.integrateTrapz(self.convolutionA, self.data.ti)
        self.convolutionA = [self.convolutionA[i] / A for i in range(len(self.convolutionA))]
        return [self.integrateTrapz(self.convolutionA[: i], self.data.ti[: i]) for i in self.data.ti[1:]]

    def search_ppf(self, cdf_values, target, epsilon=1e-6):
        # ... (Same as before)


def main():
    data_input = DataInput()
    data_analysis = Solution(data_input)
    print(f"mean1A = {round(data_analysis.mean1A, 2)}")
    print(f"mean2A = {round(data_analysis.mean2A, 2)}")
    print(f"mean1A + mean2A = {round(data_analysis.mean1A + data_analysis.mean2A, 2)}")
    print("The probability that two events will take less than t' < t:")
    print("PrA(t'< {:2.1f} s) = {:2.2f}".format(data_analysis.timeModelA, data_input.probModel))


if __name__ == "__main__":
    main()
