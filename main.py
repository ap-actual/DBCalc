from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import pandas as pd
from datetime import datetime


def getUDBfile():

    answer = messagebox.askokcancel("UDB Output Select", "Hello! Please select UDB output file...")
    filepath = askopenfilename()
    return filepath

def getAllowancefile():

    answer = messagebox.askokcancel("UDB Output Select", "Now select Allowance file...")
    filepath = askopenfilename()
    return filepath


def readfile(fname):

    # TODO: input checks & error handling

    try:
        ans = pd.read_csv(fname)

    except:
        ans = -1

    return ans

# ========================================================


if __name__ == '__main__':

    fname = getUDBfile()
    fname_allow = getAllowancefile()
    df = readfile(fname)
    df_allow = readfile(fname_allow)

    # Go through each rehearsal
    for col in df.columns:

        # if header contains the word 'Rehearsal', then it's a rehearsal!
        if 'Rehearsal' in str(col):
            # pull out rehearsal start & end time from column heading string
            col_str = str(col)
            col_str = col_str.split('\n')
            rehearsal_time = col_str[2]
            rehearsal_time = rehearsal_time.split('-')
            rehearsal_start = rehearsal_time[0]
            rehearsal_end = rehearsal_time[1]
            rehearsal_start_obj = datetime.strptime(str(rehearsal_start), '%I:%M %p')  # convert string to datetime
            rehearsal_end_obj   = datetime.strptime(str(rehearsal_end), '%I:%M %p')  # convert string to datetime
            day_of_week = col_str[1].split(',')  # get day of week
            day_of_week = day_of_week[0]  # get day of week
            missed_minutes_col =  str('Minutes missed at ' + col_str[1])  # add column to existing df
            comments_col = str('Comments on ' + col_str[1])  # add column to existing df
            df.insert(len(df.columns), missed_minutes_col, 0)  # insert column at end of df
            df.insert(len(df.columns), comments_col, '')  # insert column at end of df

            for index, row in df.iterrows():

                # handle tardy entries
                if 'Tardy' in str(row[col]):
                    time_in = str(row[col]).split('|')
                    time_in = time_in[1]
                    time_in_obj = datetime.strptime(time_in, ' %I:%M %p')

                    # check if time in is after allowed time
                    tardy_student = df_allow.loc[(df_allow['Last name'] == row['Last name']) & (df_allow['First name'] == row['First name'])]
                    time_in_allowed = tardy_student[day_of_week+str(' Arrive')]
                    time_in_allowed_str = str(time_in_allowed.iloc[0])
                    time_in_allowed = datetime.strptime(str(time_in_allowed.iloc[0]), '%H:%M')

                    if time_in_obj - rehearsal_start_obj > time_in_allowed - rehearsal_start_obj:
                        time_missed = time_in_obj - rehearsal_start_obj
                        time_missed_minutes = time_missed.total_seconds()/60
                        df.at[index, comments_col] = 'Missed ' + str(time_missed_minutes) + ' mins for signing in on UDB at ' + time_in + ' . They were allowed to arrive at ' + str(time_in_allowed_str)

                    else:
                        time_missed = 0
                        df.at[index, comments_col] = str(time_missed)

                # handle DNCI entries
                elif 'DNCI' in str(row[col]):
                    time_missed = rehearsal_end_obj-rehearsal_start_obj
                    time_missed_minutes = time_missed.total_seconds()/60
                    df.at[index, comments_col] = 'Missed ' + str(time_missed_minutes) + ' (entire rehearsal) because of DNCI'

                elif 'EBD' in str(row[col]):
                    time_missed_minutes = -999
                    df.at[index, comments_col] = 'EBD'

                else:
                    time_missed_minutes = 0

                df.at[index, missed_minutes_col] = time_missed_minutes

# TODO: make this better
df.to_csv(str('OUTPUT.csv'))
