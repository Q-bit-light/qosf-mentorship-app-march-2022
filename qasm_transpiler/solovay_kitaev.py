"""
Recursive algorithm (on depth n (calling n-1))
Args: 
gate = unitary gate we wish to approximate
depth = accuracy of approximation (as n tends to infinity we get perfect accuracy)

Work in Progress!
"""
class SolovayKitaev:
    def solovayKitaev(gate, depth, basis):
        if depth==0:
            return self.basicApprox(gate)
        else:
            self.solovayKitaev(gate, depth-1)

    def basicApprox(gate):
        pass