from tkinter.filedialog import askopenfilename
import pandas as pd
from datetime import datetime


def getfile():

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

    fname = getfile()
    df = readfile(fname)

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
            rehearsal_start_obj = datetime.strptime(str(rehearsal_start), '%I:%M %p') # convert string to datetime
            rehearsal_end_obj   = datetime.strptime(str(rehearsal_end), '%I:%M %p') # convert string to datetime
            missed_minutes_col =  str('Minutes missed at ' + col_str[1]) # add column to existing df
            comments_col = str('Comments on ' + col_str[1]) # add column to existing df
            df.insert(len(df.columns), missed_minutes_col, 0) # insert column at end of df
            df.insert(len(df.columns), comments_col, '')  # insert column at end of df

            for index, row in df.iterrows():

                # handle tardy entries
                if 'Tardy' in str(row[col]):
                    time_in = str(row[col]).split('|')
                    time_in = time_in[1]
                    time_in_obj = datetime.strptime(time_in, ' %I:%M %p')
                    time_missed = time_in_obj - rehearsal_start_obj
                    time_missed_minutes = time_missed.total_seconds()/60
                    df.at[index, comments_col] = 'Missed ' + str(time_missed_minutes) + ' mins for signing in on UDB at ' + time_in

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
