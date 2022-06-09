#/usr/bin/env python

import sys
import os
import copy
import numpy as np

def usage(progname):
    print("Usage: " + progname + " matpower_filename")

def next_key(lines, pos):
    key = ""
    while pos < len(lines):
        terms = lines[pos].split()
        if terms and terms[0] in ["mpc.baseMVA", "mpc.bus", "mpc.gen", "mpc.branch", "mpc.gencost"]:
            key = terms[0]
            break
        else:
            pos += 1

    return key, pos

def read_raw_data(filename):
    # Read data from the MATPOWER case file.
    f = open(filename, "r")
    lines = f.readlines()
    p = 0
    data = {}
    while p < len(lines):
        key, p = next_key(lines, p)
        p += 1

        if key == "":
            break
        elif key == "mpc.baseMVA":
            data["mpc.baseMVA"] = float(lines[p-1].split("=")[1].strip().replace(";",""))
        else:
            q = p
            while not lines[q].startswith("];"):
                q += 1
            data[key] = [[float(x.strip().replace(";","")) for x in lines[j].split()] for j in range(p,q)]
    f.close()

    data["baseMVA"] = data["mpc.baseMVA"]

    return data

def add_bus(data):
    nbus = len(data["mpc.bus"])
    data["bus"] = [{} for i in range(nbus)]
    data["bus2idx"] = {}
    busref = []
    for i in range(nbus):
        data["bus2idx"][int(data["mpc.bus"][i][0])] = i
        if int(data["mpc.bus"][i][1]) == 3:
            busref.append(data["mpc.bus"][i][0])
    if not busref:
        print("Error: reference bus was not found.")
        sys.exit(-1)
    data["busref"] = []
    for r in busref:
        data["busref"].append(int(r))

    bf_name = [ "bus_i", "type", "Pd", "Qd", "Gs", "Bs", "area",
                "Vm", "Va", "baseKV", "zone", "Vmax", "Vmin" ]
    for i in range(nbus):
        for k, v in enumerate(bf_name):
            data["bus"][i][v] = data["mpc.bus"][i][k]
            if v == "Va":
                data["bus"][i][v] = data["mpc.bus"][i][k] * (np.pi/180)
            else:
                data["bus"][i][v] = data["mpc.bus"][i][k]

def add_gen(data):
    ngen = len(data["mpc.gen"])
    data["gen"] = []
    data["gencost"] = [[x for x in data["mpc.gencost"][k]] for (k,v) in enumerate(data["mpc.gen"]) if int(v[7]) == 1]
    data["busgen"] = [[] for i in range(len(data["bus"])) ]
    gf_name = [ "bus", "Pg", "Qg", "Qmax", "Qmin", "Vg", "mBase",
                "status", "Pmax", "Pmin", "Pc1", "Pc2", "Qc1min",
                "Qc1max", "Qc2min", "Qc2max", "ramp_agc", "ramp_10",
                "ramp_30", "ramp_q", "apf" ]
    j = 0
    for i in range(ngen):
        if int(data["mpc.gen"][i][7]) == 1:
            data["busgen"][data["bus2idx"][int(data["mpc.gen"][i][0])]].append(j)

            kv_pair = {}
            for k, v in enumerate(gf_name):
                kv_pair[v] = data["mpc.gen"][i][k]
                if v in ["Pg", "Qg", "Qmax", "Qmin", "Pmax", "Pmin"]:
                    kv_pair[v] /= data["baseMVA"]
            data["gen"].append(kv_pair)
            j += 1

def add_branch(data):
    nbr = len(data["mpc.branch"])
    data["branch"] = []
    lf_name = [ "fbus", "tbus", "r", "x", "b", "rateA", "rateB",
                "rateC", "ratio", "angle", "status", "angmin", "angmax" ]

    j = 0
    for i in range(nbr):
        if int(data["mpc.branch"][i][10]) == 1:
            kv_pair = {}
            for k, v in enumerate(lf_name):
                kv_pair[v] = data["mpc.branch"][i][k]
            data["branch"].append(kv_pair)
            data["branch"][j]["rateA"] /= data["baseMVA"]
            data["branch"][j]["rateB"] /= data["baseMVA"]
            data["branch"][j]["rateC"] /= data["baseMVA"]
            j += 1

