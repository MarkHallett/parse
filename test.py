# test.py
# Mark Hallett


import os
import collections

class Daydata(object):
    def __init__(self, day, data, value= None, description=None):
        '''
        This class is a container for the data for a given day (mon-fri)
        each instance contains the appropriate format/template to produce the requied output
        '''
        self.data = {}
        self.data['day'] = day

        # for range specified days, data will not contain the value and description
        if value:
            self.data['value'] = value
        else:
            self.data['value'] = data[day]
            description = data['description']

        if day in ['mon','tue','wed']:
            calc = int(self.data['value']) ** 2
            self.data['calc'] = calc
            self.data['description'] = ('%s %s') %(description, calc)
            template_s = '''{'day': '%(day)s', 'description': '%(description)s', 'square': %(calc)s, 'value': %(value)s }'''
            self.data['template'] = template_s
        else:
            calc = int(self.data['value']) * 2
            self.data['calc'] = calc
            self.data['description'] = ('%s %s') %(description, calc)
            template_d = '''{'day': '%(day)s', 'description': '%(description)s', 'double': %(calc)s, 'value': %(value)s }'''
            self.data['template'] = template_d

    def __str__(self):
        return self.data['template']%self.data


class Parser(object):
    '''
    This class, for a given file, will reads and parse the contents of the file,
    it has the ability to output the contents of the file in the required format
    '''
    def __init__(self, directory,filename):
        self.filename = filename
        self.file_name = os.path.join(directory,filename)
        self.file_info = self.readfile()
        self.weeks_data = self.parse_info() #into self.weeks_data


    def readfile(self):
        '''
        get and the data from the filename, and store it as key value pairs
        '''
        with open(self.file_name) as f:
            filecontent = f.read().splitlines()
        f.close()

        headers = filecontent[0]
        data = filecontent[1]

        file_info = dict(zip(headers.split(','),data.split(',')))
        return file_info

    def parse_info(self):
        '''
        get the required data for each of the week days mon-fri
        data is stored per day either
         - explicitly eg mon
         - in a range eg mon-wed
        '''

        weeks_data = collections.OrderedDict() #day:data
        week_days = ['mon','tue','wed', 'thu','fri']

        range_start_day = None #start of a day range eg mon-wed (mon)
        range_end_day = None #end of a day range eg mon-wed (wed)
        range_description = None
        range_value = None

        for week_day in week_days:

            #if self.file_info.has_key(week_day):
            if week_day in self.file_info:
                # explicit day data
                x = Daydata(week_day,self.file_info)
                weeks_data[week_day] = x

            else:
                #could not find explicit week_day
                #use day range.

                #if the range_start_day has been set, then in the middle of a range,
                #otherwise, at the start of a range.
                #NB remember to set the range_start_day to None at the end of the range processing

                if range_start_day == None:
                    #at the start of a new day range
                    #get the range vaues from the file info
                    range_description = self.file_info['description']

                    #find the end day of the range
                    for day in week_days:
                        search_for_key = '%s-%s' %(week_day,day)
                        #if self.file_info.has_key(search_for_key):
                        if search_for_key in self.file_info:
                            range_start_day, range_end_day = search_for_key.split('-')
                            range_value = self.file_info[search_for_key] #get the value from the file info

                            x = Daydata(range_start_day,self.file_info,range_value,range_description)
                            weeks_data[week_day] = x
                            break #only expect one end day
                else:
                    # save the data for a mid range day
                    x = Daydata(week_day,weeks_data[range_start_day],range_value, range_description)
                    weeks_data[week_day] = x

                    if week_day == range_end_day:
                        range_start_day = None
                        range_end_day = None

        if len(weeks_data) != len(week_days):
            raise Exception('Missing data')
        return weeks_data


    def pp(self):
        print (self.filename)
        out =[str(v) for k,v in self.weeks_data.items()]
        sep = ',\n '
        print ('[%s]' %sep.join(out))
        print ('')


if __name__ == '__main__':

    directory = 'csv_files'
    filenames = ['1.csv','2.csv','3.csv']

    #process each file, one at a time
    for filename in filenames:
        p = Parser(directory,filename)
        p.pp()
