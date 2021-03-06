from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import ntpath


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
    ans = pd.read_csv(fname)

    return ans

def getMinutesMissed(df, df_allow):

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
            rehearsal_end_obj = datetime.strptime(str(rehearsal_end), '%I:%M %p')  # convert string to datetime
            day_of_week = col_str[1].split(',')  # get day of week
            day_of_week = day_of_week[0]  # get day of week
            missed_minutes_col = str('Minutes missed at ' + col_str[1])  # add column to existing df
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
                    time_in_allowed = getAllowedTime(df_allow, day_of_week, row['First name'], row['Last name'])

                    if time_in_obj - rehearsal_start_obj > time_in_allowed - rehearsal_start_obj:
                        time_missed = time_in_obj - rehearsal_start_obj
                        time_missed_minutes = time_missed.total_seconds() / 60
                        df.at[index, comments_col] = 'Missed ' + str(time_missed_minutes) + \
                                                     ' mins for signing in on UDB at ' + time_in + \
                                                     ' . They were allowed to arrive at ' + \
                                                     str(time_in_allowed.strftime("%I:%M %p"))
                    else:
                        time_missed = 0
                        df.at[index, comments_col] = str(time_missed)

                # handle DNCI entries
                elif 'DNCI' in str(row[col]):
                    time_missed = rehearsal_end_obj - rehearsal_start_obj
                    time_missed_minutes = time_missed.total_seconds() / 60
                    df.at[index, comments_col] = 'Missed ' + str(
                        time_missed_minutes) + ' (entire rehearsal) because of DNCI'

                elif 'EBD' in str(row[col]):
                    time_missed_minutes = 0
                    df.at[index, comments_col] = 'EBD'

                else:
                    time_missed_minutes = 0

                df.at[index, missed_minutes_col] = time_missed_minutes

    return df



def getAllowedTime(df_allow, day_of_week, first_name, last_name):
    print(df_allow)
    try:
        tardy_student = df_allow.loc[
            (df_allow['Last name'] == last_name) & (df_allow['First name'] == first_name)]
        try:
            t_in_allw = tardy_student[day_of_week + str(' Arrive')]
            # time_in_allowed_str = str(t_in_allw.iloc[0])
            t_in_allw = datetime.strptime(str(t_in_allw.iloc[0]), '%H:%M')
        except:
            print('found ' + str(first_name) + ' ' + str(last_name)+ ' in allowance spreadsheet, '
                                                                     'but could not parse time\n')
            t_in_allw = datetime.strptime(str('17:30'), '%H:%M')

    except KeyError:
        print(str(first_name) + ' ' + str(last_name) + ' not found in allowance sheet, '
                                                       'setting default allowed time in of 17:30')
        t_in_allw = datetime.strptime(str('17:30'), '%H:%M')

    else:
        print('unhandled exception in getAllowedTime function\n')
        t_in_allw = datetime.strptime(str('17:30'), '%H:%M')

    return t_in_allw

def getOutputFileName(fname):

    head, tail = ntpath.split(fname)
    f_out = tail
    print('Exporting to CALC_' + tail + ' .....')

    return f_out

# ========================================================


if __name__ == '__main__':

    fname = getUDBfile()  # get UDB file path from UI
    fname_allow = getAllowancefile()  # get allowance file path from UI
    df = readfile(fname)  # read file into df
    df_allow = readfile(fname_allow)  # read file into df
    df_mm = getMinutesMissed(df, df_allow)  # get minutes missed dataframe
    fname_out = getOutputFileName(fname)  # get output file name

# TODO: make this better
    df_mm.to_csv(str('CALC_'+ fname_out))  # output to new csv
