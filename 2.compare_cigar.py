from sys import argv

wt_dic = {}
rgen_dic = {}

f1 = open(argv[1]) # WT
for line in f1:
    num, cigar = line.strip().split("\t")
    wt_dic[int(num)] = cigar
f1.close()

wt_count = int(num)

f2 = open(argv[2]) # RGEN
for line in f2:
    num, cigar = line.strip().split("\t")
    rgen_dic[int(num)] = cigar
f2.close()

rgen_count = int(num)
cnt = max( (rgen_count, wt_count) )

fo = open(".".join(argv[2].split(".")[:-1]) + "_diff.txt", "w")
for i in range(1, cnt+1):
    if i in wt_dic and i in rgen_dic and wt_dic[i] != rgen_dic[i]:
        fo.write('%d\t%s\t%s\n'%(i, wt_dic[i], rgen_dic[i]))
    elif i in rgen_dic and not i in wt_dic:
        fo.write('%d\t%s\t%s\n'%(i, ".", rgen_dic[i]))
    elif not i in rgen_dic and i in wt_dic:
        fo.write('%d\t%s\t%s\n'%(i, wt_dic[i], "."))

fo.close()
