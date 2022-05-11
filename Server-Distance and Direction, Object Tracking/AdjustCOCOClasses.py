# import required module
import os

# assign directory
directory = 'train2017'

# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(f)
        with open(f, 'r+') as f:
            lines = list(f)
            separator = " "
            new_lines = []

            while len(lines) != 0:
                line = lines.pop(0)
                line_split = line.split()
                if line_split[0] == '0':
                    line_split[0] = '0'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '1':
                    line_split[0] = '1'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '2':
                    line_split[0] = '2'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '3':
                    line_split[0] = '3'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '5':
                    line_split[0] = '4'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '6':
                    line_split[0] = '5'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '7':
                    line_split[0] = '6'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '8':
                    line_split[0] = '7'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '9':
                    line_split[0] = '8'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '10':
                    line_split[0] = '9'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '11':
                    line_split[0] = '10'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '12':
                    line_split[0] = '11'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '13':
                    line_split[0] = '12'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '15':
                    line_split[0] = '13'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '16':
                    line_split[0] = '14'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '17':
                    line_split[0] = '15'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '18':
                    line_split[0] = '16'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '19':
                    line_split[0] = '17'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '56':
                    line_split[0] = '18'
                    line = separator.join(line_split)
                    new_lines.append(line)
                elif line_split[0] == '58':
                    line_split[0] = '19'
                    line = separator.join(line_split)
                    new_lines.append(line)
            f.seek(0)
            f.truncate(0)
            for line in new_lines:
                f.write(line)
                f.write("\n")
            f.close()
