import numpy
from copy import copy

class JumpPenaltyDenoiser(object):
    """docstring for JumpPenaltyDenoiser"""
    def __init__(self, calculator):
        super(JumpPenaltyDenoiser, self).__init__()
        self.calculator = calculator

    def run_denoising(self, time_series, square, gamma, noisy=False):
        N = len(time_series)
        # r = zeros(0,1) # Knot locations
        r = []

        # Eold = Inf
        Eold = 1e99

        if noisy:
            print 'Iter# Global functional'

        # Iterate
        iter_num = 1
        maxiter = 50
        while iter_num < maxiter:

            if noisy:
                print '%5d %7.2e' % (iter_num, Eold)

            # Greedy scan for new knot location
            # NLL = zeros(N,1);
            NLL = numpy.zeros(N)

            # for i = 1:N
            for i in xrange(N):
                # Append new location
                # r1 = r;
                # r1(end+1) = i;
                # r1 = sort(r1);
                r1 = copy(r)
                r1.append(i)
                r1.sort()

                # Find optimum levels
                this_lh = self.find_optimum_levels(time_series, square, r1,
                                                   iter_num, N)
                NLL[i] = this_lh

            # Choose new location that minimizes the likelihood term
            # [v,i] = min(NLL);
            min_val = numpy.min(NLL)
            i = numpy.argmin(NLL)

            # Add to knot locations
            # r(end+1) = i;
            r.append(i)
            # r = sort(r);
            r.sort()

            # Re-compute solution at this iteration
            Enew, xnew = self.compute_solution(time_series, square, gamma,
                                                 r, iter_num, N)

            # Detect local minima in global functional
            if Eold < Enew:
                if noisy:
                    print 'Converged in %d iterations' % iter_num
                break

            Eold = Enew;
            iter_num += 1

        if noisy:
            if iter_num == maxiter:
                print 'Maximum iterations exceeded'

        x = xnew
        E = Enew
        return x

    def compute_global_fcn(self, x, y, square, gamma, iter_num):
        E = self.compute_likelihood(x, y, square)
        E += gamma * iter_num
        # if square:
            # E = 0.5 * self.calculator.sum((x-y)**2) + gamma*iter_num
        # else:
            # E = self.calculator.sum(self.calculator.abs(x-y)) + gamma*iter_num
        return E

    def compute_likelihood(self, x, y, square):
        if square:
            # likelihood = 0.5 * self.calculator.sum((x-y)**2)
            likelihood = self.calculator.sum(self.calculator.square_diff(x, y))
            likelihood *= 0.5
        else:
            # likelihood = self.calculator.sum(self.calculator.abs(x-y))
            likelihood = self.calculator.sum(self.calculator.abs_diff(x, y))
        return likelihood

    def mean_or_median(self, y, square):
        if len(y) == 0:
            m = numpy.nan
        else:
            if square:
                m = self.calculator.mean(y)
            else:
                m = self.calculator.median(y)
        return m

    def find_optimum_levels(self, time_series, square, r1, iter_num, N):
        # xtest = zeros(N,1);
        xtest = time_series.make_copy()
        xtest.set_signal_from_scalar(0.0)
        assert xtest.isfinite(), str(xtest)
        # L = 1:(r1(1)-1);
        upper_limit = r1[0]-1
        L = range(upper_limit)
        if len(L) > 0:
            # xtest(L) = mean_or_median(y(L), square);
            mean_or_median = self.mean_or_median(
                                time_series.get_values_at_indices(L),
                                square)
            xtest.set_signal_from_scalar(mean_or_median, L)
            assert xtest.isfinite(), str(L)
        else:
            pass
        # for j = 2:iter
        for j in xrange(1, iter_num):
            # L = r1(j-1):(r1(j)-1);
            L = range(r1[j-1], r1[j])
            if len(L) > 0:
                # xtest(L) = mean_or_median(y(L), square);
                mean_or_median = self.mean_or_median(
                                    time_series.get_values_at_indices(L),
                                    square)
                xtest.set_signal_from_scalar(mean_or_median, L)
                assert xtest.isfinite(), str(xtest)
            else:
                pass

        # L = r1(iter):N;
        L = range(r1[iter_num-1], N)
        # xtest(L) = mean_or_median(y(L), square);
        if len(L) > 0:
            mean_or_median = self.mean_or_median(
                                time_series.get_values_at_indices(L),
                                square)
            xtest.set_signal_from_scalar(mean_or_median, L)
            assert xtest.isfinite(), str(xtest)
        else:
            pass

        # Compute likelihood
        # NLL(i) = compute_likelihood(xtest, y, square);
        this_lh = self.compute_likelihood(xtest, time_series, square)
        assert numpy.isfinite(this_lh), str(xtest)
        assert xtest.isfinite(), str(xtest)
        return this_lh

    def compute_solution(self, time_series, square, gamma, r, iter_num, N):
        # i = 1:(r(1)-1);
        i = range(r[0]-1)
        # xnew = zeros(N,1);
        xnew = time_series.make_copy()
        xnew.set_signal_from_scalar(0.0)
        # xnew(i) = mean_or_median(y(i), square);
        mean_or_median = self.mean_or_median(
                            time_series.get_values_at_indices(i), square)
        xnew.set_signal_from_scalar(mean_or_median, i)
        # for j = 2:iter
        for j in xrange(1, iter_num):
            # i = r(j-1):(r(j)-1);
            i = range(r[j-1], r[j])
            # xnew(i) = mean_or_median(y(i), square);
            mean_or_median = self.mean_or_median(
                                time_series.get_values_at_indices(i),
                                square)
            xnew.set_signal_from_scalar(mean_or_median, i)

        # i = r(iter):N;
        i = range(r[iter_num-1], N)
        # xnew(i) = mean_or_median(y(i), square);
        mean_or_median = self.mean_or_median(
                            time_series.get_values_at_indices(i), square)
        xnew.set_signal_from_scalar(mean_or_median, i)

        # Compute global functional value at current solution
        # Enew = compute_global_fcn(xnew, y, square, gamma, iter);
        Enew = self.compute_global_fcn(xnew, time_series, square, gamma,
                                       iter_num)
        return Enew, xnew

