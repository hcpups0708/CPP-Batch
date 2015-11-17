import os
import sh
import re
import subprocess

# the base path of student's homework
basepath = "/home/mhwong/Documents/ICP/Homework5/student"

# two test data set
test_data_accepted = [
    "123.45\n",
    "123.\n",
    ".45\n",
    "+23.456\n",
    "-0.\n",
    "+.0\n",
    "++--23.45\n"
]
test_data_rejected = [
    "1234\n",
    "1..2\n",
    "1.2.3\n",
    "+12.+34\n",
    "+123.45+\n",
    ".\n",
    "+-+-.\n",
    "\n"
]

# open the result file to write
result = open(basepath + "/result", 'w')

# the header line
header_line = '{:>18} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}'\
    .format('FileName', '123.45', '123.', '.45', '+23.456', '-0.', '+.0', '++--23.45', '1234', '1..2', '1.2.3', '+12.+34',
            '+123.45+', '.', '++--.', 'newline', 'Score')
result.write(header_line)
result.write("\n")

# for all files under the base path
for file in sorted(os.listdir(basepath)):
    path = os.path.join(basepath, file)     # to form a full pathname
    if not os.path.isdir(path):             # continue when it isn't a directory
        if file.endswith(".c") or file.endswith(".cpp"):    # check if it is ended with c or cpp
            print(file)
            result.write('{:>18} '.format(file))            # print the file name
            compile_cmd = ["gcc", "-std=c99", path, "-o", path + ".o"]      # command to compile the file
            p = subprocess.Popen(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)       # run the command
            p.wait()
            return_code = p.returncode      # get the return code
            if return_code == 0:  # if not 0 => compile error
                try:
                    correct_counter = 0
                    for data in test_data_accepted:     # test with the first data set
                        p = subprocess.Popen([path + ".o"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
                        response = p.communicate(str.encode(data), timeout=2)[0].decode("utf-8")    # send the data
                        if re.match('.*Accept.*', response, re.IGNORECASE | re.DOTALL):
                            print(data.replace("\n", "") + " correct")
                            result.write("{:>10} ".format("O"))
                            correct_counter += 1
                        else:
                            print(data.replace("\n", "") + " incorrect")
                            result.write("{:>10} ".format("X"))

                    for data in test_data_rejected:     # test with the second data set
                        p = subprocess.Popen([path + ".o"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
                        response = p.communicate(str.encode(data), timeout=2)[0].decode("utf-8")
                        if re.match('.*Reject.*', response, re.IGNORECASE | re.DOTALL):
                            print(data.replace("\n", "") + " correct")
                            result.write("{:>10} ".format("O"))
                            correct_counter += 1
                        else:
                            print(data.replace("\n", "") + " incorrect")
                            result.write("{:>10} ".format("X"))
                    score = round(correct_counter / 15 * 100, 3)
                    result.write("{:>10} ".format(str(score) + "\n"))
                    # if correct_counter == 15:
                    #     sh.cp(path, basepath + "/correct/" + file)
                    # elif correct_counter == 0:
                    #     sh.cp(path, basepath + "/incorrect" + file)
                except subprocess.TimeoutExpired:
                    print('time out')
                    result.write("{:>10} ".format("TO\n"))
                    p.kill()
                    # sh.cp(path, basepath + "/timeout/" + file)
                sh.rm(path + ".o")
            else:
                # sh.cp(path, basepath + "/compile_error/" + file)
                result.write("{:>10} ".format("CE\n"))
                print('compile error')

        else:
            print(file)
            print("not matched")

