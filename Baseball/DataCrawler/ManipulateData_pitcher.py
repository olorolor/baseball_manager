import pandas as pd
import numpy as np
import os.path
import glob
import re


class Data():
    fileName = ''


    def __init__(self, fileName):
        self.fileName = fileName

    def readCsvFile(self):
        table = pd.read_csv(self.fileName, engine='python', encoding='utf-8', index_col=0, header=0)

        return table

    def addColumn(self, table):
        table['팀명'] = np.nan
        table['연도'] = np.nan

        return table


    def setYear(self, filePath):
        fileName = filePath.split('\\')[1]
        year = fileName[0:4]

        return year

    def getTeamName(self, fileName):
        yearAndTeamName = fileName.split('_')[0]
        teamName = yearAndTeamName[4:]

        return teamName


def main():
    path = "./PITCHER/*.csv"

    fileList = glob.glob(path)

    columList = ['순', '팀', 'FIP', '출장', 'ERA', 'BB/9', 'HR/9',
                 'K/BB', 'PFR', 'BIPA', 'LOB%', '타율']

    for file in fileList:
        obj = Data(file)

        table = obj.readCsvFile()
        print(table)
        teamName = obj.getTeamName(file.split('\\')[1])
        year = obj.setYear(file)

        # print(teamName, year)

        modifiedTable = obj.addColumn(table)


        teamName = obj.getTeamName(file.split('\\')[1])
        year = obj.setYear(file)

        modifiedTable['팀명'] = teamName
        modifiedTable['연도'] = year
        #
        # 필요없어진 컬럼 삭제하기
        for column in columList:
            del modifiedTable[column]

        columnChangedTable = pd.DataFrame(modifiedTable, columns=['이름', '연도', '팀명',
                                                                  '이닝', 'K/9', '출루율'])


        columnChangedTable.rename(columns={'이름':'선수명'}, inplace=True)
        # print(columnChangedTable)

        del modifiedTable
        del columnChangedTable
        # columnChangedTable.to_csv(str(year) + str(teamName) + '_pitcher.csv', encoding="utf-8", mode="w")
        # print(str(year) + str(teamName) + '_pitcher.csv : COMPLETED')



if __name__ == "__main__":
    main()