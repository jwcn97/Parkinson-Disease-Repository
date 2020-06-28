def pearson():
    for i in combinations([Lxi,Lyi,Lzi],2):
    #             display(pd.DataFrame(i))
        for x,y in [i]:
    #                 display(pd.DataFrame(x*y))
            if len(Lxi) == leng[0]:
                appended4.append(sum(x*y)/(leng[0]-1))
                appended4.append(float((sum(x*y)/(leng[0]-1)))/(appended2[2][0]*appended2[2][1]))

            elif len(Lxi) == leng[1]:
                appended4.append(sum(x*y)/(leng[1]-1))
                appended4.append(float((sum(x*y)/(leng[1]-1)))/(appended2[2][0]*appended2[2][2]))

            elif len(Lxi) == leng[2]:
                appended4.append(sum(x*y)/(leng[2]-1))
                appended4.append(float((sum(x*y)/(leng[2]-1)))/(appended2[2][1]*appended2[2][2]))

        covstats4 = {'Covariance':[appended4[0], appended4[6], appended4[12]],
                'Pearsons Correlation Coefficient':[appended4[1], appended4[7],appended4[13]]}

        covstats4_df = pd.DataFrame(covstats4,index=[['xy','xy','xy'],['try1','try2','try3']])

        covstats5 = {'Covariance':[appended4[2], appended4[8], appended4[14]],
                'Pearsons Correlation Coefficient':[appended4[3], appended4[9],appended4[15]]}

        covstats5_df = pd.DataFrame(covstats5,index=[['xz','xz','xz'],['try1','try2','try3']])

        covstats6 = {'Covariance':[appended4[4], appended4[10], appended4[16]],
                'Pearsons Correlation Coefficient':[appended4[5], appended4[11],appended4[17]]}

        covstats6_df = pd.DataFrame(covstats6,index=[['yz','yz','yz'],['try1','try2','try3']])

        gyro_df1 = (timestats4_df.append(timestats5_df)).append(timestats6_df)
        gyro_df2 = (covstats4_df.append(covstats5_df)).append(covstats6_df)