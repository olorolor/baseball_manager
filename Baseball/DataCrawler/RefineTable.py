import pandas as pd
import numpy as np
import os.path
import glob
import re

class Data():

    fileName = ''

    columnList = ['이름/팀', 'WAR', 'G', '타석', '타수', '득점', '안타', '2타',
                  '3타', '홈런', '루타', '타점', '도루', '도실', '볼넷',
                  '사구', '고4', '삼진', '병살', '희타', '희비', '타율',
                  '출루율', '장타', 'OPS', 'wOBA', 'WRC+', 'WAR', '선수명','연도','포지션']

    def __init__(self, fileName):
        self.fileName = fileName


    def readCsvFile(self):
        table = pd.read_csv(self.fileName, engine='python', encoding='utf-8',
                            index_col=0, header=0)
            
        return table


    def addColumn(self, table):

        table['선수명'] = np.nan
        table['팀명'] = np.nan
        table['연도'] = np.nan
        table['포지션'] = np.nan

        return table

    def takeOutIndex(self, indexToPosition):
        index = re.search('^[0-9]{1,}', indexToPosition)
        nameToPosition = indexToPosition[len(str(index.group())):]

        return nameToPosition


    def getPlayerName(self, year, nameToPosition):
        selection = nameToPosition.split(year)[0]

        return selection


    def setYear(self, filePath):
        fileName = filePath.split('\\')[1]
        year = fileName[0:4]

        return year


    def getTeamName(self, fileName):
        yearAndTeamName = fileName.split('_')[0]
        teamName = yearAndTeamName[4:]

        return teamName


    def getPosition(self, yearToPosition):
        year = re.search('[0-9]{1,}', yearToPosition)

        position = yearToPosition[(len(year.group()) + 1):]
        return position



def main():

    path = "./BATTER_MOD/*.csv"

    fileList = glob.glob(path)

    columList = ['이름/팀', 'WAR', 'G', '타석', '타수', '득점', '루타', '타점', '도루',
                '도실', '사구', '고4', '삼진', '병살', '희타', '희비', '타율', '장타',
                 'OPS', 'wOBA', 'WRC+', 'WAR.1']

    for file in fileList:
        obj = Data(file)

        table = obj.readCsvFile()

        # 'nameToPosition'항목의 형식은 '홍길동18롯1B'와 같은 형식이다.
        # 18은 연도, 롯은 팀명, 1B는 포지션/ 팀안에서 연도와 팀은 모두 같다.
        teamName = obj.getTeamName(file.split('\\')[1])
        year = obj.setYear(file)

        modifiedTable = obj.addColumn(table)

        indexToPositionList = modifiedTable['이름/팀']

        nameList = []
        positionList = []

        for index, indexToPosition in enumerate(indexToPositionList):
            nameToPosition = obj.takeOutIndex(indexToPosition)
            name = obj.getPlayerName(year[2:], nameToPosition)

            yearToPosition = nameToPosition.split(name)[1]
            position = yearToPosition.split(teamName[0])

            if len(yearToPosition) <= 2:
                nameList.append(name)

                # 혹시나 팀명이나 연도 표기가 안되어있는 선수가 있을 것에 대비하여.
                if (len(position) == 0) or (position[1] == ''):
                    positionList.append('')
                else:
                    positionList.append(position[1])

                continue
            #
            position = obj.getPosition(yearToPosition)
            teamName = obj.getTeamName(file.split('\\')[1])
            year = obj.setYear(file)
            # print(name, year, teamName, position)

            nameList.append(name)
            positionList.append(position)

        nameList_series = pd.Series(nameList)
        modifiedTable['선수명'] = nameList_series
        modifiedTable['팀명'] = teamName
        modifiedTable['연도'] = year

        positionList_series = pd.Series(positionList)
        modifiedTable['포지션'] = positionList_series
        
        # 필요없어진 컬럼 삭제하기
        for column in columList:
            del modifiedTable[column]
            
        columnChangedTable = pd.DataFrame(modifiedTable, columns=['선수명', '연도', '팀명', '포지션',
                                             '안타', '2타', '3타', '홈런', '볼넷', '출루율'])

        columnChangedTable.to_csv(str(year) + str(teamName) + '_batter.csv', encoding="utf-8", mode="w")
        print(str(year) + str(teamName) + '_batter.csv : COMPLETED')

if __name__ == "__main__":

    main()


