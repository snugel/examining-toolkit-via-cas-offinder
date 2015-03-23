from glob import glob
from sys import argv
from os import path
from collections import defaultdict
import re
import pysam

cigar_len = 10
if len(argv) > 3:
    threshold = int(argv[3])

filename = '.'.join(argv[2].split(".")[:-1])
outfilename = "most_"+filename+".txt"

cigar_list = []

p1 = re.compile(r'[^\d]+')
p2 = re.compile(r'\d+')

def find_most_common_cigar(cigar_list):
    rtncigar = ''
    cigars = zip(*cigar_list)
    for cigar in cigars:
        max_dic = defaultdict(lambda: 0)
        cnt_i = 0
        cnt_d = 0
        for c in cigar:
            if c == 'I':
                cnt_i += 1
            elif c == 'D':
                cnt_d += 1
            else:
                max_dic[c] += 1
        if (cnt_i * 100.0) / len(cigar) > threshold or (cnt_d * 100.0) / len(cigar) > threshold:
            if cnt_i < cnt_d:
                rtncigar += 'D'
            else:
                rtncigar += 'I'
            continue
        if len(max_dic) > 1 and '_' in max_dic:
            del max_dic['_']
        rtncigar += max(max_dic.iteritems(), key=lambda e: e[1])[0]
    return rtncigar

def find_in_samfile(ref_filename, sam_filename):
    genes_dic = {}
    with open(ref_filename) as f:
        for line in f:
            entries = line.strip().split(":")
            sc1 = entries[0].split(".")
            if len(sc1) == 2:
                num, chrom = sc1
            else:
                num, chrom = entries[0].split()
            start, end = entries[1].split("-")
            entries = (num, int(start), int(end))
            if chrom in genes_dic:
                genes_dic[chrom].append( entries )
            else:
                genes_dic[chrom] = [ entries ]
    flag = False
    with pysam.Samfile(sam_filename) as f:
        for chrom in genes_dic:
            for num, start, end in genes_dic[chrom]:
                if flag == True:
                    yield old_num, find_most_common_cigar(cigar_list)
                else:
                    flag = True
                cigar_list = []
                for entry in f.fetch(chrom, start-1, end-1):
                    if entry.cigarstring != "":
                        pos = entry.pos
                        cigar = entry.cigarstring
                        str_list=p1.findall(cigar)
                        num_list=map(int, p2.findall(cigar))
    
                        fullcigar = ''.join(s*n for s, n in zip(str_list, num_list))
                        resultcigar = ""
                        if start < pos:
                            if end > pos:
                                resultcigar = (pos-start)*"_"
                                resultcigar += fullcigar[:end-pos]
                                cigar_list.append(resultcigar)
                        elif end > pos+150:
                            if start < pos+150:
                                resultcigar = fullcigar[start-pos:]
                                resultcigar += (end-pos-150)*"_"
                                cigar_list.append(resultcigar)
                        else:
                            resultcigar = fullcigar[start-pos:end-pos]
                            cigar_list.append(resultcigar)
                old_num = num
    yield old_num, find_most_common_cigar(cigar_list)
    
with open(outfilename, 'w') as fo:
    for cnt, (num, most_common_cigar) in enumerate(find_in_samfile(argv[1], argv[2])):
        if most_common_cigar != "":
            fo.write('%s\t%s\n'%(num, most_common_cigar))
        if cnt % 1000 == 0:
            print (cnt)
print "END"
