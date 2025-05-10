from itertools import combinations
import random
import time
import sys
import itertools
sys.setrecursionlimit(1000001)
def resolution_sat(clauses):
    clauses_set = set(frozenset(c) for c in clauses)
    new = set()
    while True:
        pairs = list(itertools.combinations(clauses_set, 2))
        for (c1, c2) in pairs:
            for lit in c1:
                if -lit in c2:
                    resolvent = (c1 - {lit}) | (c2 - {-lit})
                    if not resolvent:
                        return False
                    if any(l in resolvent and -l in resolvent for l in resolvent):
                        continue
                    new.add(frozenset(resolvent))
        if new.issubset(clauses_set):
            return True
        clauses_set |= new
        new.clear()

def dp_eliminate(clauses, var):
    pos   = {c for c in clauses if var in c}
    neg   = {c for c in clauses if -var in c}
    others= {c for c in clauses if var not in c and -var not in c}
    resolvents = set()
    for ci in pos:
        for cj in neg:
            resolvent = (ci.union(cj)) - {var, -var}
            resolvents.add(frozenset(resolvent))
    return others.union(resolvents)

def dp_sat(clauses):
    clauses = set(clauses)
    if frozenset() in clauses:
        return False
    if not clauses:
        return True
    lit = next(iter(next(iter(clauses))))
    print("test")
    var = abs(lit)
    return dp_sat(dp_eliminate(clauses, var))

def unit_propagate(clauses, assignment):
    changed = True
    while changed:
        changed = False
        for c in list(clauses):
            if len(c) == 1:
                lit = next(iter(c))
                var, val = abs(lit), (lit > 0)
                if var in assignment and assignment[var] != val:
                    return None, None
                assignment[var] = val
                new_clauses = set()
                for d in clauses:
                    if lit in d:
                        continue
                    if -lit in d:
                        reduced = frozenset(d - {-lit})
                        if not reduced:
                            return None, None
                        new_clauses.add(reduced)
                    else:
                        new_clauses.add(d)
                clauses = new_clauses
                changed = True
                break
    return clauses, assignment

def pure_literal_assign(clauses, assignment):
    counts = {}
    for c in clauses:
        for lit in c:
            counts[lit] = counts.get(lit, 0) + 1
    pures = {lit for lit in counts if -lit not in counts}
    for lit in pures:
        assignment[abs(lit)] = (lit > 0)
    clauses = {c for c in clauses if not any(lit in c for lit in pures)}
    return clauses, assignment

def dpll_sat(clauses, assignment=None):
    if assignment is None:
        assignment = {}
    clauses = set(clauses)
    clauses, assignment = unit_propagate(clauses, assignment)
    if clauses is None:
        return False
    clauses, assignment = pure_literal_assign(clauses, assignment)
    if not clauses:
        return True
    if frozenset() in clauses:
        return False
    lit = next(iter(next(iter(clauses))))
    var = abs(lit)
    for val in [True, False]:
        new_assign = dict(assignment)
        new_assign[var] = val
        new_clauses = set()
        for c in clauses:
            if (var if val else -var) in c:
                continue
            if (-var if val else var) in c:
                new_clauses.add(frozenset(c - {(-var if val else var)}))
                print("test")
            else:
                new_clauses.add(c)
        if dpll_sat(new_clauses, new_assign):
            return True
    return False

def gen_random_cnf(n_vars, n_clauses, k=3, seed=None):
    rnd = random.Random(seed)
    cnf = []
    for _ in range(n_clauses):
        lits = set()
        while len(lits) < k:
            var = rnd.randint(1, n_vars)
            lit = var if rnd.choice([True, False]) else -var
            if -lit not in lits:
                lits.add(lit)
        cnf.append(frozenset(lits))
    return cnf
print("WARNING: Programul poate esua la probleme de dimensiuni mari")
num_samples = int(input("Number of samples"))
n_vars      = int(input("Number of variables"))
n_clauses   = int(input("Number of clauses"))
samples     = [gen_random_cnf(n_vars, n_clauses, seed=i) for i in range(num_samples)]
results     = []

for idx, cnf in enumerate(samples, 1):
    t0 = time.perf_counter(); r = resolution_sat(cnf);    rt = time.perf_counter() - t0
    t0 = time.perf_counter(); d = dp_sat(cnf);            dt = time.perf_counter() - t0
    t0 = time.perf_counter(); p = dpll_sat(cnf);          pt = time.perf_counter() - t0
    results.append((f'random_{idx}', rt, dt, pt))
print("| formula | resolution_time (s) | dp_time (s) | dpll_time (s) |")
print("|:--------|--------------------:|------------:|-------------:|")
for name, rt, dt, pt in results:
    print(f"| {name} | {rt:.4f} | {dt:.4f} | {pt:.4f} |")