def add_admittance_shunt(data):
    data["Gii"] = [ 0.0 for i in range(len(data["bus"])) ]
    data["Bii"] = [ 0.0 for i in range(len(data["bus"])) ]
    data["gs"] = []; data["bs"] = []
    data["YshR"] = []; data["YshI"] = []
    for i in range(len(data["bus"])):
        gs = data["bus"][i]["Gs"] / data["baseMVA"]
        bs = data["bus"][i]["Bs"] / data["baseMVA"]
        data["gs"].append(gs)
        data["bs"].append(bs)
        data["Gii"][i] = gs
        data["Bii"][i] = bs
        data["YshR"].append(gs)
        data["YshI"].append(bs)

    data["Gij"] = []; data["Bij"] = []
    data["Gji"] = []; data["Bji"] = []
    data["gij"] = []; data["bij"] = []
    data["YffR"] = []; data["YffI"] = []
    data["YttR"] = []; data["YttI"] = []
    data["YftR"] = []; data["YftI"] = []
    data["YtfR"] = []; data["YtfI"] = []

    for k in range(len(data["branch"])):
        fr = data["bus2idx"][int(data["branch"][k]["fbus"])]
        to = data["bus2idx"][int(data["branch"][k]["tbus"])]
        r = data["branch"][k]["r"]
        x = data["branch"][k]["x"]
        b = data["branch"][k]["b"]
        tap = data["branch"][k]["ratio"]
        angle = data["branch"][k]["angle"]

        if tap == 0.0:
            tap = 1.0
        tap *= np.exp((angle * (np.pi/180)) * 1j)

        Ys = 1 / (r + x*1j)
        Ytt = Ys + (0.5*b)*1j
        Yff = Ytt / (np.conj(tap)*tap)
        Yft = -Ys / np.conj(tap)
        Ytf = -Ys / tap

        data["Gij"].append(Yft.real); data["Bij"].append(Yft.imag)
        data["Gji"].append(Ytf.real); data["Bji"].append(Ytf.imag)
        data["gij"].append(Ys.real); data["bij"].append(Ys.imag)

        data["Gii"][fr] += Yff.real; data["Gii"][to] += Ytt.real
        data["Bii"][fr] += Yff.imag; data["Bii"][to] += Ytt.imag

        data["YffR"].append(Yff.real); data["YffI"].append(Yff.imag)
        data["YttR"].append(Ytt.real); data["YttI"].append(Ytt.imag)
        data["YftR"].append(Yft.real); data["YftI"].append(Yft.imag)
        data["YtfR"].append(Ytf.real); data["YtfI"].append(Ytf.imag)

def add_mapping(data):
    nbus = len(data["bus"])
    ngen = len(data["gen"])
    nbranch = len(data["branch"])

    data["busgen"] = {i:[] for i in range(nbus)}
    for g in range(ngen):
        idx = data["bus2idx"][int(data["gen"][g]["bus"])]
        data["busgen"][idx].append(g)

    data["frombus"] = {i:[] for i in range(nbus)}
    data["tobus"] = {i:[] for i in range(nbus)}
    for l in range(nbranch):
        fr = data["bus2idx"][int(data["branch"][l]["fbus"])]
        to = data["bus2idx"][int(data["branch"][l]["tbus"])]
        data["frombus"][fr].append(l)
        data["tobus"][to].append(l)

def parse(filename):
    data = read_raw_data(filename)
    case = os.path.splitext(os.path.basename(filename))[0]

    # Add raw data into data.
    add_bus(data)
    add_gen(data)
    add_branch(data)

    # Add a nodal admittance and shunt values.
    add_admittance_shunt(data)

    # Add mappings
    add_mapping(data)

    print(" ** Statistics of", case)
    print("  # buses     : {0:5d}".format(len(data["bus"])))
    print("  # generators: {0:5d} ({1:5d} active)".format(len(data["mpc.gen"]), len(data["gen"])))
    print("  # branches  : {0:5d} ({1:5d} active)".format(len(data["mpc.branch"]), len(data["branch"])))
    print("  # gencost   : {0:5d} ({1:5d} active)".format(len(data["mpc.gencost"]), len(data["gencost"])))

    return data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage(sys.argv[0])
        exit(-1)
    parse(sys.argv[1])
