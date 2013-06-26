"""
Implements the least-squares and least-absolute jump penalization methods
described by Little and Jones:
Little, M. A., and Jones, N. S. Generalized methods and solvers for noise
removal from piecewise constant signals. II. New methods.
Proc. R. Soc. A-Math. Phys. Eng. Sci. 467, 2135 (2011), 3115-3140.

Input arguments:
square     `True` perform least-squares fitting,
           `False` perform least-absolute (robust) fitting.
gamma      Positive regularization parameter.
"""

import numpy
from copy import copy

class JumpPenaltyDenoiser(object):
    """docstring for JumpPenaltyDenoiser"""
    def __init__(self, calculator):
        super(JumpPenaltyDenoiser, self).__init__()
        self.calculator = calculator

    def run_denoising(self, raw_ts, square, gamma, noisy=False):
        N = len(raw_ts)
        knot_list = []

        H_old = 1e99

        if noisy:
            print 'Iter# Global functional'

        iter_num = 1
        maxiter = 50
        while iter_num < maxiter:
            if noisy:
                print '%5d %7.2e' % (iter_num, H_old)
            # =====================================
            # = Greedy scan for new knot location =
            # =====================================
            NLL = numpy.zeros(N)
            for i in xrange(N):
                # Append new location
                trial_knot_list = copy(knot_list)
                trial_knot_list.append(i)
                trial_knot_list.sort()
                # Find optimum levels
                this_lh = self.find_optimum_levels(
                            raw_ts, square, trial_knot_list, iter_num, N)
                NLL[i] = this_lh
                # end for
            # ==========================================================
            # = Choose new location that minimizes the likelihood term =
            # ==========================================================
            min_val = numpy.min(NLL)
            i = numpy.argmin(NLL)
            # Add to knot locations
            knot_list.append(i)
            knot_list.sort()
            # Re-compute solution at this iteration
            H_new, smooth_ts = self.compute_solution(raw_ts, square, gamma,
                                                     knot_list, iter_num, N)
            # =========================
            # = Check for convergence =
            # =========================
            if H_old < H_new:
                if noisy:
                    print 'Converged in %d iterations' % iter_num
                break # stop while loop
            else:
                H_old = H_new;
                iter_num += 1
            # end while

        if noisy:
            if iter_num == maxiter:
                print 'Maximum iterations exceeded'
        return smooth_ts

    def compute_global_fcn(self, m, x, square, gamma, iter_num):
        H = self.compute_likelihood(m, x, square)
        H += gamma * iter_num
        return H

    def compute_likelihood(self, m, x, square):
        if square:
            likelihood = self.calculator.sum(self.calculator.square_diff(m, x))
            likelihood *= 0.5
        else:
            likelihood = self.calculator.sum(self.calculator.abs_diff(m, x))
        return likelihood

    def compute_level(self, x, square):
        if len(x) == 0:
            level = numpy.nan
        else:
            if square:
                level = self.calculator.mean(x)
            else:
                level = self.calculator.median(x)
        return level

    def find_optimum_levels(self, raw_ts, square, knot_list, iter_num, N):
        smooth_ts = raw_ts.make_copy()
        smooth_ts.set_signal_from_scalar(0.0)
        upper_limit = knot_list[0]-1
        L = range(upper_limit)
        if len(L) > 0:
            level = self.compute_level(raw_ts.get_values_at_indices(L), square)
            smooth_ts.set_signal_from_scalar(level, L)
            assert smooth_ts.isfinite(), str(L)
        else:
            pass
        for j in xrange(1, iter_num):
            L = range(knot_list[j-1], knot_list[j])
            if len(L) > 0:
                level = self.compute_level(
                            raw_ts.get_values_at_indices(L), square)
                smooth_ts.set_signal_from_scalar(level, L)
                assert smooth_ts.isfinite(), str(smooth_ts)
            else:
                pass
        L = range(knot_list[iter_num-1], N)
        if len(L) > 0:
            level = self.compute_level(raw_ts.get_values_at_indices(L), square)
            smooth_ts.set_signal_from_scalar(level, L)
            assert smooth_ts.isfinite(), str(smooth_ts)
        else:
            pass
        # Compute likelihood
        this_lh = self.compute_likelihood(smooth_ts, raw_ts, square)
        return this_lh

    def compute_solution(self, raw_ts, square, gamma, knot_list, iter_num, N):
        i = range(0, knot_list[0]-1)
        smooth_ts = raw_ts.make_copy()
        smooth_ts.set_signal_from_scalar(0.0)
        level = self.compute_level(raw_ts.get_values_at_indices(i), square)
        smooth_ts.set_signal_from_scalar(level, i)
        for j in xrange(1, iter_num):
            i = range(knot_list[j-1], knot_list[j])
            level = self.compute_level(raw_ts.get_values_at_indices(i), square)
            smooth_ts.set_signal_from_scalar(level, i)
        i = range(knot_list[iter_num-1], N)
        level = self.compute_level(raw_ts.get_values_at_indices(i), square)
        smooth_ts.set_signal_from_scalar(level, i)
        # Compute global functional value at current solution
        H = self.compute_global_fcn(smooth_ts, raw_ts, square, gamma, iter_num)
        return H, smooth_ts

