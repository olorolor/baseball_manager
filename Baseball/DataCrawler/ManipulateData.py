import pandas as pd
import re
import glob


def takeNumOut(filePath):
    table = pd.read_csv(filePath, engine='python',encoding='utf-8', index_col=0, header=0)

    print(table['이름/팀'])
    for index, line in enumerate(table['이름/팀']):
        print(line)
        # print('type(line) = ', type(line))
        selection = re.match(r'[^가-힣]+', line)
        # line.replace(str(selection.group()), '')
        # print(type(selection))
        if selection != None:
            print(selection.group())
            print(line.replace(str(selection.group()), ''))
            table['이름/팀'][index] = line.split(str(selection.group()))[1]

    table.to_csv(filePath, encoding='utf-8')

def getDataFromPath(path):
    fileList = glob.glob(path)

    for file in fileList:
        # print(file)
        takeNumOut(file)




if __name__ == "__main__":
    getDataFromPath("./BATTER/*.csv")


