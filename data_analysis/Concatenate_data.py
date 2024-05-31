import pandas as pd
import glob



RENAME_COLUMNS = "Timestamp,Delay,Size\n"


class Concatenate_data():
    """
    
    """
    def __init__(self, path_p, sub_directories_p=False, columns_p=[], col_all_p=False, output_path_p="./automatic_name.csv") -> None:
        """
        Concatenate data into one single file. Can use data from subdirectories.
        """
        self.path = path_p
        self.use_sub = sub_directories_p
        self.use_all_columns = col_all_p
        self.colums = columns_p
        if self.colums == []:
            self.use_all_columns = True
        self.output_path = output_path_p
        self.data = pd.DataFrame()

    

    def merge_column(self):
        """
        Append data to a single file
        Each csv's data are appened to the final file as new columns
        """
        #Work in progress
        if self.use_sub:
            csv_files = glob.glob('*.{}'.format('csv'))
            csv_files
        
        else:
            csv_files = glob.glob('./fast_KILO/*.{}'.format('csv')) 
            l = []
            
            for f in csv_files:
                l.append(pd.read_csv(f))
                
            df_res = pd.concat(l, ignore_index=True, sort=False)
            df_res.to_csv("./test.csv")
            print(df_res)


    def merge_row(self):
        """
        Append data to a single file
        Each csv's data are appened to the final file as new rows
        """

        #Work in progress
        if self.use_sub:
            csv_files = glob.glob('*.{}'.format('csv'))
            csv_files
        
        else:
            csv_files = glob.glob('./fast_KILO/*.{}'.format('csv')) 
            l = []
            
            for f in csv_files:
                l.append(pd.read_csv(f))
                
            df_res = pd.concat(l, ignore_index=True, sort=False)
            df_res.to_csv("./test.csv")
            print(df_res)
    

    def write_csv(self, path_p):
        """
        Write the name of the 
        """
        self.data.to_csv(path_p)




# concat = Concatenate_data(path_p="YES")

 
def rename_columns(column_name_p):
    """
    Rename the first column of a file
    """
    delay_files = glob.glob('/home/gabriel/Documents/TheLab/python/data_science/NLOS_exp/*/*_delay.{}'.format('csv')) 

    for fil in delay_files:

        with open(fil) as f:
            lines = f.readlines()

        lines[0] = column_name_p # ['This is the first line.\n', 'This is the second line.\n']

        with open(fil, "w") as f:
            f.writelines(lines)

        f.close()

rename_columns(RENAME_COLUMNS)