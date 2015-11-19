import os
import re
import subprocess

# the base path of student's homework
basepath = "C:/Users/user/Documents/GitHub/CPP-Batch/hw6"

# the base path of gcc compiler
gccpath = "C:/Program Files (x86)/CodeBlocks/MinGW/bin"

# two test data set
input_string = [
    '1\n1\n',
    '10\n1\n',
    '9999999\n90\n',
    '987654321\n123456789\n',
    '987654321987654321\n123456789123456789\n',
    '12345\n9\n',
    '1000000000000000000000000000000\n100000000000000000000000000000\n',
    '1234\n123\n',
    '10\n0\n',
    '0\n0\n'
]
output_string = [
    ['2','0','1'],
     ['11','9','10'],
     ['10000089','9999909','899999910'],
     ['1111111110','864197532','121932631112635269'],
     ['1111111111111111110','864197532864197532','121932631356500531347203169112635269'],
     ['12354','12336','111105'],
     ['1100000000000000000000000000000','900000000000000000000000000000','100000000000000000000000000000000000000000000000000000000000'],
     ['1357','1111','151782'],
     ['10','10','0'],
     ['0','0','0']
]

# open the result file to write
result = open(os.path.join(basepath, "result.txt") , 'w')
# the header line
header_line = '{:>18} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}'\
    .format('FileName', '1_1', '10_1', '9999999_90', '9~1_1~9', '9~19~1_1~91~9', '12345_9', '10^30_10^29', '1234_123', '10_0', '0_0', 'Score')
result.write(header_line)
result.write("\n")
a=os.listdir(basepath)
print(os.listdir(basepath))
# for all files under the base path
for file in sorted(os.listdir(basepath)):
    path = os.path.join(basepath, file)     # to form a full pathname
    if not os.path.isdir(path):             # continue when it isn't a directory
        if file.endswith(".c") or file.endswith(".cpp"):    # check if it is ended with c or cpp
            print(file)
            result.write('{:>18} '.format(file))            # print the file name
            compile_cmd = [os.path.join(gccpath, "gcc.exe"), "-std=c99", path, "-o", path + ".exe"]      # command to compile the file
            p = subprocess.Popen(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)       # run the command
            p.wait()
            return_code = p.returncode      # get the return code
            if return_code == 0:  # if not 0 => compile error
                #try:
                    correct_counter = 0.0
                    for idx,input in enumerate(input_string):     # test with the first data set
                        p = subprocess.Popen([path + ".exe"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
                        response = p.communicate(str.encode(input))[0].decode("utf-8")    # send the data
                        result_string=''
                        if re.match('.*a ?\+ ?b ?=?:? ?'+output_string[idx][0]+r' ?(?:$|(\r\n))', response, re.IGNORECASE | re.DOTALL|re.M):
                            print(input.replace("\n", "_") + " +_correct")
                            result_string+='+'
                            correct_counter += 40
                        else:
                            print(input.replace("\n", "_") + " +_incorrect")
                            result_string+='X'
                        if re.match('.*a ?- ?b ?=?:? ?'+output_string[idx][1]+r' ?(?:$|(\r\n))', response, re.IGNORECASE | re.DOTALL):
                            print(input.replace("\n", "_") + " -_correct")
                            result_string+='-'
                            correct_counter += 40
                        else:
                            print(input.replace("\n", "_") + " -_incorrect")
                            result_string+='X'
                        if re.match('.*a ?[\*x] ?b ?=?:? ?'+output_string[idx][2]+r' ?(?:$|(\r\n))', response, re.IGNORECASE | re.DOTALL):
                            print(input.replace("\n", "_") + " *_correct")
                            result_string+='*'
                            correct_counter += 20
                        else:
                            print(input.replace("\n", "_") + " *_incorrect")
                            result_string+='X'
                        result.write("{:>10} ".format(result_string))
                    score = round(correct_counter /10, 3)
                    result.write("{:>10} ".format(str(score) + "\n"))
                    # if correct_counter == 15:
                    #     sh.cp(path, basepath + "/correct/" + file)
                    # elif correct_counter == 0:
                    #     sh.cp(path, basepath + "/incorrect" + file)
                #except subprocess.TimeoutExpired:
                #    print('time out')
                #    result.write("{:>10} ".format("TO\n"))
                #    p.kill()
                # sh.cp(path, basepath + "/timeout/" + file)
            else:
                # sh.cp(path, basepath + "/compile_error/" + file)
                result.write("{:>10} ".format("CE\n"))
                print('compile error')

        else:
            print(file)
            print("not .c or .cpp")

